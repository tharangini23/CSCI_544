import tree
import re
import time
import math
import sys, fileinput
import matplotlib.pyplot as plt

def parseFromTable(start, end,  root, back):

    cur = back[start][end][root]
    if len(cur)==1:
        return  "("+root+" "+cur[0]+")"
    split = cur[0]
    l = cur[1]
    r = cur[2]
    right = parseFromTable(split, end, r, back)
    left = parseFromTable(start, split, l, back)
    return "(" + root +" "+left +" "+right +")"

def getRules(NON_TERMINALS, B, C):
    all_combi = []
    for A in NON_TERMINALS:
        for b in B:
            res = []
            for c in C:
                res.append(A)
                res.append(b)
                res.append(c)
                all_combi.append(res)
                res = []


    return all_combi

def buildChart(words, grammer, NON_TERMINALS):
    score = [[{} for i in range(0, len(words)+1)] for j in  range(0, len(words)+1)]
    back = [[{} for i in range(0, len(words)+1)] for j in  range(0, len(words)+1)]
    i=0
    for i in range(0, len(words)):
        begin = i
        end = i+1


        for A in NON_TERMINALS:
            rule = A+","+ words[i]

            if rule in grammer:
                ruleDict = score[begin][end]
                if A in ruleDict:#check if it has already been generated in score
                    #probability check
                    if ruleDict[A]<grammer[rule]:
                        ruleDict[A] =grammer[rule]
                        back[begin][end][A] = [words[i]]
                        score[begin][end] = ruleDict
                else:
                    ruleDict[A] =grammer[rule]

                    back[begin][end][A] = [words[i]]
                    score[begin][end] = ruleDict

    #print score
    for span in range(2, len(words)+1):
        for begin in range(0, len(words)-span+1):
            end = begin + span
            for split in range(begin+1, end+1):
                B = score[begin][split].keys()
                C = score[split][end].keys()
                for rule in getRules(NON_TERMINALS, B, C):
                    if ",".join(rule) in grammer:
                        prob = score[begin][split][rule[1]]*score[split][end][rule[2]]*grammer[",".join(rule)]
                        all_rules =score[begin][end]
                        if rule[0] in all_rules:
                            if prob > all_rules[rule[0]]:
                                all_rules[rule[0]]=prob
                                score[begin][end] = all_rules
                                back[begin][end][rule[0]] = [split ,rule[1],rule[2]]
                        else:
                            all_rules[rule[0]]=prob
                            score[begin][end] = all_rules
                            back[begin][end][rule[0]] = [split ,rule[1],rule[2]]


    #for i in score:
    #     print i
    output = ""
    if len(back[0][len(back[0])-1].keys())==0:
        output=""
    else:
        output =  parseFromTable(0, len(back[0])-1, "TOP",back)

    return output
def drawPlot(parseingTime, sentenceLength):
    plt.subplot(221)
    plt.plot(sentenceLength, parseingTime, 'ro')
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Sentence Length')
    plt.ylabel('Parseing Time')
    plt.title('parsing time vs length')
    plt.show()


def getRulesInTheTree(tree, ruleCount, pblityCountHelper, TERMINALS, treeString):
    treeNodeQueue = []
    treeNodeQueue.append(tree.root)
    while len(treeNodeQueue) > 0:
        lhs = treeNodeQueue.pop()
        rule = [str(lhs)]
        children = lhs.children

        for r in children:
            rule.append(str(r))
            if len(r.children)>0:
                treeNodeQueue.append(r)
        rule_key = ",".join(rule)
        if len(children) == 1:
            TERMINALS.add(str(children[0]))

        #store count of rules
        if rule_key not in ruleCount:
            ruleCount[rule_key] = 0
        ruleCount[rule_key] = ruleCount[rule_key] + 1

        #store count of rules with rhs as key
        if str(lhs) not in pblityCountHelper:
            pblityCountHelper[str(lhs)] = {}
        allRhs = pblityCountHelper[str(lhs)]
        allRhs[rule_key] = allRhs.get(rule_key,0) + 1
        pblityCountHelper[str(lhs)] = allRhs

def writeToFile(str, fileName):
    f = open(fileName, 'w')
    f.write(str)


def readTreesAndGetRules(inputTestFile):
    #key ="A,B,C" value = count
    ruleCount = {}
    #key ="A" value = [["A,B,C",3],["A,milk",1]]
    #key ="A" value = {"A,B,C":3,"A,milk":1} dict of dict
    pblityCountHelper = {}
    TERMINALS = set()
    for treeString in open("train.trees.pre.unk","r"):
        t = tree.Tree.from_str(treeString)

        getRulesInTheTree(t, ruleCount, pblityCountHelper, TERMINALS, treeString)


    NON_TERMINALS = pblityCountHelper.keys()

    pblityCount = {}
    sentenceLength = []
    parseingTime = []
    for lhs in pblityCountHelper:
        #total occurance of lhs
        total = sum(pblityCountHelper[lhs].values())
        allRhs = pblityCountHelper[lhs]
        for rhs in allRhs:
            rhsCount = allRhs[rhs]
            pblityCount[rhs] = float(rhsCount)/total

    ruleString = ""
    for rule in pblityCount:

        pblty = pblityCount[rule]
        rule = re.split(",",rule)
        formattedRule = rule[0]+" -> "+" ".join(rule[1:])

        ruleString+= formattedRule + " # "+ str(pblty)+"\n"
        #print ruleString
    writeToFile(ruleString, "rules" )

    words = ["What is <unk> I A ?"]
    output = ""
    for sentence in open(inputTestFile,"r"):
    #for sentence in words:
        s = sentence.strip().split(" ")
        sentence = sentence.strip().split(" ")

        for i in range(0, len(sentence)):
            if sentence[i] not in TERMINALS :

                sentence[i] = "<unk>"

        #print i, sentence
        startTime = time.time()
        parsedTree = buildChart(sentence, pblityCount, NON_TERMINALS)
        output += parsedTree
        output += "\n"
        endTime = time.time()
        if len(parsedTree)>0:
            parseingTime.append(endTime - startTime )
            sentenceLength.append(len(s))
    #print output
    #drawPlot(parseingTime, sentenceLength)
    return output

"""
    pblityCount = {}
    pblityCount["S,NP,VP"]=1.0
    pblityCount["NP,DT,NN"]=0.3
    pblityCount["NP,NN,NNS"]=0.6
    pblityCount["VP,VBP,NP"]=0.7
    pblityCount["VP,VP,PP"]=0.2
    pblityCount["PP,IN,NP"]=1.0
    pblityCount["NP,time"]=0.05
    pblityCount["NP,fruit"]=0.05
    pblityCount["VP,flies"]=0.1
    pblityCount["DT,a"]=0.5
    pblityCount["DT,an"]=0.5
    pblityCount["NN,time"]=0.25
    pblityCount["NN,fruit"]=0.25
    pblityCount["NN,arrow"]=0.25
    pblityCount["NN,banana"]=0.25
    pblityCount["VBP,like"]=1.0
    pblityCount["NNS,flies"]=1.0
    pblityCount["IN,like"]=1.0
    NON_TERMINALS = ["S","NP","VP","DT","NN","NNS","VBP","PP","IN"]
"""


def main():
    args = sys.argv
    output = readTreesAndGetRules(args[1])
    print output




if __name__ == '__main__':
  main()
