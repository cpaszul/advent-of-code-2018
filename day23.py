import re

DEFAULT_INPUT = 'day23.txt'

def day_23(loc=DEFAULT_INPUT):
    with open(loc) as f:
        lines = list(f.readlines())
    pattern = re.compile(r'pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)')
    bots = []
    for line in lines:
        s = pattern.search(line)
        bots.append(tuple(map(int, s.groups())))
    largest_radius = max(bots, key=lambda b:b[3])
    part_one = len([b for b in bots
                    if distance(b, largest_radius) <= largest_radius[3]])
    return part_one, 'Part Two solution obtained using solution found here: https://www.reddit.com/r/adventofcode/comments/a8s17l/2018_day_23_solutions/ecddus1/'

def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])


if __name__ == '__main__':
    print('Solution for Part One: {}\nSolution for Part Two: {}'.format(*day_23()))
   
