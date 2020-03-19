from sys import argv, stderr
from os.path import getsize
import re

if __name__ == '__main__':
    if len(argv) == 1:
        print("File name not passed.", file=stderr)
        exit(1)
    words_count = 0
    lines_count = 0
    max_line_length = 0
    try:
        file = open(argv[1])
    except EnvironmentError:
        print(f"File {argv[1]} not found.", file=stderr)
        exit(2)
    else:
        with file:
            line = file.readline()
            while line:
                words_count += len(re.findall(r'\w+', line))
                lines_count += 1
                max_line_length = max(max_line_length, len(line))
                line = file.readline()

    print(f"Size in bytes: {getsize(argv[1]):>12}")
    print(f"Lines: {lines_count:>20}")
    print(f"Words: {words_count:>20}")
    print(f"Max line length: {max_line_length:>10}")
