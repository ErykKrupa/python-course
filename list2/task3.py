from sys import argv, stderr
from os import walk, rename
from os.path import isdir, join

if __name__ == '__main__':
    if len(argv) == 1:
        print("Dictionary name not passed.", file=stderr)
        exit(1)
    if not isdir(argv[1]):
        print(f"Dictionary {argv[1]} not found.", file=stderr)
        exit(2)
    for root, _, files in walk(argv[1]):
        rename(root, root.lower())
        for name in files:
            rename(join(root, name), join(root, name).lower())

