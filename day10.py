import re

DEFAULT_INPUT = 'day10.txt'

class Point:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.time = 0
        self.vx = vx
        self.vy = vy

    def advance(self, n=1):
        for _ in range(n):
            self.x += self.vx
            self.y += self.vy
            self.time += 1

    def reverse(self, n=1):
        for _ in range(n):
            self.x -= self.vx
            self.y -= self.vy
            self.time -= 1

    def set_to_time(self, n):
        if n > self.time:
            self.advance(n - self.time)
        elif n < self.time:
            self.reverse(self.time - n)

def day_10(loc=DEFAULT_INPUT):
    r = re.compile(r'position=< ?(-?\d+), +(-?\d+)> velocity=< ?(-?\d+), +(-?\d+)>')
    points = []
    with open(loc) as f:
        for line in f.readlines():
            line = line.rstrip()
            m = r.match(line)
            x = int(m.group(1))
            y = int(m.group(2))
            vx = int(m.group(3))
            vy = int(m.group(4))
            points.append(Point(x, y, vx, vy))
    area = total_area(points)
    t = 0
    while True:
        for point in points:
            point.advance()
        new_area = total_area(points)
        if new_area > area:
            closest_at = t
            break
        else:
            area = new_area
            t += 1
    draw(points, t)
    return t

def total_area(points):
    min_x = min(points, key=lambda p:p.x).x
    min_y = min(points, key=lambda p:p.y).y
    max_x = max(points, key=lambda p:p.x).x
    max_y = max(points, key=lambda p:p.y).y
    return (max_x - min_x + 1) * (max_y - min_y + 1)

def draw(points, t=None):
    if t:
        for point in points:
            point.set_to_time(t)
    min_x = min(points, key=lambda p:p.x).x
    min_y = min(points, key=lambda p:p.y).y
    max_x = max(points, key=lambda p:p.x).x
    max_y = max(points, key=lambda p:p.y).y
    grid = []
    width = max_x - min_x + 1
    height = max_y - min_y + 1
    for _ in range(height):
        row = ['.' for _ in range(width)]
        grid.append(row)
    for point in points:
        mod_x = point.x - min_x
        mod_y = point.y - min_y
        grid[mod_y][mod_x] = '#'
    print('\n'.join(''.join(row) for row in grid))
    
if __name__ == '__main__':
    print('Solution for Part Two:', day_10())
