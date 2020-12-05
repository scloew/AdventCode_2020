from collections import namedtuple
from operator import mul
from functools import reduce


def fetch_input(file_name):
    with open(r'inputs/' + file_name, 'r') as in_file:
        data = in_file.read()
    return data


def day_1a(target=2020, data=None):
    observed = set()
    if data is None:
        data = (int(i) for i in fetch_input('day_1A.txt').split('\n') if i)
    for i in data:
        if i and target - int(i) in observed:
            return i * (target - i)
        observed.add(i)


def day_1b():
    data = tuple(int(i) for i in fetch_input('day_1A.txt').split('\n') if i)
    for i, v in enumerate(data):
        temp = day_1a(target=2020 - v, data=data[i + 1:])
        if temp:
            return v * temp


def day_2a():
    Entry = namedtuple('Entry', ['min', 'max', 'char', 'password'])
    return day_2_helper(Entry, lambda e: 1 if e.password.count(e.char) in range(int(e.min), int(e.max) + 1) else 0)


def day_2b():
    Entry = namedtuple('Entry', ['index_0', 'index_1', 'char', 'pw'])
    return day_2_helper(Entry, lambda e: (e.pw[int(e.index_0) - 1] == e.char) ^ (e.pw[int(e.index_1) - 1] == e.char))


def day_2_helper(tuple_, valid_pw):
    data = fetch_input('day_2.txt').replace(':', '').replace('-', ' ').split('\n')[:-1]
    return sum(valid_pw(tuple_(*i.split(' '))) for i in data)


def day_3a():
    return day_3_helper(3)


def day_3b():
    slopes = (1, 3, 5, 7)
    return reduce(mul, (day_3_helper(i) for i in slopes), 1) * day_3_helper(1, y_inc=2)


def day_3_helper(x_inc, y_inc=1):
    data = fetch_input('day_3.txt').split('\n')[:-1]
    if not y_inc == 1:
        data = (v for i, v in enumerate(data) if i % y_inc == 0)
    x, ret = 0, 0
    for row in data:
        if row[x % len(row)] == '#':
            ret += 1
        x += x_inc
    return ret


def day_4a():
    fields = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
    data, ret = fetch_input('day_4.txt').split('\n\n'), 0
    for entry in data:
        valid = True
        for field in fields:
            if field not in entry:
                valid = False
                break
        if valid:
            ret += 1
    return ret


def day_4b():
    hgt_helpers = {'cm': lambda e: 150 <= int(e) <= 193,
                   'in': lambda e: 59 <= int(e) <= 76}

    fields = {'byr': lambda e: len(e) == 8 and e[4:].isdigit() and 1920 <= int(e[4:]) <= 2002,
              'iyr': lambda e: len(e) == 8 and e[4:].isdigit() and 2010 <= int(e[4:]) <= 2020,
              'eyr': lambda e: len(e) == 8 and e[4:].isdigit() and 2020 <= int(e[4:]) <= 2030,
              'hgt': lambda e: e[-2:] in {'cm', 'in'} and hgt_helpers[e[-2:]](e[4:-2]),
              'hcl': lambda e: e[4] == '#' and len(e[5:]) == 6 and set(e[5:]).issubset(set('0123456789abcdef')),
              'ecl': lambda e: e[4:] in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'},
              'pid': lambda e: len(e[4:]) == 9 and e[4:].isdigit()}

    data, ret = fetch_input('day_4.txt').split('\n\n'), 0
    for entry in data:
        for field, check in fields.items():
            temp = entry.replace('\n', ' ').split(' ')
            valid = False
            for word in temp:
                if field in word and check(word):
                    valid = True
                    break
            if not valid:
                break
        if valid:
            ret += 1
    return ret


def day_5a():
    return max(day_5_seat_helper())


def day_5b():
    get_id = lambda r, c: r * 8 + c
    available_seats = {get_id(r, c) for r in range(1, 127) for c in range(8)}
    taken_seats = set(day_5_seat_helper())
    empty_seats = available_seats - taken_seats
    for i in empty_seats:
        if i in range(13, 1018) and i-1 in taken_seats and i+1 in taken_seats:
            return i


def day_5_seat_helper():
    data = fetch_input('day_5.txt').split('\n')[:-1]
    args_r, args_c = ('B', 'F'), ('R', 'L')
    for entry in data:
        row, column = entry[:7], entry[7:]
        yield day_5_helper(row, *args_r) * 8 + day_5_helper(column, *args_c)


def day_5_helper(string, one, zero):
    temp = string.replace(one, '1').replace(zero, '0')
    return int(temp, 2)


if __name__ == '__main__':
    print('1A := ', day_1a())
    print('1B := ', day_1b())
    print('2A := ', day_2a())
    print('2B := ', day_2b())
    print('3A := ', day_3a())
    print('3B := ', day_3b())
    print('4A := ', day_4a())
    print('4B := ', day_4b())
    print('5A := ', day_5a())
    print('5B := ', day_5b())
