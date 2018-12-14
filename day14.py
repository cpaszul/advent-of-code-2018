DEFAULT_INPUT = '190221'

def part_1(s=DEFAULT_INPUT):
    scoreboard = '37'
    i = 0
    j = 1
    n = int(s)
    while len(scoreboard) < n + 10:
        i_score = int(scoreboard[i])
        j_score = int(scoreboard[j])
        new_score = str(i_score + j_score)
        scoreboard += new_score
        i += (1 + i_score)
        i %= len(scoreboard)
        j += (1 + j_score)
        j %= len(scoreboard)
    return scoreboard[n:n + 10]

def part_2(s=DEFAULT_INPUT):
    scoreboard = '37'
    i = 0
    j = 1
    while True:
        i_score = int(scoreboard[i])
        j_score = int(scoreboard[j])
        new_score = str(i_score + j_score)
        scoreboard += new_score
        i += (1 + i_score)
        i %= len(scoreboard)
        j += (1 + j_score)
        j %= len(scoreboard)
        if s in scoreboard:
            return scoreboard.index(s)

if __name__ == '__main__':
    print('Solution for Part One:', part_1())
    print('Solution for Part Two:', part_2())
