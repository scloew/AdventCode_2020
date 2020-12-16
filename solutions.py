from collections import namedtuple
from operator import mul
from functools import reduce
from collections import Counter


def fetch_input(file_name):
    with open(r'inputs/' + file_name, 'r') as in_file:
        return in_file.read()


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
        if i in range(13, 1018) and i - 1 in taken_seats and i + 1 in taken_seats:
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


def day_6a():
    data = fetch_input('day_6.txt').split('\n\n')
    return sum(len(set(entry.replace('\n', ''))) for entry in data)


def day_6b():
    data = fetch_input('day_6.txt').split('\n\n')
    data = [i.split('\n') for i in data]
    data[-1] = data[-1][:-1]
    total = 0
    for group in data:
        group_size = len(group)
        counts = Counter(''.join(group))
        counts = Counter(counts.values())[group_size]
        total += counts
    return total


def day_7a():
    graph = day_7_build_graph()
    return len(bfs(graph)[0]) - 1


def day_7b():
    graph = day_7_build_graph()
    return bfs(graph)[1]


def day_7_build_graph():
    Edge = namedtuple('Edge', ['weight', 'vertex'])
    data = fetch_input('day_7.txt').replace('.', '')
    data = data.replace(' no other bags', '') .replace('bags', 'bag').split('\n')[:-1]
    graph = {}
    for entry in data:
        if entry.count('bag') == 1:
            continue
        temp = entry.split(' contain ')
        bag, content = temp[0], temp[1].split(', ')
        for item in content:
            temp = item.split(' ')
            wght, temp_bag = temp[0], ' '.join(temp[1:])
            temp_list = graph.get(temp_bag, [])
            temp_list.append(Edge(int(wght), bag))
            graph[temp_bag] = temp_list
    return graph


def bfs(graph, start_node='shiny gold bag'):
    count = 1
    new_nodes, observed = [start_node], set()
    while new_nodes:
        temp_nodes = []
        for node in new_nodes:
            observed.add(node)
            if node not in graph.keys():
                continue
            for wght, vertex in graph[node]:
                count *= wght
                if vertex not in observed:
                    temp_nodes.append(vertex)
        new_nodes = temp_nodes
    return observed, count


def day_8a():
    return day_8_helper()[0]


def day_8b():
    data = fetch_input('day_8.txt').split('\n')[:-1]
    jmps = [index for index, entry in enumerate(data) if 'jmp' in entry]
    for jmp in jmps:
        data[jmp], temp = 'acc 0', data[jmp]
        acc, success = day_8_helper(data)
        if success:
            return acc
        data[jmp] = temp


def day_8_helper(data=None):
    if data is None:
        data = fetch_input('day_8.txt').split('\n')[:-1]
    index, acc = 0, 0
    observed = set()
    while index < len(data):
        if index in observed:
            return acc, False
        observed.add(index)
        cmd, val = data[index].split(' ')
        if cmd == 'nop':
            index += 1
        elif cmd == 'acc':
            acc += int(val)
            index += 1
        elif cmd == 'jmp':
            index += int(val)
    return acc, True


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
    print('6A := ', day_6a())
    print('6B := ', day_6b())
    print('7A := ', day_7a())
    # print('7B := ', day_7b())
    print('8A := ', day_8a())
    print('8B := ', day_8b())
