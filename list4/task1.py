from time import time, sleep


def show_time(func):
    def print_time(*args):
        start_time = time()
        func(*args)
        print(f'time: {time() - start_time}')
    return print_time


@show_time
def test(amount, sleep_time):
    for i in range(1, amount + 1):
        sleep(sleep_time)
        print(f"test {i}")


if __name__ == '__main__':
    test(20, 0.1)
