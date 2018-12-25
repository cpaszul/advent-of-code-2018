from collections import defaultdict, deque

DEFAULT_INPUT = 'day25.txt'

def day_25(loc=DEFAULT_INPUT):
    graph = defaultdict(set)
    points = []
    with open(loc) as f:
        for line in f.readlines():
            points.append(tuple(map(int, line.rstrip().split(','))))
    for i, point in enumerate(points):
        for other in points[i + 1:]:
            if distance(point, other) <= 3:
                graph[point].add(other)
                graph[other].add(point)
    constellations = []
    seen = set()
    for start_point in points:
        if start_point not in seen:
            d = deque([start_point])
            seen.add(start_point)
            cons = [start_point]
            while d:
                node = d.pop()
                for adj_node in graph[node]:
                    if adj_node not in seen:
                        seen.add(adj_node)
                        cons.append(adj_node)
                        d.append(adj_node)
            constellations.append(cons)
    return len(constellations)
            
                

def distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) + \
           abs(p1[2] - p2[2]) + abs(p1[3] - p2[3])
if __name__ == '__main__':
    print('Solution for Part One:', day_25())
