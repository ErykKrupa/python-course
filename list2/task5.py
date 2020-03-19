from argparse import ArgumentParser
from sys import argv, stderr
import random


def _is_prime(number, attempts=10):
    """
        Miller-Rabin primality test.

        A return value of False means n is certainly not prime. A return value of
        True means n is very likely a prime.
    """
    if number != int(number):
        return False
    number = int(number)
    if attempts != int(attempts):
        attempts = 10
    if number in [0, 1, 4, 6, 8, 9]:
        return False
    if number in [2, 3, 5, 7]:
        return True
    s = 0
    d = number - 1
    while d % 2 == 0:
        d >>= 1
        s += 1
    assert (2 ** s * d == number - 1)

    def _trial_composite(test_number):
        if pow(test_number, d, number) == 1:
            return False
        for j in range(s):
            if pow(test_number, 2 ** j * d, number) == number - 1:
                return False
        return True

    for i in range(attempts):
        if _trial_composite(random.randrange(2, number)):
            return False
    return True


# greatest common divisor
def _gcd(a, b):
    if a == 0:
        return b
    return _gcd(b % a, a)


def _naive_generate(phi):
    e = random.randint(1, phi)
    while _gcd(e, phi) != 1:
        e = random.randint(1, phi)

    d = random.randint(1, phi)
    while (d * e) % phi != 1:
        d = random.randint(1, phi)

    return e, d


def _multiplicative_inversion(a, b):
    new_s = 0
    old_s = 1
    new_r = b
    old_r = a

    while new_r != 0:
        quotient = old_r // new_r
        old_r, new_r = new_r, old_r - quotient * new_r
        old_s, new_s = new_s, old_s - quotient * new_s

    return old_s


def _fast_generate(phi):
    e = -1
    while e < 0:
        d = random.randint(2, phi - 1)
        while _gcd(d, phi) != 1:
            d = random.randint(2, phi - 1)
        e = _multiplicative_inversion(d, phi)

    return e, d


def generate_keys(bits):
    bits = int(bits)
    min_number = 2 ** (bits - 1)
    max_number = 2 ** bits

    p = random.randint(min_number, max_number)
    while not _is_prime(p):
        p = random.randint(min_number, max_number)
    print(f'p   = {p}')

    q = random.randint(min_number, max_number)
    while not _is_prime(q):
        q = random.randint(min_number, max_number)
    print(f'q   = {q}')

    n = p * q
    print(f'n   = {n}')

    phi = (p - 1) * (q - 1)
    print(f'phi = {phi}')

    # e, d = naive_generate(phi)
    e, d = _fast_generate(phi)
    print(f'e   = {e}')
    print(f'd   = {d}')

    with open('key.pub', 'w') as file:
        file.write(str(n) + '\n')
        file.write(str(e) + '\n')

    with open('key.prv', 'w') as file:
        file.write(str(n) + '\n')
        file.write(str(d) + '\n')


def encrypt(message):
    try:
        with open('key.pub', 'r') as file:
            n = int(file.readline())
            e = int(file.readline())
    except FileNotFoundError:
        print("No key.pub file", file=stderr)
        exit()
    except ValueError:
        print("key.pub file damaged", file=stderr)
        exit()
    n_len = len(str(n))
    for char in message.encode("utf-8"):
        print(f'{pow(char, e, n):0{n_len}}', end='')


def decrypt(encrypted_message):
    try:
        with open('key.prv', 'r') as file:
            n = int(file.readline())
            d = int(file.readline())
    except FileNotFoundError:
        print("No key.prv file", file=stderr)
        exit()
    except ValueError:
        print("key.prv file damaged", file=stderr)
        exit()
    n_len = len(str(n))
    split_numbers = [encrypted_message[i:i + n_len] for i in range(0, len(encrypted_message), n_len)]
    message = bytes(pow(int(number), d, n) for number in split_numbers).decode()
    print(message)


if __name__ == '__main__':
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.required = True
    group.add_argument('--gen-keys', '-g')
    group.add_argument('--encrypt', '-e')
    group.add_argument('--decrypt', '-d')
    arguments = vars(parser.parse_args(argv[1:]))
    arguments = list(filter(lambda x: x[1] is not None, arguments.items()))[0]
    key, value = arguments[0], arguments[1]
    {
        "gen_keys": generate_keys,
        "encrypt": encrypt,
        "decrypt": decrypt
    }[key](value)
