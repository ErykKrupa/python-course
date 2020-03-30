def flatten(element):
    if isinstance(element, list):
        for item in element:
            yield from flatten(item)
    else:
        yield element


if __name__ == '__main__':
    print(list(flatten([[1, [], 2, ["a", 4, "b", 5, 5, 5]], [4, 5, 6], 7, [[9, [123, [[123]]]], 10]])))
