#!/usr/bin/env python
import argparse
import sys
import codecs
if sys.version_info[0] == 2:
  from itertools import izip
else:
  izip = zip
from collections import defaultdict as dd
import re
import os.path
import gzip
import tempfile
import shutil
import atexit

# Use word_tokenize to split raw text into words
from string import punctuation

import nltk
from nltk.tokenize import word_tokenize

scriptdir = os.path.dirname(os.path.abspath(__file__))

reader = codecs.getreader('utf8')
writer = codecs.getwriter('utf8')

def prepfile(fh, code):
  if type(fh) is str:
    fh = open(fh, code)
  ret = gzip.open(fh.name, code if code.endswith("t") else code+"t") if fh.name.endswith(".gz") else fh
  if sys.version_info[0] == 2:
    if code.startswith('r'):
      ret = reader(fh)
    elif code.startswith('w'):
      ret = writer(fh)
    else:
      sys.stderr.write("I didn't understand code "+code+"\n")
      sys.exit(1)
  return ret

def addonoffarg(parser, arg, dest=None, default=True, help="TODO"):
  ''' add the switches --arg and --no-arg that set parser.arg to true/false, respectively'''
  group = parser.add_mutually_exclusive_group()
  dest = arg if dest is None else dest
  group.add_argument('--%s' % arg, dest=dest, action='store_true', default=default, help=help)
  group.add_argument('--no-%s' % arg, dest=dest, action='store_false', default=default, help="See --%s" % arg)


