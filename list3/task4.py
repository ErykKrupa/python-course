import random


def quick_sort(list_):
    # functional syntax
    # return list_ if len(list_) == 0 else \
    #     (quick_sort(list(filter(lambda y: y < list_[0], list_[1:])))
    #      + [list_[0]]
    #      + quick_sort(list(filter(lambda y: y >= list_[0], list_[1:]))))
    if len(list_) == 0:
        return list_
    x = list_[0]
    xs = list_[1:]
    return (quick_sort(list(filter(lambda y: y < x, xs)))
            + [x]
            + quick_sort(list(filter(lambda y: y >= x, xs))))


if __name__ == "__main__":
    test_list = [random.randrange(-50, 100) for i in range(200)]
    sorted_list = sorted(test_list)
    quick_sorted_list = quick_sort(test_list)
    print('pass' if sorted_list == quick_sorted_list else 'fail')
