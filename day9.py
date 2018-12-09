from collections import Counter, deque

DEFAULT_INPUT = 'day9.txt'

def day_9(loc=DEFAULT_INPUT):
    with open(loc) as f:
        s = f.readline().split(' ')
        num_players = int(s[0])
        end_point_one = int(s[-2])
        end_point_two = end_point_one * 100
    marbles = deque([0])
    current_marble = 1
    current_player = 1
    players = Counter()
    while current_marble <= end_point_two:
        if current_marble % 23 == 0:
            players[current_player] += current_marble
            marbles.rotate(6)
            players[current_player] += marbles.pop()
        elif len(marbles) >= 2:
            marbles.insert(2, current_marble)
            marbles.rotate(-2)
        else:
            marbles.appendleft(1)
        if current_marble == end_point_one:
            part_one = max(players.values())
        current_marble += 1
        current_player += 1
        if current_player > num_players:
            current_player = 1
    return part_one, max(players.values())

def part_2(loc=DEFAULT_INPUT):
    pass

if __name__ == '__main__':
    print('Solution for Part One: {}\nSolution for Part Two: {}'.format(*day_9()))
