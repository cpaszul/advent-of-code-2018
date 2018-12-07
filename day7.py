from collections import defaultdict
from string import ascii_uppercase

DEFAULT_INPUT = 'day7.txt'

class Worker:
    def __init__(self):
        self.time_remaining = -1
        self.current_char = None
        self.has_char = False

    def time_needed(self, char):
        return 61 + ascii_uppercase.index(char)

    def advance_time(self):
        if self.current_char:
            self.time_remaining -= 1
            if self.time_remaining == 0:
                self.has_char = False
                c = self.current_char
                self.current_char = None
                return c
            else:
                return None
        else:
            return None

    def add_char(self, char):
        self.current_char = char
        self.time_remaining = self.time_needed(char)
        self.has_char = True

def part_1(loc=DEFAULT_INPUT):
    graph = defaultdict(set)
    chars = set()
    with open(loc) as f:
        for line in f.readlines():
            s = line.split(' ')
            start = s[1]
            end = s[7]
            graph[end].add(start)
            chars.add(start)
            chars.add(end)
    queue = [char for char in chars if not graph[char]]
    queue.sort()
    path = ''
    while queue:
        current = queue.pop(0)
        path += current
        new_queue = []
        for char in chars:
            if char not in path:
                if all(ch in path for ch in graph[char]):
                    new_queue.append(char)
        new_queue.sort()
        queue = new_queue
    return path      
            
def part_2(loc=DEFAULT_INPUT):
    graph = defaultdict(set)
    chars = set()
    with open(loc) as f:
        for line in f.readlines():
            s = line.split(' ')
            start = s[1]
            end = s[7]
            graph[end].add(start)
            chars.add(start)
            chars.add(end)
    path = ''
    t = -1
    workers = [Worker() for _ in range(5)]
    in_workers = set()
    while len(path) != len(chars):
        for w in workers:
            c = w.advance_time()
            if c:
                path += c
                in_workers.remove(c)
        queue = []
        for char in chars:
            if char not in path:
                if all(ch in path for ch in graph[char]) and \
                   char not in in_workers:
                    queue.append(char)
        queue.sort()
        for w in workers:
            if queue and not w.has_char:
                c = queue.pop(0)
                in_workers.add(c)
                w.add_char(c)
        t += 1
    return t
        
if __name__ == '__main__':
    print('Solution for Part One:', part_1())
    print('Solution for Part Two:', part_2())
