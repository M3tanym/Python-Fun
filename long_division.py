#!/usr/bin/env python3

# Long Division with repeating decimals
# https://en.wikipedia.org/wiki/Long_division
# Special thanks to Max R and Josette G 

import sys

def long_division(numerator, denominator):
    ''' Return a string with the repeating decimal notation for this division '''
    # the return string, ie, the top of the long division bar
    answer = str(numerator) + '/' + str(denominator) + ' = '
    # a list of numerators we've seen -- for repeating detection
    seen_numerators = []
    # a flag to indicate if we're on the first place (before the .)
    firstPlace = True
    # a flag to indicate if we're still running through the division
    done = False
    
    # each iteration is one "level" in the long division
    while not done:
        # if the numerator doesn't go into the denominator
        if numerator < denominator:
            # "bring down" a 0, ie, multiply by 10
            numerator *= 10
            # add a 0 to the answer
            answer += '0'
            # check if this was the first digit/number, if so, add a "." and clear the flag
            if firstPlace:
                answer += '.'
                firstPlace = False

        # mark that we've seen this numerator
        seen_numerators.insert(0, numerator)

        #print('seen_numerators seen: ' + str(seen_numerators))
        #print('Numerator: ' + str(numerator))
        #print('Denominator: ' + str(denominator))

        # get the next digit with integer division
        digit = numerator // denominator
        # find the remainder with modulus
        remainder = numerator % denominator
        # "bring down" a 0
        new_numerator = remainder * 10

        # add the digit to the string and add a "." if necessary
        answer += str(digit)
        if firstPlace:
            answer += '.'
            firstPlace = False

        #print('Next Digit: ' + str(digit))
        #print('New Numerator: ' + str(new_numerator))
        #print('')

        # if the next numerator is 0, we're done!
        if new_numerator == 0:
            break
        # check for repeating decimals
        for i in range(len(seen_numerators)):
            # check each see numerator, which are ordered backwards for convenience
            if seen_numerators[i] == new_numerator:
                # we found a repeated numerator! This means that the last "i" digits will be repeated
                # insert parentheses accordingly
                i += 1 # off-by-1 because indexed at 0
                answer = answer[:-i] + '(' + answer[-i:] + ')'
                # ans = [the non-repeating part] + ( + [the repeating part] + )
                done = True
                # flag to exit the loop
                break
        # prepare for the next iteration by setting the numerator
        numerator = new_numerator
    # after the loop, return the answer string
    return answer

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: ./' + sys.argv[0] + ' [numerator] [denominator]')
    else:
        answer = long_division(int(sys.argv[1]), int(sys.argv[2]))
        print(answer)
