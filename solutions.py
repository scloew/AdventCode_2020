from collections import namedtuple
from operator import mul
from functools import reduce
from collections import Counter, OrderedDict


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
    graph = day_7_build_graph_b()
    # return graph
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


def day_7_build_graph_b():
    Edge = namedtuple('Edge', ['weight', 'vertex'])
    data = fetch_input('day_7.txt').replace('.', '')
    data = data.replace(' no other bags', '') .replace('bags', 'bag').split('\n')[:-1]
    graph = {}
    for entry in data:
        if entry.count('bag') == 1:
            continue
        temp = entry.split(' contain ')
        bag, content = temp[0], temp[1].split(', ')
        temp_content = graph.get(bag, [])
        for item in content:
            temp = item.split(' ')
            wght, temp_bag = temp[0], ' '.join(temp[1:])
            temp_content.append(Edge(int(wght), bag))
        graph[bag] = temp_content
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


def bfs_7b(graph, start_node='shiny gold bag'):
    count = 1
    graph, start_node = 'shiny gold bag'
    new_nodes, observed = graph[start_node], set()
    # need to make this recursive to handle wght * count of bag
    while new_nodes:
        temp_nodes = []
        for node in new_nodes:
            observed.add(node)
            # if node not in graph.keys():
            #     continue
            for wght, vertex in graph[node]:
                count += wght * bfs_7b(graph, vertex)
                if vertex not in observed:
                    temp_nodes.append(vertex)
        new_nodes = temp_nodes
    return count


def day_8a():
    return day_8_helper()[0]


def day_8b():
    data = fetch_input('day_8.txt').split('\n')[:-1]
    jmps = [index for index, entry in enumerate(data) if 'jmp' in entry and '-' in entry]
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


def day_9a():
    data = [int(i) for i in fetch_input('day_9.txt').split('\n')[:-1]]
    index, offset, previous = 25, 25, set(data[:25])
    while index < len(data):
        current = data[index]
        if not day_1a(target=current, data=data):
            return current
        previous.remove(data[index-offset])
        previous.add(current)
        index += 1


def day_9b():
    data = [int(i) for i in fetch_input('day_9.txt').split('\n')[:-1]]
    target = day_9a()
    start, stop = 0, 1
    temp = sum(data[:2])
    while stop < len(data):
        if temp == target:
            stop += 1
            return max(data[start:stop]) + min(data[start:stop])
        elif target < temp:
            temp -= data[start]
            start += 1
            continue
        stop += 1
        temp += data[stop]


def day_10a():
    data = sorted((int(i) for i in fetch_input('day_10.txt').split('\n')[:-1]))
    counter = Counter((data[i+1]-v for i, v in enumerate(data) if i < len(data)-1))
    return (counter[1]+1) * (counter[3]+1)


def day_10b():
    data = sorted((int(i) for i in fetch_input('day_10.txt').split('\n')[:-1]))
    data = [0] + data + [data[-1] + 3]
    graph = OrderedDict([(x, {y for y in range(x+1, x+4) if y in data}) for x in data])
    return day_10b_helper(graph, 0)


def day_10b_helper(graph, v, map_=None):
    map_ = {} if map_ is None else map_
    if v in map_:
        return map_[v]
    elif graph[v]:
        map_[v] = sum(day_10b_helper(graph, x, map_) for x in graph[v])
        return map_[v]
    else:
        return 1


def day_11a():
    from copy import copy
    data = [list(i) for i in fetch_input('day_11.txt').split('\n')[:-1]]
    altered = True
    count = 0
    while altered:
        count += 1
        print(count)
        print('\n'.join([''.join(i) for i in data]))
        print('\n=======\n')
        new_data = copy(data)
        altered = False
        for row_num, row in enumerate(data):
            for seat_num, seat in enumerate(row):
                # TODO currently modifying data which results in some seats not being vacated when they should be
                altered |= day_11a_helper(seat, row_num, seat_num, data, new_data)
        data = new_data
        if 7 < count:
            break
    return 'neat'


def day_11a_helper(seat, row, col, data, new_data):
    # from copy import copy
    # temp = copy(data)
    empty, occupied = 'L', '#'
    directions = ((y, x) for x in range(-1, 2) for y in range(-1, 2) if not x == y == 0)
    if seat == empty:
        new_data[row][col] = occupied
        return True
    elif seat == occupied:
        count = 0
        for y, x in directions:
            try:
                if data[row+y][col+x] == occupied and 0 <= min(row+y, col+x):
                    count += 1
            except IndexError:
                pass
        if 4 <= count:
            new_data[row][col] = empty
            return True
    # data = temp
    return False


def day_12a():
    facing_index = 0
    shifters, directions = {'R': 1, 'L': -1}, ['E', 'S', 'W', 'N']
    mags = dict(zip(directions, [0 for _ in range(5)]))
    data = ((i[0], int(i[1:])) for i in fetch_input('day_12.txt').split('\n')[:-1])
    for dir_, val in data:
        if dir_ in ('R', 'L'):
            facing_index = (facing_index+(val//90) * shifters[dir_]) % len(directions)
        elif dir_ == 'F':
            mags[directions[facing_index]] += val
        else:
            mags[dir_] += val
    return abs(mags['E'] - mags['W']) + abs(mags['N']-mags['S'])


# not working yet
def day_12b():
    dirs = {'N': 1, 'E': 1, 'S': -1, 'W': -1}
    ship_x, ship_y = 0, 0
    wp_x, wp_y = 10, 1
    for dir_, val in ((i[0], int(i[1:])) for i in fetch_input('day_12b_test.txt').split('\n')[:-1]):
        if dir_ in ('R', 'L'):
            for _ in range(val//90):
                if dir_ == 'R':
                    wp_x, wp_y = wp_y, -wp_x
                else:
                    wp_x, wp_y = -wp_y, wp_x
        elif dir_ == 'F':
            ship_x += val * wp_x
            ship_y += val * wp_y
        elif dir_ in ('N', 'S'):
            wp_y += val * dirs[dir_]
        else:
            wp_x = val * dirs[dir_]
    return abs(ship_x) + abs(ship_y)


def day_22a():
    data = fetch_input('day22.txt').split('\n\n')
    p1, p2 = [int(i) for i in data[0].split('\n')[1:]], [int(i) for i in data[1].split('\n')[1:-1]]
    while p1 and p2:
        c1, c2 = p1.pop(0), p2.pop(0)
        if c1 > c2:
            p1.append(c1)
            p1.append(c2)
        else:
            p2.append(c2)
            p2.append(c1)
    winner = p1 if p1 else p2
    total = 0
    for i, v in enumerate(winner[::-1]):
        total += (i+1) * v
    return total


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
    print('7B := ', day_7b())
    print('8A := ', day_8a())
    print('8B := ', day_8b())
    print('9A := ', day_9a())
    print('9B := ', day_9b())
    print('10A := ', day_10a())
    print('10B := ', day_10b())
    print('11A := ', day_11a())
    print('12A := ', day_12a())
    print('12B := ', day_12b())
    print('22A := ', day_22a())
