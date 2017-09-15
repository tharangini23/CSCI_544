from fst import FST
import string, sys
from fsmutils import composechars, trace

def letters_to_numbers():
    vowels = ['a', 'e', 'i', 'o', 'u', 'h', 'w', 'y']
    f1 = FST('fst1')
    f1.add_state('start')
    f1.initial_state = 'start'
    f1.add_state('first')
    f1.set_final('first')
    f1.add_state('g1')
    f1.set_final('g1')
    f1.add_state('g2')
    f1.set_final('g2')
    f1.add_state('g3')
    f1.set_final('g3')
    f1.add_state('g4')
    f1.set_final('g4')
    f1.add_state('g5')
    f1.set_final('g5')
    f1.add_state('g6')
    f1.set_final('g6')


    f1.set_final('start')
    num = {}
    g1 = ['b', 'f', 'v', 'p']
    g2 = ['c', 'g', 'j', 'k', 'q', 's', 'x', 'z']
    g3 = ['d', 't']
    g4 = ['l']
    g5 = ['m', 'n']
    g6 = ['r']

    one = ((i, 1) for i in ['b', 'f', 'v', 'p'])
    two = ((i, 2) for i in ['c', 'g', 'j', 'k', 'q', 's', 'x', 'z'])
    num = dict(one)
    num.update(two)
    num['d'] = 3
    num['t'] = 3
    num['l'] = 4
    num['m'] = 5
    num['n'] = 5
    num['r'] = 6
    print(num)

    first = True
    firstOccurrences = []
    for letter in string.ascii_letters:

        if letter.lower() in vowels:
             _ = f1.add_arc('start', 'first', (letter), (letter))
             _ = f1.add_arc('first', 'first', (letter), (''))
             _ = f1.add_arc('g1', 'first', (letter), (''))
             _ = f1.add_arc('g2', 'first', (letter), (''))
             _ = f1.add_arc('g3', 'first', (letter), (''))
             _ = f1.add_arc('g4', 'first', (letter), (''))
             _ = f1.add_arc('g5', 'first', (letter), (''))
             _ = f1.add_arc('g6', 'first', (letter), (''))

        elif letter.lower() in g1:
            _ = f1.add_arc('start', 'g1', (letter), (letter))
            _ = f1.add_arc('first', 'g1', (letter), ('1'))
            _ = f1.add_arc('g1', 'g1', (letter), (''))
            _ = f1.add_arc('g2', 'g1', (letter), ('1'))
            _ = f1.add_arc('g3', 'g1', (letter), ('1'))
            _ = f1.add_arc('g4', 'g1', (letter), ('1'))
            _ = f1.add_arc('g5', 'g1', (letter), ('1'))
            _ = f1.add_arc('g6', 'g1', (letter), ('1'))

        elif letter.lower() in g2:
            _ = f1.add_arc('start', 'g2', (letter), (letter))
            _ = f1.add_arc('first', 'g2', (letter), ('2'))
            _ = f1.add_arc('g2', 'g2', (letter), (''))
            _ = f1.add_arc('g1', 'g2', (letter), ('2'))
            _ = f1.add_arc('g3', 'g2', (letter), ('2'))
            _ = f1.add_arc('g4', 'g2', (letter), ('2'))
            _ = f1.add_arc('g5', 'g2', (letter), ('2'))
            _ = f1.add_arc('g6', 'g2', (letter), ('2'))

        elif letter.lower() in g3:
            _ = f1.add_arc('start', 'g3', (letter), (letter))
            _ = f1.add_arc('first', 'g3', (letter), ('3'))
            _ = f1.add_arc('g3', 'g3', (letter), (''))
            _ = f1.add_arc('g1', 'g3', (letter), ('3'))
            _ = f1.add_arc('g2', 'g3', (letter), ('3'))
            _ = f1.add_arc('g4', 'g3', (letter), ('3'))
            _ = f1.add_arc('g5', 'g3', (letter), ('3'))
            _ = f1.add_arc('g6', 'g3', (letter), ('3'))

        elif letter.lower() in g4:
            _ = f1.add_arc('start', 'g4', (letter), (letter))
            _ = f1.add_arc('first', 'g4', (letter), ('4'))
            _ = f1.add_arc('g4', 'g4', (letter), (''))
            _ = f1.add_arc('g1', 'g4', (letter), ('4'))
            _ = f1.add_arc('g2', 'g4', (letter), ('4'))
            _ = f1.add_arc('g3', 'g4', (letter), ('4'))
            _ = f1.add_arc('g5', 'g4', (letter), ('4'))
            _ = f1.add_arc('g6', 'g4', (letter), ('4'))
        elif letter.lower() in g5:
            _ = f1.add_arc('start', 'g5', (letter), (letter))
            _ = f1.add_arc('first', 'g5', (letter), ('5'))
            _ = f1.add_arc('g5', 'g5', (letter), (''))
            _ = f1.add_arc('g1', 'g5', (letter), ('5'))
            _ = f1.add_arc('g2', 'g5', (letter), ('5'))
            _ = f1.add_arc('g3', 'g5', (letter), ('5'))
            _ = f1.add_arc('g4', 'g5', (letter), ('5'))
            _ = f1.add_arc('g6', 'g5', (letter), ('5'))
        elif letter.lower() in g6:
            _ = f1.add_arc('start', 'g6', (letter), (letter))
            _ = f1.add_arc('first', 'g6', (letter), ('6'))
            _ = f1.add_arc('g6', 'g6', (letter), (''))
            _ = f1.add_arc('g1', 'g6', (letter), ('6'))
            _ = f1.add_arc('g2', 'g6', (letter), ('6'))
            _ = f1.add_arc('g3', 'g6', (letter), ('6'))
            _ = f1.add_arc('g4', 'g6', (letter), ('6'))
            _ = f1.add_arc('g5', 'g6', (letter), ('6'))




    return f1

    # The stub code above converts all letters except the first into '0'.
    # How can you change it to do the right conversion?

