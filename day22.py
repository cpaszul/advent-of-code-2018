from enum import Enum, IntEnum
import heapq

DEFAULT_INPUT = 'day22.txt'

class Area(Enum):
    ROCKY = 1
    WET = 2
    NARROW = 3

class Tool(IntEnum):
    NONE = 1
    GEAR = 2
    TORCH = 3

class Region:
    def __init__(self, depth, target_x, target_y):
        self.depth = depth
        self.target_x = target_x
        self.target_y = target_y
        self._erosion = {}

    def erosion(self, x, y):
        if (x, y) not in self._erosion:
            if (x, y) in ((0, 0), (self.target_x, self.target_y)):
                geo = 0
            elif y == 0:
                geo = x * 16807
            elif x == 0:
                geo = y * 48271
            else:
                geo = self.erosion(x - 1, y)[0] * \
                      self.erosion(x, y - 1)[0]
            e = (geo + self.depth) % 20183
            region_type = [Area.ROCKY, Area.WET, Area.NARROW][e % 3]
            self._erosion[(x, y)] = (e, region_type)
        return self._erosion[(x, y)]

    def risk_area(self):
        return sum(self.erosion(x, y)[0] % 3
                   for x in range(self.target_x + 1)
                   for y in range(self.target_y + 1))

    def shortest_path(self):
        h = [(0, 0, 0, Tool.TORCH)]
        fastest = {}
        target = (self.target_x, self.target_y, Tool.TORCH)
        while h:
            time, x, y, tool = heapq.heappop(h)
            if (x, y, tool) in fastest and fastest[(x, y, tool)] <= time:
                continue
            fastest[(x, y, tool)] = time
            if (x, y, tool) == target:
                return time
            adjs = self.adjacents(x, y, tool)
            for adj in adjs:
                if self.can_enter(*adj):
                    newtime = time + (1 if adj[2] == tool else 7)
                    heapq.heappush(h, (newtime, adj[0], adj[1], adj[2]))

    def adjacents(self, x, y, t):
        raw = [(x + 1, y, t), (x - 1, y, t),
               (x, y + 1, t), (x, y - 1, t),
               (x, y, self.change_tool(x, y, t))]
        return [(i, j, t) for i, j, t in raw
                if i >= 0 and j >= 0]

    def can_enter(self, x, y, t):
        if self.erosion(x, y)[1] is Area.ROCKY:
            return t in (Tool.GEAR, Tool.TORCH)
        elif self.erosion(x, y)[1] is Area.WET:
            return t in (Tool.GEAR, Tool.NONE)
        else:
            return t in (Tool.TORCH, Tool.NONE)

    def change_tool(self, x, y, t):
        if self.erosion(x, y)[1] is Area.ROCKY:
            return Tool.GEAR if t is Tool.TORCH else Tool.TORCH
        elif self.erosion(x, y)[1] is Area.WET:
            return Tool.GEAR if t is Tool.NONE else Tool.NONE
        else:
            return Tool.TORCH if t is Tool.NONE else Tool.NONE

def day_22(loc=DEFAULT_INPUT):
    with open(loc) as f:
        depth = int(f.readline().split(' ')[1])
        target_x, target_y = map(int, f.readline().split(' ')[1].split(','))
    region = Region(depth, target_x, target_y)
    return region.risk_area(), region.shortest_path()

if __name__ == '__main__':
    print('Solution for Part One: {}\nSolution for Part Two: {}'.format(*day_22()))

