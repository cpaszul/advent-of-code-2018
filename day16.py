from collections import defaultdict

DEFAULT_INPUT = 'day16.txt'

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

OPCODES = [addr, addi, mulr, muli,
           banr, bani, borr, bori,
           setr, seti,
           gtir, gtri, gtrr,
           eqir, eqri, eqrr]

def day_16(loc=DEFAULT_INPUT):
    lines = ''
    with open(loc) as f:
        for line in f.readlines():
            lines += line
    lines, program = lines.split('\n\n\n\n')
    program = program.split('\n')
    examples = lines.split('\n\n')
    part_1 = 0
    opcodes = defaultdict(lambda:set(OPCODES))
    for example in examples:
        before, inputs, after = example.split('\n')
        before = list(map(int, before.split('[')[1][:-1].split(', ')))
        after = list(map(int, after.split('[')[1][:-1].split(', ')))
        code = int(inputs.split(' ')[0])
        values = list(map(int, inputs.split(' ')[1:]))
        potential_ops = set([op for op in OPCODES
                             if op(before, *values) == after])
        if len(potential_ops) > 2:
            part_1 += 1
        opcodes[code] &= potential_ops
    actual_ops = {}
    unsolved = set(OPCODES)
    while len(actual_ops) < len(opcodes):
        for code in opcodes:
            possible = opcodes[code] & unsolved
            if len(possible) == 1:
                actual = possible.pop()
                actual_ops[code] = actual
                unsolved.remove(actual)
    registers = [0, 0, 0, 0]
    for line in program:
        code = int(line.split(' ')[0])
        values = list(map(int, line.split(' ')[1:]))
        registers = actual_ops[code](registers, *values)
    return part_1, registers[0]

if __name__ == '__main__':
    print('Solution for Part One: {}\nSolution for Part Two: {}'.format(*day_16()))
   
