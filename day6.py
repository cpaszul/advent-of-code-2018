from collections import Counter

DEFAULT_INPUT = 'day6.txt'

def part_1(loc=DEFAULT_INPUT):
    with open(loc) as f:
        coords = [tuple(map(int, line.rstrip().split(', ')))
                  for line in f.readlines()]
    min_x = min(coords, key=lambda c:c[0])[0]
    min_y = min(coords, key=lambda c:c[1])[1]
    max_x = max(coords, key=lambda c:c[0])[0]
    max_y = max(coords, key=lambda c:c[1])[1]
    count = Counter()
    invalid = set([-1])
    i = 0
    points = []
    for c in coords:
        points.append((i, c))
        i += 1
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            p = x, y
            closest = closest_point(p, points)
            count[closest] += 1
            if x in (min_x, max_x) or y in (min_y, max_y):
                invalid.add(closest)
    valid_count = {k:v for k, v in count.items() if k not in invalid}
    return max(valid_count.values())
    
def distance(pa, pb):
    return abs(pa[0] - pb[0]) + abs(pa[1] - pb[1])

def closest_point(p, points):
    closest = -1
    closest_dist = 10**12
    for point in points:
        dist = distance(p, point[1])
        if dist < closest_dist:
            closest_dist = dist
            closest = point[0]
        elif dist == closest_dist:
            closest = -1
    return closest
            
def part_2(loc=DEFAULT_INPUT):
    with open(loc) as f:
        points = [tuple(map(int, line.rstrip().split(', ')))
                  for line in f.readlines()]
    p0 = points[0]
    count = 0
    for i in range(10001):
        for j in range(10001 - i):
            x, y = p0
            coords = set()
            coords.add((x + i, y + j))
            coords.add((x - i, y + j))
            coords.add((x + i, y - j))
            coords.add((x - i, y - j))
            for c in coords:
                if valid_point(c, points):
                    count += 1
    return count

def valid_point(p, points, limit=10000):
    current = 0
    for point in points:
        current += distance(p, point)
        if current >= limit:
            return False
    return True
                
        
if __name__ == '__main__':
    print('Solution for Part One:', part_1())
    print('Solution for Part Two:', part_2())
