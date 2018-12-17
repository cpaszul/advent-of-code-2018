from collections import deque

DEFAULT_INPUT = 'day15.txt'

class ElfDeath(Exception):
    pass

class Combat:
    def __init__(self, grid, elf_damage=3, break_on_elf_death=False):
        self.break_on_elf_death = break_on_elf_death
        self.turn = 0
        self.elves = []
        self.goblins = []
        self.tiles = set()
        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                if cell == 'E':
                    self.elves.append(Unit('E', x, y, elf_damage))
                    self.tiles.add((x, y))
                elif cell == 'G':
                    self.goblins.append(Unit('G', x, y))
                    self.tiles.add((x, y))
                elif cell == '.':
                    self.tiles.add((x, y))

    def resolved(self):
        living_elves = [e for e in self.elves if e.is_alive]
        living_goblins = [g for g in self.goblins if g.is_alive]
        return living_elves == [] or living_goblins == []
            
    def trim(self):
        self.elves = [e for e in self.elves if e.is_alive]
        self.goblins = [g for g in self.goblins if g.is_alive]

    def unit_at_point(self, x, y):
        for u in self.elves + self.goblins:
            if u.is_alive and u.x == x and u.y == y:
                return u
        return ''

    def display(self):
        max_x = max(self.tiles, key=lambda p:p[0])[0]
        max_y = max(self.tiles, key=lambda p:p[1])[1]
        rows = []
        for y in range(max_y + 1):
            row = ''
            for x in range(max_x + 1):
                u = self.unit_at_point(x, y)
                if u:
                    row += u.name
                else:
                    row += '.' if (x, y) in self.tiles else '#'
            rows.append(row)
        print('\n'.join(rows))

    def tick(self):
        units = self.elves + self.goblins
        units.sort(key=lambda u:u.x)
        units.sort(key=lambda u:u.y)
        for unit in units:
            if unit.is_alive:
                if self.resolved():
                    return True
                targets = self.goblins if unit.name == 'E' else self.elves
                adjs = set()
                for t in targets:
                    adjs.update(t.adjacents())
                valid_adjs = [adj for adj in adjs if adj in self.tiles]
                if (unit.x, unit.y) not in valid_adjs:
                    self.move_unit(unit, valid_adjs)
                valid_targets = [self.unit_at_point(*adj)
                                 for adj in unit.adjacents()
                                 if self.unit_at_point(*adj) and \
                                 self.unit_at_point(*adj).name != unit.name and \
                                 self.unit_at_point(*adj).is_alive]
                if valid_targets:
                    valid_targets.sort(key=lambda u:u.x)
                    valid_targets.sort(key=lambda u:u.y)
                    valid_targets.sort(key=lambda u:u.health)
                    t = valid_targets[0]
                    unit.attack(t)
                    if not t.is_alive and t.name == 'E' and self.break_on_elf_death:
                        raise ElfDeath
        self.turn += 1
        self.trim()
                

    def move_unit(self, unit, target_spaces):
        target_spaces = [(x, y) for x, y in target_spaces
                         if not self.unit_at_point(x, y)]
        unit_adjs = [adj for adj in unit.adjacents()
                     if adj in self.tiles and not self.unit_at_point(*adj)]
        paths = []
        for adj in unit_adjs:
            endpoint, distance = self.move_from_point(adj, target_spaces)
            if distance:
                paths.append((distance, endpoint, adj))
        if paths:
            paths.sort(key=lambda t:t[2][0])
            paths.sort(key=lambda t:t[2][1])
            paths.sort(key=lambda t:t[1][0])
            paths.sort(key=lambda t:t[1][1])
            paths.sort(key=lambda t:t[0])
            move = paths[0][2]
            unit.x = move[0]
            unit.y = move[1]

    def move_from_point(self, start, ends):
        if start in ends:
            return (start, 1)
        paths = []
        queue = deque([(start, 1)])
        min_distance = 10**9
        seen = set([start])
        while queue:
            node, distance = queue.popleft()
            if distance < min_distance:
                x, y = node
                adjs = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
                for adj in adjs:
                    if self.valid_move(*adj) and adj not in seen:
                        path = (adj, distance + 1)
                        seen.add(adj)
                        if adj in ends:
                            paths.append(path)
                        else:
                            queue.append(path)
        if len(paths) == 0:
            return (None, None)
        paths.sort(key=lambda t:t[0][0])
        paths.sort(key=lambda t:t[0][1])
        return paths[0]
                            
                    

    
    def valid_move(self, x, y):
        return (x, y) in self.tiles and not self.unit_at_point(x, y)

    def total_health(self):
        living_units = [u for u in self.elves + self.goblins if u.is_alive]
        return sum(u.health for u in living_units)

class Unit:
    def __init__(self, name, x, y, damage=3):
        self.name = name
        self.x = x
        self.y = y
        self.damage = damage
        self.health = 200
        self.is_alive = True

    def attack(self, other):
        other.health -= self.damage
        if other.health <= 0:
            other.is_alive = False

    def adjacents(self):
        return [(self.x + 1, self.y), (self.x - 1, self.y),
                (self.x, self.y + 1), (self.x, self.y - 1)]

    def __repr__(self):
        return f'{self.name} at {self.x},{self.y}'

def part_1(loc=DEFAULT_INPUT):
    with open(loc) as f:
        combat = Combat(list(line.rstrip() for line in f.readlines()))
    while not combat.resolved():
        combat.tick()
    return combat.turn * combat.total_health()

def part_2(loc=DEFAULT_INPUT):
    with open(loc) as f:
        combat = Combat(list(line.rstrip() for line in f.readlines()))
    damage = 4
    while True:
        with open(loc) as f:
            combat = Combat(list(line.rstrip() for line in f.readlines()), damage, True)
        try:
            while not combat.resolved():
                combat.tick()
            return combat.turn * combat.total_health()
        except ElfDeath:
            damage += 1
    

if __name__ == '__main__':
    print('Solution for Part One:', part_1())
    print('Solution for Part Two:', part_2())
