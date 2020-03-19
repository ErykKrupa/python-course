from sys import argv, stderr
from os import walk
from os.path import isdir, join, getsize
from hashlib import sha512

if __name__ == '__main__':
    if len(argv) == 1:
        print("Dictionary name not passed.", file=stderr)
        exit(1)
    if not isdir(argv[1]):
        print(f"Dictionary {argv[1]} not found.", file=stderr)
        exit(2)

    files_list = {}
    for root, _, files_names in walk(argv[1]):
        for name in files_names:
            name = join(root, name)
            with open(name, 'r') as file:
                content = file.read()
            hash_ = sha512(content.encode()).hexdigest()
            size = getsize(name)
            if (hash_, size) in files_list:
                files_list[(hash_, size)].append(name)
            else:
                files_list[(hash_, size)] = [name]
    for files_names in files_list.values():
        if len(files_names) > 1:
            for name in files_names:
                print(name)
            print('--------------------')
