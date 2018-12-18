from enum import Enum

DEFAULT_INPUT = 'day18.txt'

class Acre(Enum):
    OPEN = 1
    TREES = 2
    LUMBER = 3
    
class CellAuto:
    def __init__(self, lines):
        self.grid = {}
        for y, row in enumerate(lines):
            for x, cell in enumerate(row):
                if cell == '.':
                    self.grid[(x, y)] = Acre.OPEN
                elif cell == '|':
                    self.grid[(x, y)] = Acre.TREES
                else:
                    self.grid[(x, y)] = Acre.LUMBER
        self.time = 0

    def change(self, x, y):
        adj = self.adjacent(x, y)
        if self.grid[(x, y)] is Acre.OPEN:
            if self.count(adj, Acre.TREES) >= 3:
                return Acre.TREES
            else:
                return False
        elif self.grid[(x, y)] is Acre.TREES:
            if self.count(adj, Acre.LUMBER) >= 3:
                return Acre.LUMBER
            else:
                return False
        else:
            if self.count(adj, Acre.TREES) >= 1 and \
               self.count(adj, Acre.LUMBER) >= 1:
                return False
            else:
                return Acre.OPEN

    def adjacent(self, x, y):
        return [(x + i, y + j) for i in range(-1, 2) for j in range(-1, 2)
                if (i != 0 or j != 0) and (x + i, y + j) in self.grid]

    def count(self, points, value):
        return sum(1 for point in points if self.grid[point] is value)

    def tick(self):
        transformations = {}
        for x in range(50):
            for y in range(50):
                value_change = self.change(x, y)
                if value_change:
                    transformations[(x, y)] = value_change
        for k, v in transformations.items():
            self.grid[k] = v
        self.time += 1

    def resource_value(self):
        lumber, trees = 0, 0
        for val in self.grid.values():
            if val is Acre.LUMBER:
                lumber += 1
            elif val is Acre.TREES:
                trees += 1
        return lumber * trees

    def __str__(self):
        s = ''
        for y in range(50):
            for x in range(50):
                cell = self.grid[(x, y)]
                if cell is Acre.OPEN:
                    s += '.'
                elif cell is Acre.TREES:
                    s += '|'
                else:
                    s += '#'
        return s


def part_1(loc=DEFAULT_INPUT):
    with open(loc) as f:
        ca = CellAuto((line.rstrip() for line in f.readlines()))
    for _ in range(10):
        ca.tick()
    return ca.resource_value()

def part_2(loc=DEFAULT_INPUT):
    with open(loc) as f:
        ca = CellAuto((line.rstrip() for line in f.readlines()))
    target = 1000000000
    states = {str(ca): (ca.time, ca.resource_value())}
    while True:
        ca.tick()
        s = str(ca)
        if s in states:
            cycle_start = states[s][0]
            cycle_end = ca.time
            break
        else:
            states[s] = (ca.time, ca.resource_value())
    cycle_len = cycle_end - cycle_start
    time_equivalent = cycle_start + ((target - cycle_start) % cycle_len)
    return [v[1] for v in states.values() if v[0] == time_equivalent][0]
    
if __name__ == '__main__':
    print('Solution for Part One:', part_1())
    print('Solution for Part Two:', part_2())
