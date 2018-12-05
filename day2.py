from collections import Counter

DEFAULT_INPUT = 'day2.txt'

def part_1(loc=DEFAULT_INPUT):
    twos, threes = 0, 0
    with open(loc) as f:
        for line in f.readlines():
            c = Counter(line.rstrip())
            if 2 in c.values():
                twos += 1
            if 3 in c.values():
                threes += 1
    return twos * threes
            
def part_2(loc=DEFAULT_INPUT):
    seen = []
    with open(loc) as f:
        for line in f.readlines():
            line = line.rstrip()
            for seen_line in seen:
                if diff(line, seen_line) == 1:
                    return ''.join(c1 for c1, c2 in zip(line, seen_line)
                                   if c1 == c2)
            seen.append(line)

def diff(s1, s2):
    return sum(1 for c1, c2 in zip(s1, s2) if c1 != c2)

if __name__ == '__main__':
    print('Solution for Part One:', part_1())
    print('Solution for Part Two:', part_2())
