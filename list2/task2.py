from sys import argv, stderr
import re

_base64_str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'


def encode(raw_file_path, encrypted_file_path):
    raw_file = open(raw_file_path, 'r')
    encrypted_file = open(encrypted_file_path, 'w')

    blob = ''.join(f'{char:08b}'
                   for char in raw_file.read().encode('utf-8'))
    bits_list = re.findall(".{1,6}", blob)
    if len(bits_list[-1]) == 2:
        bits_list[-1] += '0000'
        end = '=='
    elif len(bits_list[-1]) == 4:
        bits_list[-1] += '00'
        end = '='
    else:
        end = ''
    encrypted_file.write(''.join(_base64_str[int(bits, 2)] for bits in bits_list))
    encrypted_file.write(end)

    raw_file.close()
    encrypted_file.close()


def decode(encrypted_file_path, raw_file_path):
    encrypted_file = open(encrypted_file_path, 'r')
    raw_file = open(raw_file_path, 'w')

    blob = ''.join(f'{_base64_str.index(char):06b}'
                   for char in encrypted_file.read() if char != '=')
    bits_list = re.findall(".{1,8}", blob)
    if len(bits_list[-1]) != 8:
        del bits_list[-1]
    raw_file.write(''.join(chr(int(bits, 2)) for bits in bits_list))

    raw_file.close()
    encrypted_file.close()


if __name__ == '__main__':
    if len(argv) <= 3:
        print("Not enough parameters.", file=stderr)
        exit(1)
    try:
        if argv[1] == '--encode' or argv[1] == '-e':
            encode(argv[2], argv[3])
        elif argv[1] == '--decode' or argv[1] == '-d':
            decode(argv[2], argv[3])
        else:
            print(f"Unknown parameter {argv[1]}.", file=stderr)
            exit(2)
    except EnvironmentError:
        print(f"Problem with access {argv[2]} or {argv[3]} occurred."
              f"Does {argv[2]} exist?", file=stderr)
        exit(3)