def truncate_to_three_digits():
    """
    Create an FST that will truncate a soundex string to three digits
    """

    # Ok so now let's do the second FST, the one that will truncate
    # the number of digits to 3
    f2 = FST('soundex-truncate')
# Indicate initial and final states


    f2.add_state('1')
    f2.set_final('1')
    f2.initial_state = '1'
    f2.add_state('2')
    f2.set_final('2')
    f2.add_state('3')
    f2.set_final('3')
    f2.add_state('4')
    f2.set_final('4')

    # Add the arcs
    for letter in string.letters:
        f2.add_arc('1', '1', (letter), (letter))

    for n in range(10):
        f2.add_arc('1', '2', (str(n)), (str(n)))
        f2.add_arc('2', '3', (str(n)), (str(n)))
        f2.add_arc('3', '4', (str(n)), (str(n)))
        f2.add_arc('4', '4', (str(n)), (''))

    return f2

    # The above stub code doesn't do any truncating at all -- it passes letter and number input through
    # what changes would make it truncate digits to 3?

def add_zero_padding():
    # Now, the third fst - the zero-padding fst
    f3 = FST('soundex-padzero')


    f3.add_state('0')
    f3.add_state('1')
    f3.add_state('2')
    f3.add_state('3')

    f3.initial_state = '0'
    f3.set_final('3')

    for letter in string.letters:
        f3.add_arc('0', '0', (letter), (letter))
    for number in xrange(10):
        f3.add_arc('0', '1', (str(number)), (str(number)))
        f3.add_arc('1', '2', (str(number)), (str(number)))
        f3.add_arc('2', '3', (str(number)), (str(number)))

        #f3.add_arc('3', '3', (str(number)), '')
    f3.add_arc('0', '3', (''), ('000'))
    f3.add_arc('1', '3', (''), ('00'))
    f3.add_arc('2', '3', (''), ('0'))
    return f3

    # The above code adds zeroes but doesn't have any padding logic. Add some!

if __name__ == '__main__':
    user_input = raw_input().strip()
    f1 = letters_to_numbers()
    f2 = truncate_to_three_digits()
    f3 = add_zero_padding()

    if user_input:
        print("%s -> %s" % (user_input, composechars(tuple(user_input), f1, f2, f3)))
