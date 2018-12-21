from collections import defaultdict

DEFAULT_INPUT = 'day17.txt'

class Reservoir:
    def __init__(self, lines):
        self.grid = defaultdict(lambda: '.')
        for line in lines:
            a, b = line.rstrip().split(', ')
            if a[0] == 'x':
                x_val = int(a.split('=')[1])
                y_min = int(b.split('=')[1].split('..')[0])
                y_max = int(b.split('=')[1].split('..')[1])
                for y_val in range(y_min, y_max + 1):
                    self.grid[(x_val, y_val)] = '#'
            else:
                y_val = int(a.split('=')[1])
                x_min = int(b.split('=')[1].split('..')[0])
                x_max = int(b.split('=')[1].split('..')[1])
                for x_val in range(x_min, x_max + 1):
                    self.grid[(x_val, y_val)] = '#'
        self.grid[(500, 0)] = '+'
        self.min_y = min((k for k,v in self.grid.items() if v == '#'),
                         key=lambda p:p[1])[1]
        self.max_y = max((k for k,v in self.grid.items() if v == '#'),
                         key=lambda p:p[1])[1]

    def display(self):
        max_x = max((k for k,v in self.grid.items() if v != '.'),
                    key=lambda p:p[0])[0]
        min_x = min((k for k,v in self.grid.items() if v != '.'),
                    key=lambda p:p[0])[0]
        rows = []
        for y in range(0, self.max_y + 1):
            row = ''
            for x in range(min_x, max_x + 1):
                row += self.grid[(x, y)]
            rows.append(row)
        print('\n'.join(rows))

    def tick(self):
        if self.grid[(500, 1)] in '?W':
            return True
        self.move_water((500, 1))
        return False

    def move_water(self, point, direction='D'):
        x, y = point
        while True:
            down = (x, y + 1)
            right = (x + 1, y)
            left = (x - 1, y)
            if y == self.max_y or self.grid[down] == '?':
                self.grid[(x, y)] = '?'
                return True
            elif self.grid[down] in '#W':
                if self.grid[right] == '.' and direction != 'L':
                    self.move_water(right, 'R')
                elif self.grid[left] == '.' and direction != 'R':
                    self.move_water(left, 'L')
                if direction == 'R':
                    if self.grid[right] == '?':
                        self.grid[(x, y)] = '?'
                    elif self.grid[right] in 'W#':
                        self.grid[(x, y)] = 'W'
                elif direction == 'L':
                    if self.grid[left] == '?':
                        self.grid[(x, y)] = '?'
                    elif self.grid[left] in 'W#':
                        self.grid[(x, y)] = 'W'
                else:
                    if (self.grid[left] == '?' and self.grid[right] != '.') or \
                       (self.grid[right] == '?' and self.grid[left] != '.'):
                        self.grid[(x, y)] = '?'
                        if self.grid[right] == 'W':
                            self.set_to_flowing(right)
                        if self.grid[left] == 'W':
                            self.set_to_flowing(left)
                    elif self.grid[left] != '.' and self.grid[right] != '.':
                        self.grid[(x, y)] = 'W'
                return True 
            else:
                y += 1
                direction = 'D'

    def set_to_flowing(self, point):
        self.grid[point] = '?'
        x, y = point
        if self.grid[(x + 1, y)] == 'W':
            self.set_to_flowing((x + 1, y))
        if self.grid[(x - 1, y)] == 'W':
            self.set_to_flowing((x - 1, y))

    def water_tiles(self):
        return (sum(1 for k, v in self.grid.items()
                    if v in '?W' and self.min_y <= k[1] <= self.max_y),
                sum(1 for k, v in self.grid.items()
                    if v == 'W' and self.min_y <= k[1] <= self.max_y))


def day_17(loc=DEFAULT_INPUT):
    with open(loc) as f:
        res = Reservoir(f.readlines())
    finished_flow = False
    while not finished_flow:
        finished_flow = res.tick()
    return res.water_tiles()

if __name__ == '__main__':
    print('Solution for Part One: {}\nSolution for Part Two: {}'.format(*day_17()))
   