class LimerickDetector:

    def __init__(self):
        """
        Initializes the object to have a pronunciation dictionary available
        """
        self._pronunciations = nltk.corpus.cmudict.dict()
        self.digits = [str(i) for i in range(0,10)]

    def apostrophe_tokenize(self, line):
        words = re.split("\s+", line)
        results = []
        for word in words:
            match = re.match("([a-z]+)([,.])", word)
            if(match):
                results+= match.groups()
            else:
                results.append(word)
        return results

    def guess_syllables(self, word):
        vowels = ['a', 'e', 'i', 'o', 'u', 'y']
        count = 0
        prev = False
        first_found = False
        for char in word:

            if char in vowels and prev==False:
                count += 1
                first_found = True
                prev = True
            else:
                if first_found :
                    prev = False
        if prev == True and count >= 2:
            return count -1
        return count




    #return 1 if consonant
    def isConsonant(self, char):
        if char in self.digits:
            return 0
        return 1
    def isDigit(self, char):
        if char in self.digits:
            return 1
        return 0
    def num_syllables1(self, word):
        """
        Returns the number of syllables in a word.  If there's more than one
        pronunciation, take the shorter one.  If there is no entry in the
        dictionary, return 1.
        """

        # TODO: provide an implementation!
        if word in self._pronunciations:
            pronunciations = self._pronunciations[word]
            syllableCountList = []
            for pronunciation in pronunciations :
                numberOfSyllables = 0
                for phones in pronunciation:
                    if self.isDigit(phones[-1]):
                        numberOfSyllables += 1
                syllableCountList.append(numberOfSyllables)

            return min(syllableCountList)

        return 1
    def getIndexOfFirstVowel(self, word):
        for i in range(0, len(word)):
            if self.isDigit(word[i][-1]):
                return i

        return -1
    #returns true if second is a subset of first
    def isSubset(self, first, second):
        if(len(second) > len(first)):
            return False
        if(second == first[(len(first) - len(second)):]):
            return True
        return False

    def isRhymingCheck(self, firstWord, secondWord):
        """
        Returns True if two words (represented as lower-case strings) rhyme,
        False otherwise.
        """

        if(len(firstWord) != len(secondWord)):
            if(len(firstWord) > len(secondWord)):
                secondWordVowelIndex = self.getIndexOfFirstVowel(secondWord)
                if(secondWordVowelIndex != -1 ):
                    isRhyming = self.isSubset(firstWord, secondWord[secondWordVowelIndex : ])

            else:
                firstWordVowelIndex = self.getIndexOfFirstVowel(firstWord)
                if(firstWordVowelIndex != -1 ):
                    isRhyming = self.isSubset(secondWord, firstWord[firstWordVowelIndex : ])
        else:
            firstWordVowelIndex = self.getIndexOfFirstVowel(firstWord)
            secondWordVowelIndex = self.getIndexOfFirstVowel(secondWord)

            if(firstWordVowelIndex != -1 and secondWordVowelIndex != -1):
                isRhyming = self.isSubset(secondWord[secondWordVowelIndex : ], firstWord[firstWordVowelIndex : ])

        return isRhyming

    def rhymes(self, a, b):

        """
        Returns True if two words (represented as lower-case strings) rhyme,
        False otherwise.
        """
        #if lengths dont match
        isRhyming = False
        if not {a, b} <= set(self._pronunciations):
           return False

        firstWord = self._pronunciations[a]
        secondWord = self._pronunciations[b]

        for i in firstWord:
            for j in secondWord:
                isRhyming = self.isRhymingCheck(i, j) or isRhyming
        return isRhyming
    def isPunctuation(self, char):
        if char in [',', '.', '!']:
            return True
        return False
    def clean(self, line):
        if self.isPunctuation(line[-1]):
            line.pop(len(line)-1)
        for i in range(0, len(line)):
            if len(line[i])==0 and self.isPunctuation(line[i]):
                line.pop(len(line)-1)
        return line
    def getNumberOfSyllablesInLine(self, line):
        count = 0
        for i in line:
            count += self.num_syllables(i)
        return count


    def is_limerick(self, text):
        """
        Takes text where lines are separated by newline characters.  Returns
        True if the text is a limerick, False otherwise.

        A limerick is defined as a poem with the form AABBA, where the A lines
        rhyme with each other, the B lines rhyme with each other, and the A lines do not
        rhyme with the B lines.


        Additionally, the following syllable constraints should be observed:
          * No two A lines should differ in their number of syllables by more than two.
          * The B lines should differ in their number of syllables by no more than two.
          * Each of the B lines should have fewer syllables than each of the A lines.
          * No line should have fewer than 4 syllables

        (English professors may disagree with this definition, but that's what
        we're using here.)

        """
        A_LINES = [0,1,4]
        lines = re.split("\n", text)

        linesTokenised = []
        for line in lines:
            line = line.strip()
            if(len(line) > 0):
                tokenisedLines = nltk.tokenize.word_tokenize(line)
                tokenisedLines = map(lambda x : self.clean(x), [tokenisedLines])
                linesTokenised += (tokenisedLines)

        numSyllablesInLine = []
        if(len(linesTokenised) < 5):
            return False
        if not (self.rhymes(linesTokenised[0][-1], linesTokenised[1][-1]) and self.rhymes(linesTokenised[1][-1], linesTokenised[4][-1])):
            return False
        for i in linesTokenised:
            numSyllablesInLine.append(self.getNumberOfSyllablesInLine(i))
        for i in numSyllablesInLine:
            if i < 4:
                return False
        if(abs(numSyllablesInLine[0] - numSyllablesInLine[1])>2 or abs(numSyllablesInLine[1] - numSyllablesInLine[4])>2 or abs(numSyllablesInLine[0] - numSyllablesInLine[4])>2):
            return False
        if(abs(numSyllablesInLine[2] - numSyllablesInLine[3])>2 ):
            return False
        if(numSyllablesInLine[2] > numSyllablesInLine[0] or numSyllablesInLine[2] > numSyllablesInLine[1] or numSyllablesInLine[2] > numSyllablesInLine[4]):
            return False
        if(numSyllablesInLine[3] > numSyllablesInLine[0] or numSyllablesInLine[3] > numSyllablesInLine[1] or numSyllablesInLine[3] > numSyllablesInLine[4]):
            return False
        return True







        # TODO: provide an implementation!
        return False


# The code below should not need to be modified
def main():
  parser = argparse.ArgumentParser(description="limerick detector. Given a file containing a poem, indicate whether that poem is a limerick or not",
                                   formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  addonoffarg(parser, 'debug', help="debug mode", default=False)
  parser.add_argument("--infile", "-i", nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="input file")
  parser.add_argument("--outfile", "-o", nargs='?', type=argparse.FileType('w'), default=sys.stdout, help="output file")




  try:
    args = parser.parse_args()
  except IOError as msg:
    parser.error(str(msg))

  infile = prepfile(args.infile, 'r')
  outfile = prepfile(args.outfile, 'w')

  ld = LimerickDetector()
  lines = ''.join(infile.readlines())
  outfile.write("{}\n-----------\n{}\n".format(lines.strip(), ld.is_limerick(lines)))

if __name__ == '__main__':
  main()

