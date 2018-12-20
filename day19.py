DEFAULT_INPUT = 'day19.txt'

def addr(regs, a, b, c):
    res = regs[::]
    res[c] = res[a] + res[b]
    return res

def addi(regs, a, b, c):
    res = regs[::]
    res[c] = res[a] + b
    return res

def mulr(regs, a, b, c):
    res = regs[::]
    res[c] = res[a] * res[b]
    return res

def muli(regs, a, b, c):
    res = regs[::]
    res[c] = res[a] * b
    return res

def banr(regs, a, b, c):
    res = regs[::]
    res[c] = res[a] & res[b]
    return res

def bani(regs, a, b, c):
    res = regs[::]
    res[c] = res[a] & b
    return res

def borr(regs, a, b, c):
    res = regs[::]
    res[c] = res[a] | res[b]
    return res

def bori(regs, a, b, c):
    res = regs[::]
    res[c] = res[a] | b
    return res

def setr(regs, a, b, c):
    res = regs[::]
    res[c] = res[a]
    return res
    
def seti(regs, a, b, c):
    res = regs[::]
    res[c] = a
    return res

def gtir(regs, a, b, c):
    res = regs[::]
    res[c] = 1 if a > res[b] else 0
    return res

def gtri(regs, a, b, c):
    res = regs[::]
    res[c] = 1 if res[a] > b else 0
    return res

def gtrr(regs, a, b, c):
    res = regs[::]
    res[c] = 1 if res[a] > res[b] else 0
    return res

def eqir(regs, a, b, c):
    res = regs[::]
    res[c] = 1 if a == res[b] else 0
    return res

def eqri(regs, a, b, c):
    res = regs[::]
    res[c] = 1 if res[a] == b else 0
    return res

def eqrr(regs, a, b, c):
    res = regs[::]
    res[c] = 1 if res[a] == res[b] else 0
    return res

FUNC_TABLE = {'addi': addi, 'addr': addr, 'muli': muli, 'mulr': mulr,
              'bani': bani, 'banr': banr, 'bori': bori, 'borr': borr,
              'seti': seti, 'setr': setr, 'gtir': gtir, 'gtri': gtri,
              'gtrr': gtrr, 'eqir': eqir, 'eqri': eqri, 'eqrr': eqrr}

def part_1(loc=DEFAULT_INPUT):
    regs = [0, 0, 0, 0, 0, 0]
    i = 0
    lines = []
    with open(loc) as f:
        ip_reg = int(f.readline().split(' ')[1])
        for line in f.readlines():
            f, a, b, c = line.rstrip().split(' ')
            lines.append((FUNC_TABLE[f], int(a), int(b), int(c)))
    while 0 <= i < len(lines):
        regs[ip_reg] = i
        f, a, b, c = lines[i]
        regs = f(regs, a, b, c)
        i = regs[ip_reg]
        i += 1
    return regs[0]

def part_2(loc=DEFAULT_INPUT):
    regs = [1, 0, 0, 0, 0, 0]
    i = 0
    lines = []
    with open(loc) as f:
        ip_reg = int(f.readline().split(' ')[1])
        for line in f.readlines():
            f, a, b, c = line.rstrip().split(' ')
            lines.append((FUNC_TABLE[f], int(a), int(b), int(c)))
    while 0 <= i < len(lines):
        regs[ip_reg] = i
        f, a, b, c = lines[i]
        regs = f(regs, a, b, c)
        i = regs[ip_reg]
        i += 1
    return regs[0]

if __name__ == '__main__':
    print('Solution for Part One:', part_1())
    print('Solution for Part Two:', part_2())
