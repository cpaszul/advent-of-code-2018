import datetime
from collections import defaultdict, Counter

DEFAULT_INPUT = 'day4.txt'

def day_4(loc=DEFAULT_INPUT):
    with open(loc) as f:
        raw_lines = [line.rstrip() for line in f.readlines()]
    lines = [line_format(line) for line in raw_lines]
    lines.sort(key=lambda t:t[0])
    sleep_times = defaultdict(lambda:[0, Counter()])
    current_guard = None
    time_sleep = None
    for dt, info in lines:
        if info == 'falls asleep':
            time_sleep = dt
        elif info == 'wakes up':
            time_slept = (dt - time_sleep).seconds // 60
            sleep_times[current_guard][0] += time_slept
            counts = sleep_times[current_guard][1]
            for minute in range(time_sleep.minute, dt.minute):
                counts[minute] += 1
        else:
            current_guard = int(info.split(' ')[1][1:])
    highest_time_asleep = max(sleep_times.items(), key=lambda t:t[1][0])
    highest_counter = highest_time_asleep[1][1]
    highest_minute = max(highest_counter.items(), key=lambda t:t[1])[0]
    part_1 = highest_time_asleep[0] * highest_minute
    most_time_asleep = -1
    most_time_asleep_minute = None
    most_time_asleep_guard = None
    for guard, sleep_tuple in sleep_times.items():
        minute, time_asleep = max(sleep_tuple[1].items(), key=lambda t:t[1])
        if time_asleep > most_time_asleep:
            most_time_asleep = time_asleep
            most_time_asleep_minute = minute
            most_time_asleep_guard = guard
    part_2 = most_time_asleep_guard * most_time_asleep_minute
    return part_1, part_2

def line_format(line):
    dt_str, info = line[1:].split('] ')
    d_str, t_str = dt_str.split(' ')
    y, mn, day = map(int, d_str.split('-'))
    h, m = map(int, t_str.split(':'))
    dt = datetime.datetime(y, mn, day, h, m)
    return dt, info

if __name__ == '__main__':
    print('Solution for Part One: {}\nSolution for Part Two: {}'.format(*day_4()))
