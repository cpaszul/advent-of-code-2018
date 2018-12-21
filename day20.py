from collections import defaultdict

DEFAULT_INPUT = 'day20.txt'

def day_20(loc=DEFAULT_INPUT):
    with open(loc) as f:
        line = f.readline()
    grid = defaultdict(set)
    x, y = 0, 0
    prev_x, prev_y = 0, 0
    dirs = {'N': (0, 1), 'E': (1, 0), 'S': (0, -1), 'W': (-1, 0)}
    pos_stack = []
    distances = {(0, 0): 0}
    for char in line[1:-1]:
        if char == '(':
            pos_stack.append((x, y))
        elif char == '|':
            x, y = pos_stack[-1]
        elif char == ')':
            x, y = pos_stack.pop()
        else:
            dx, dy = dirs[char]
            x += dx
            y += dy
            grid[(prev_x, prev_y)].add((x, y))
            grid[(x, y)].add((prev_x, prev_y))
            if (x, y) in distances:
                distances[(x, y)] = min(distances[(x, y)],
                                        distances[(prev_x, prev_y)] + 1)
            else:
                distances[(x, y)] = distances[(prev_x, prev_y)] + 1
        prev_x, prev_y = x, y
    return max(distances.values()), sum(1 for v in distances.values() if v > 999)

if __name__ == '__main__':
    print('Solution for Part One: {}\nSolution for Part Two: {}'.format(*day_20()))

