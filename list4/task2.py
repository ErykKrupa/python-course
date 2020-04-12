from random import randrange, shuffle
from typing import List, Generator


def update_sequence(sequence: List[int]) -> None:
    for i in range(len(sequence)):
        if sequence[i] != 2:
            sequence[i] += 1
            break
        else:
            sequence[i] = 1
    else:
        sequence.append(1)


def generate(height: int) -> List:
    amount = randrange(height ** 2, (height + 1) ** 2)
    data = [str(i) for i in range(amount)]
    shuffle(data)
    tree = [data[0], None, None]
    sequence = [1]
    for i in range(1, amount):
        sub_tree = tree
        for j in range(len(sequence) - 1, 0, -1):
            sub_tree = sub_tree[sequence[j]]
        sub_tree[sequence[0]] = [data[i], None, None]
        update_sequence(sequence)
    return tree


def dfs(tree: List) -> Generator:
    if tree is None:
        return
    yield tree[0]
    yield from dfs(tree[1])
    yield from dfs(tree[2])


def bfs(tree: List) -> Generator:
    subtrees = [tree]
    while subtrees:
        subtree = subtrees.pop(0)
        yield subtree[0]
        if subtree[1] is not None:
            subtrees.append(subtree[1])
        if subtree[2] is not None:
            subtrees.append(subtree[2])


if __name__ == "__main__":
    x = generate(3)
    print(x)
    print("DFS: ", end='')
    for element in dfs(x):
        print(element, end=" ")
    print()
    print("BFS: ", end='')
    for element in bfs(x):
        print(element, end=" ")
