from inspect import getfullargspec
import math


class overload:
    functions = {}

    def __init__(self, func):
        self.name = func.__name__
        args_count = len(getfullargspec(func).args)
        if self.name not in overload.functions.keys():
            overload.functions[self.name] = {args_count: func}
        else:
            overload.functions[self.name][args_count] = func

    def __call__(self, *args, **kwargs):
        return overload.functions[self.name][len(args)](*args, **kwargs)


@overload
def norm(x, y):
    return math.sqrt(x * x + y * y)


@overload
def norm(x, y, z):
    return abs(x) + abs(y) + abs(z)


print(f"norm(2,4) = {norm(2, 4)}")
print(f"norm(2,3,4) = {norm(2, 3, 4)}")

