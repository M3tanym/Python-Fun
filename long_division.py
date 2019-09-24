#!/usr/bin/env python3

# Long Division with repeating decimals
# https://en.wikipedia.org/wiki/Long_division
# Special thanks to Max R and Josette G

import sys

def seen_before(numerators, n):
    for i in range(len(numerators)):
        # check each previous numerator, which are ordered backwards for convenience
        if numerators[i] == n:
            # we found a repeated numerator! This means that the last "i + 1" digits will be repeated
            i += 1 # off-by-1 because indexed at 0
            return i
    return -1

def long_division(numerator, denominator, show_math):
    ''' Return a string with the repeating decimal notation for this division '''
    # the return string, ie, the top of the long division bar
    answer = str(numerator) + '/' + str(denominator) + ' = '
    # a list of numerators we've seen -- for repeating detection
    seen_numerators = []
    # a flag to indicate if we're on the first place (before the .)
    firstPlace = True
    # a flag to indicate if we're still running through the division
    done = False

    # check for a negative answer and normalize if needed
    if numerator < 0 or denominator < 0:
       if numerator / denominator < 0:
           answer += '-'
       numerator = abs(numerator)
       denominator = abs(denominator)

    # each iteration is one "level" in the long division
    while True:
        # debug if desired
        if show_math:
            print('Numerator: ' + str(numerator))
            print('Denominator: ' + str(denominator))
            print('Numerators Seen: ' + str(seen_numerators))

        # flag in case a trailing 0 needs to be in the repating segment
        extra_zero = False
        # if the numerator doesn't go into the denominator
        if denominator > numerator:
            # add a 0 to the answer
            answer += '0'
            extra_zero = True
            # add a "." if necessary
            if firstPlace:
                answer += '.'
                firstPlace = False
            # "bring down" a 0
            numerator *= 10

        # check for previously seen numerators (repeating decimals)
        i = seen_before(seen_numerators, numerator)
        if i != -1:
            if show_math:
                print('Repeat detected!')
            # offset the index by 1 if there's an extra zero to include
            if extra_zero:
                i += 1
            answer = answer[:-i] + '(' + answer[-i:] + ')'
            # answer = [the non-repeating part] + ( + [the repeating part] + )
            break
        # mark that we've seen this numerator
        seen_numerators.insert(0, numerator)

        # get the next digit with integer division
        digit = numerator // denominator
        # find the remainder (new numerator), could also be done with mod
        numerator = numerator - (denominator * digit)
        # add the digit to the string
        answer += str(digit)
        # add a "." if necessary (only if there are more decimals)
        if firstPlace and numerator != 0:
            answer += '.'
            firstPlace = False
        # "bring down" a 0
        numerator *= 10

        # if the numerator is 0, we're done!
        if numerator == 0:
            break

        # print debug info if desired
        if show_math:
            print('Added Digit: ' + str(digit))
            print('Answer is currently: ' + answer)
            print('')

    # after the loop, return the answer string
    return answer

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: ' + sys.argv[0] + ' numerator denominator [(v)erbose]')
    else:
        show_math = len(sys.argv) > 3 # if a fourth arg is provided, show the long division
        answer = long_division(int(sys.argv[1]), int(sys.argv[2]), show_math)
        print(answer)
