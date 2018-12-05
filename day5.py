from string import ascii_lowercase

DEFAULT_INPUT = 'day5.txt'

def part_1(loc=DEFAULT_INPUT):
    with open(loc) as f:
        polymer = f.readline()
    polymer = fully_reduce_polymer(polymer)
    return len(polymer)

def fully_reduce_polymer(polymer):
    while True:
        current_len = len(polymer)
        polymer = reduce_polymer(polymer)
        if len(polymer) == current_len:
            break
    return polymer

def reduce_polymer(polymer):
    new_polymer = []
    for char in polymer:
        if new_polymer:
            prev_char = new_polymer[-1]
            if char.lower() == prev_char.lower() and char != prev_char:
                new_polymer.pop(-1)
            else:
                new_polymer.append(char)
        else:
            new_polymer.append(char)
    return ''.join(new_polymer)
            
def part_2(loc=DEFAULT_INPUT):
    with open(loc) as f:
        polymer = f.readline()
    current_min = len(polymer)
    for char in ascii_lowercase:
        poly = fully_reduce_polymer(''.join(poly_char
                                            for poly_char in polymer
                                            if poly_char.lower() != char))
        current_min = min(current_min, len(poly))
    return current_min
        
if __name__ == '__main__':
    print('Solution for Part One:', part_1())
    print('Solution for Part Two:', part_2())
