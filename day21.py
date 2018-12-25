DEFAULT_INPUT = 'day21.txt'

def seti(regs, a, b, c):
    regs[c] = a

def bani(regs, a, b, c):
    regs[c] = regs[a] & b

def eqri(regs, a, b, c):
    regs[c] = 1 if regs[a] == b else 0

def addr(regs, a, b, c):
    regs[c] = regs[a] + regs[b]

def bori(regs, a, b, c):
    regs[c] = regs[a] | b

def muli(regs, a, b, c):
    regs[c] = regs[a] * b

def gtir(regs, a, b, c):
    regs[c] = 1 if a > regs[b] else 0

def addi(regs, a, b, c):
    regs[c] = regs[a] + b

def gtrr(regs, a, b, c):
    regs[c] = 1 if regs[a] > regs[b] else 0

def setr(regs, a, b, c):
    regs[c] = regs[a]

def eqrr(regs, a, b, c):
    regs[c] = 1 if regs[a] == regs[b] else 0

FUNC_TABLE = {'seti': seti, 'bani': bani, 'eqri': eqri, 'addr': addr,
              'bori': bori, 'muli': muli, 'gtir': gtir, 'addi': addi,
              'gtrr': gtrr, 'setr': setr, 'eqrr': eqrr}

def day_21(loc=DEFAULT_INPUT):
    regs = [0, 0, 0, 0, 0, 0]
    lines = []
    first = None
    prev = None
    seen = set()
    with open(loc) as f:
        f.readline()
        for line in f.readlines():
            f, a, b, c = line.rstrip().split(' ')
            lines.append((FUNC_TABLE[f], int(a), int(b), int(c)))
    while True:
        if regs[5] == 28:
            if first is None:
                first = regs[3]
            if regs[3] in seen:
                return first, prev
            seen.add(regs[3])
            prev = regs[3]
        f, a, b, c = lines[regs[5]]
        f(regs, a, b, c)
        regs[5] += 1

        
if __name__ == '__main__':
    print('Solution for Part One: {}\nSolution for Part Two: {}'.format(*day_21()))
