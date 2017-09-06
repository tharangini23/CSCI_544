# import the fst module
import fst
# import the string module
import string
# Dene a list of all vowels for convenience
vowels = ['a', 'e', 'i', 'o', 'u']
# Instantiate an FST object with some name
f = fst.FST('devowelizer')
# All we need is a single state ...
f.add_state('1')
# and this same state is the initial and the nal state
f.initial_state = '1'
f.set_final('1')
# Now, we need to add an arc for each letter; if the letter is a vowel
# then the transition outputs nothing but otherwise it outputs the same
# letter that it consumed.
for letter in string.ascii_lowercase:
    if letter in vowels:
        _ = f.add_arc('1', '1', (letter), ())
    else:
        _ = f.add_arc('1', '1', (letter), (letter))

# Evaluate it on some example wordsprint ''.join(f.transduce(['v', 'o', 'w', 'e', 'l']))
print ''.join(f.transduce('e x c e p t i o n'.split()))
