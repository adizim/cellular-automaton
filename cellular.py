import argparse
import pdb
from sys import stdout

def decimal_to_binary(x):
    """
    This function converts a decimal number N into a binary number with 8 bits.
    :param x: The decimal number

    >>> decimal_to_binary(30)
    '00011110'
    >>> decimal_to_binary(139)
    '10001011'
    """
    assert 0 <= x <= 255
    return bin(x)[2:].zfill(8)


def decimal_to_key(x):
    """
    This function converts a decimal number N into a 3 bit input key.
    :param x: The decimal number

    >>> decimal_to_key(1)
    ('0', '0', '1')
    >>> decimal_to_key(5)
    ('1', '0', '1')
    >>> decimal_to_key(7)
    ('1', '1', '1')
    """
    assert 0 <= x <= 7
    return tuple(bin(x)[2:].zfill(3))


def calculate_state(state, rule_map):
    new_state = [rule_map[tuple(["0"] + state[:2])]]

    for i in range(len(state) - 2):
        new_state += [rule_map[tuple(state[i:i + 3])]]

    new_state += [rule_map[tuple(state[len(state) - 2:] + ["0"])]]
    return new_state


def generate(rule, steps, file=None):
    """
    Generate the image from given rule number and steps
    and print it to the console.
    The output image should have width of 2 * STEPS + 1 and height of STEPS + 1.

    :param rule: The rule number
    :param steps: Number of lines

    >>> generate(30, 5)
    P1 11 6
    0 0 0 0 0 1 0 0 0 0 0
    0 0 0 0 1 1 1 0 0 0 0
    0 0 0 1 1 0 0 1 0 0 0
    0 0 1 1 0 1 1 1 1 0 0
    0 1 1 0 0 1 0 0 0 1 0
    1 1 0 1 1 1 1 0 1 1 1
    """
    brule = decimal_to_binary(rule)
    rule_map = {tuple(decimal_to_key(i)): brule[7 - i] for i in range(8)}
    state = ["0"] * steps + ["1"] + ["0"] * steps
    if file:
        file.write(f"P1 {2 * steps + 1} {steps + 1}" + "\n")
        file.write(" ".join(state) + "\n")
    else:
        print(f"P1 {2 * steps + 1} {steps + 1}" + "\n")
        print(" ".join(state) + "\n")

    for _ in range(steps):
        state = calculate_state(state, rule_map)
        if file:
            file.write(" ".join(state) + "\n")
        else:
            print(" ".join(state) + "\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Cellular Automaton')
    parser.add_argument('rule', help='The Rule', type=int)
    parser.add_argument('steps', help='Number of Steps', type=int)
    parser.add_argument('-f', '--file', help='Save to a file', type=argparse.FileType('w'), default=stdout)
    parser.add_argument('-w', '--wolfram', help='Produce a Wolfram Atlas correct solution using infinite grid',
                        action='store_true')
    args = parser.parse_args()
    rule, steps, file = args.rule, args.steps, args.file

    assert 0 <= rule <= 255 and steps >= 0
    generate(rule, steps, file)
