DEFAULT_INPUT = 2866
from collections import defaultdict

class Grid:
    def __init__(self, serial):
        self.serial = serial
        self.grid = defaultdict(int)
        for x in range(300, 0, -1):
            for y in range(300, 0, -1):
                self.grid[(x, y)] = self.power_level(x, y) + \
                                    self.grid[(x + 1, y)] + \
                                    self.grid[(x, y + 1)] - \
                                    self.grid[(x + 1, y + 1)]

    def power_level(self, x, y):
        rack_id = x + 10
        level = rack_id * y
        level += self.serial
        level *= rack_id
        if level >= 100:
            level = int(str(level)[-3])
        else:
            level = 0
        level -= 5
        return level

    def square_total(self, x, y, n):
        return self.grid[(x, y)] - self.grid[(x + n, y)] - self.grid[(x, y + n)] + self.grid[(x + n, y + n)]

    def maximum_with_size(self, n):
        current_max = -1
        max_point = -1, -1
        limit = 302 - n
        for x in range(1, limit):
            for y in range(1, limit):
                sq = self.square_total(x, y, n)
                if sq > current_max:
                    current_max = sq
                    max_point = x, y
        return max_point[0], max_point[1], current_max

    def maximum(self):
        current_max = -1
        max_point = -1, -1, -1
        for n in range(1, 301):
            m = self.maximum_with_size(n)
            if m[2] > current_max:
                current_max = m[2]
                max_point = m[0], m[1], n
        return max_point
    
    
def day_11(serial=DEFAULT_INPUT):
    g = Grid(serial)
    return g.maximum_with_size(3)[:2], g.maximum()

if __name__ == '__main__':
    print('Solution for Part One: {}\nSolution for Part Two: {}'.format(*day_11()))
