DEFAULT_INPUT = 'day1.txt'

def part_1(loc=DEFAULT_INPUT):
    with open(loc) as f:
        return sum(map(int, f.readlines()))

def part_2(loc=DEFAULT_INPUT):
    with open(loc) as f:
        inputs = list(map(int, f.readlines()))
    seen = set()
    i = 0
    current = 0
    while True:
        current += inputs[i]
        if current in seen:
            return current
        else:
            seen.add(current)
            i += 1
            i %= len(inputs)

if __name__ == '__main__':
    print('Solution for Part One:', part_1())
    print('Solution for Part Two:', part_2())
