DEFAULT_INPUT = 'day13.txt'

class Track:
    def __init__(self, grid, remove_carts):
        self.grid = {}
        self.carts = []
        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                if cell in '<>':
                    self.carts.append(Cart(x, y, (1, 0) if cell == '>' else (-1, 0)))
                    self.grid[(x, y)] = '-'
                elif cell in 'v^':
                    self.carts.append(Cart(x, y, (0, 1) if cell == 'v' else (0, -1)))
                    self.grid[(x, y)] = '|'
                elif cell != ' ':
                    self.grid[(x, y)] = cell
        self.remove_carts = remove_carts

    def sort_carts(self):
        self.carts.sort(key=lambda t:t.x)
        self.carts.sort(key=lambda t:t.y)

    def tick(self):
        self.sort_carts()
        for cart in self.carts:
            if cart.exist:
                x, y = cart.advance()
                new_loc = self.grid[(x, y)]
                if self.carts_at_location(x, y) > 1:
                    if self.remove_carts:
                        self.remove_carts_at_location(x, y)
                    else:
                        return (x, y)
                if new_loc == '\\':
                    cart.direction = (cart.direction[1], cart.direction[0])
                elif new_loc == '/':
                    cart.direction = (-1 * cart.direction[1], -1 * cart.direction[0])
                elif new_loc == '+':
                    cart.intersection()
        if self.remove_carts and len(self.existing_carts()) == 1:
            return (self.existing_carts()[0].x, self.existing_carts()[0].y)
        return False

    def carts_at_location(self, x, y):
        return sum(1 for cart in self.carts
                   if cart.x == x and cart.y == y and cart.exist)

    def remove_carts_at_location(self, x, y):
        for cart in self.carts:
            if cart.x == x and cart.y == y:
                cart.exist = False

    def existing_carts(self):
        return [cart for cart in self.carts if cart.exist]

class Cart:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.i = 0
        self.exist = True

    def advance(self):
        self.x += self.direction[0]
        self.y += self.direction[1]
        return self.x, self.y

    def turn_left(self):
        if self.direction[1] == 0:
            self.direction = (-1 * self.direction[1], -1 * self.direction[0])
        else:
            self.direction = (self.direction[1], self.direction[0])

    def turn_right(self):
        if self.direction[1] == 0:
            self.direction = (self.direction[1], self.direction[0])
        else:
            self.direction = (-1 * self.direction[1], -1 * self.direction[0])

    def intersection(self):
        if self.i % 3 == 0:
            self.turn_left()
        elif self.i % 3 == 2:
            self.turn_right()
        self.i += 1
        
            
                    

def part_1(loc=DEFAULT_INPUT):
    with open(loc) as f:
        grid = [line.rstrip('\n') for line in f.readlines()]
    track = Track(grid, False)
    while True:
        has_crash = track.tick()
        if has_crash:
            return has_crash


def part_2(loc=DEFAULT_INPUT):
    with open(loc) as f:
        grid = [line.rstrip('\n') for line in f.readlines()]
    track = Track(grid, True)
    while True:
        last_cart = track.tick()
        if last_cart:
            return last_cart

if __name__ == '__main__':
    print('Solution for Part One:', part_1())
    print('Solution for Part Two:', part_2())
