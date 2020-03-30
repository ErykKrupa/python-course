def all_subsets(list_):
    # functional syntax
    # return [[]] if len(list_) == 0 else \
    #     list(map(lambda i: [list_[0]] + i, all_subsets(list_[1:]))) + all_subsets(list_[1:])
    if len(list_) == 0:
        return [[]]
    head = [list_[0]]
    subsets = all_subsets(list_[1:])
    return list(map(lambda i: head + i, subsets)) + subsets


if __name__ == '__main__':
    [print(x) for x in all_subsets([1, 2, 3, 4, 5])]
