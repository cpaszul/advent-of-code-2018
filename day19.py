import math

DEFAULT_INPUT = 'day19.txt'

def addr(regs, a, b, c):
    regs[c] = regs[a] + regs[b]

def addi(regs, a, b, c):
    regs[c] = regs[a] + b

def mulr(regs, a, b, c):
    regs[c] = regs[a] * regs[b]

def muli(regs, a, b, c):
    regs[c] = regs[a] * b

def banr(regs, a, b, c):
    regs[c] = regs[a] & regs[b]

def bani(regs, a, b, c):
    regs[c] = regs[a] & b

def borr(regs, a, b, c):
    regs[c] = regs[a] | regs[b]

def bori(regs, a, b, c):
    regs[c] = regs[a] | b

def setr(regs, a, b, c):
    regs[c] = regs[a]
    
def seti(regs, a, b, c):
    regs[c] = a

def gtir(regs, a, b, c):
    regs[c] = 1 if a > regs[b] else 0

def gtri(regs, a, b, c):
    regs[c] = 1 if regs[a] > b else 0

def gtrr(regs, a, b, c):
    regs[c] = 1 if regs[a] > regs[b] else 0

def eqir(regs, a, b, c):
    regs[c] = 1 if a == regs[b] else 0

def eqri(regs, a, b, c):
    regs[c] = 1 if regs[a] == b else 0

def eqrr(regs, a, b, c):
    regs[c] = 1 if regs[a] == regs[b] else 0

FUNC_TABLE = {'addi': addi, 'addr': addr, 'muli': muli, 'mulr': mulr,
              'bani': bani, 'banr': banr, 'bori': bori, 'borr': borr,
              'seti': seti, 'setr': setr, 'gtir': gtir, 'gtri': gtri,
              'gtrr': gtrr, 'eqir': eqir, 'eqri': eqri, 'eqrr': eqrr}

def day_19(loc=DEFAULT_INPUT):
    lines = []
    with open(loc) as f:
        ip_reg = int(f.readline().split(' ')[1])
        for line in f.readlines():
            f, a, b, c = line.rstrip().split(' ')
            lines.append((FUNC_TABLE[f], int(a), int(b), int(c)))
    regs = [0, 0, 0, 0, 0, 0]
    while 0 <= regs[ip_reg] < len(lines):
        f, a, b, c = lines[regs[ip_reg]]
        if regs[ip_reg] == 3:
            part_one = sum_of_factors(regs[1])
            break
        f(regs, a, b, c)
        regs[ip_reg] += 1
    regs = [1, 0, 0, 0, 0, 0]
    while 0 <= regs[ip_reg] < len(lines):
        f, a, b, c = lines[regs[ip_reg]]
        if regs[ip_reg] == 3:
            part_two = sum_of_factors(regs[1])
            return part_one, part_two
        f(regs, a, b, c)
        regs[ip_reg] += 1

def sum_of_factors(n):
    s = 0
    for i in range(1, math.floor(math.sqrt(n))):
        if n % i == 0:
            s += i
            if i**2 != n:
                s += (n // i)
    return s

if __name__ == '__main__':
    print('Solution for Part One: {}\nSolution for Part Two: {}'.format(*day_19()))
   
