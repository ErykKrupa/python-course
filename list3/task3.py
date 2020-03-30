from functools import reduce


def file_size(file_name):
    # functional syntax, not sure if stream is closed after it
    # return reduce(lambda x, y: x + y, (int(line.split()[-1]) for line in open(file_name).readlines()))
    with open(file_name) as file:
        return reduce(lambda x, y: x + y,
                      (int(line.split()[-1]) for line in file.readlines()))


if __name__ == '__main__':
    print(f"Total byte count: {file_size('test.txt')}")
