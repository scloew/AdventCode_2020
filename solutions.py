from collections import namedtuple


def fetch_input(file_name):
    with open(r'inputs/'+file_name, 'r') as in_file:
        data = in_file.read()
    return data


def day_1a(target=2020, data=None):
    observed = set()
    if data is None:
        data = (int(i) for i in fetch_input('day_1A.txt').split('\n') if i)
    for i in data:
        if i and target-int(i) in observed:
            return i * (target - i)
        observed.add(i)


def day_1b():
    data = tuple(int(i) for i in fetch_input('day_1A.txt').split('\n') if i)
    for i, v in enumerate(data):
        temp = day_1a(target=2020-v, data=data[i+1:])
        if temp:
            return v * temp


def day_2a():
    Entry = namedtuple('Entry', ['min', 'max', 'char', 'password'])
    return day_2_helper(Entry, lambda e: 1 if e.password.count(e.char) in range(int(e.min), int(e.max) + 1) else 0)


def day_2b():
    Entry = namedtuple('Entry', ['index_0', 'index_1', 'char', 'pw'])
    return day_2_helper(Entry, lambda e: (e.pw[int(e.index_0)-1] == e.char) ^ (e.pw[int(e.index_1)-1] == e.char))


def day_2_helper(tuple_, valid_pw):
    data = fetch_input('day_1B.txt').replace(':', '').replace('-', ' ').split('\n')[:-1]
    return sum(valid_pw(tuple_(*i.split(' '))) for i in data)


if __name__ == '__main__':
    print('1A := ', day_1a())
    print('1B := ',day_1b())
    print('2A := ', day_2a())
    print('2B := ', day_2b())
