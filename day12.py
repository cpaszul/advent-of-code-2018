from collections import defaultdict

DEFAULT_INPUT = 'day12.txt'

def part_1(loc=DEFAULT_INPUT):
    plants = defaultdict(lambda: '.')
    rules = {}
    with open(loc) as f:
        first = f.readline()
        initial = first.split(' ')[2]
        for index, char in enumerate(initial):
            if char == '#':
                plants[index] = '#'
        f.readline()
        for line in f.readlines():
            rule, result = line.rstrip().split(' => ')
            rules[rule] = result
    for _ in range(20):
        plants = advance(plants, rules)
    return sum(key for key, val in plants.items() if val == '#')

def advance(plants, rules):
    new_plants = defaultdict(lambda: '.')
    leftmost = min(key for key, val in plants.items() if val == '#') - 2
    rightmost = max(key for key, val in plants.items() if val == '#') + 2
    for n in range(leftmost, rightmost + 1):
        pattern = plants[n - 2] + plants[n - 1] + plants[n] + plants[n + 1] + plants[n + 2]
        if pattern in rules:
            new_plants[n] = rules[pattern]
    return new_plants

def part_2(loc=DEFAULT_INPUT):
    plants = defaultdict(lambda: '.')
    rules = {}
    with open(loc) as f:
        first = f.readline()
        initial = first.split(' ')[2]
        for index, char in enumerate(initial):
            if char == '#':
                plants[index] = '#'
        f.readline()
        for line in f.readlines():
            rule, result = line.rstrip().split(' => ')
            rules[rule] = result
    i = 0
    for _ in range(2500):
        plants = advance(plants, rules)
        i += 1
    size_one = sum(key for key, val in plants.items() if val == '#')
    for _ in range(250):
        plants = advance(plants, rules)
        i += 1
    size_two = sum(key for key, val in plants.items() if val == '#')
    average_growth = (size_two - size_one) // 250
    return size_two + average_growth * (50000000000 - 2750)
            


if __name__ == '__main__':
    print('Solution for Part One:', part_1())
    print('Solution for Part Two:', part_2())
