import re
from collections import Counter

DEFAULT_INPUT = 'day3.txt'

def day_3(loc=DEFAULT_INPUT):
    claimed = Counter()
    claims = []
    with open(loc) as f:
        for line in f.readlines():
            id_, x, y, width, height = map(int, re.split(r'\D+', line)[1:6])
            claims.append((id_, x, y, width, height))
            for i in range(width):
                for j in range(height):
                    claimed[(x + i, y + j)] += 1
    overlaps = sum(1 for val in claimed.values() if val > 1)
    no_overlap_id = None
    for id_, x, y, width, height in claims:
        overlap = False
        for i in range(width):
            for j in range(height):
                cell = (x + i, y + j)
                if claimed[cell] > 1:
                    overlap = True
        if not overlap:
            no_overlap_id = id_
            break
    return overlaps, no_overlap_id

if __name__ == '__main__':
    print('Solution for Part One: {}\nSolution for Part Two: {}'.format(*day_3()))
