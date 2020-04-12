from random import randrange, choice


class Node(object):
    def __init__(self, content, parent=None, *children):
        self.content = content
        self.parent = parent
        self.children = list(children)

    def add_children(self, *children) -> None:
        self.children.extend(children)


class RandomDataFactory:
    def __init__(self, height, density):
        self.range = range(density ** (height + 1))

    def get_random_data(self) -> int:
        return choice(self.range)


def generate(height: int, density: int, root: Node = None,
             element_factory: RandomDataFactory = None) -> Node:
    if element_factory is None:
        element_factory = RandomDataFactory(height, density)
    node = Node(element_factory.get_random_data(), root)
    if height == 0:
        return node
    node.add_children(
        *[generate(height - 1, density, node, element_factory)
          for i in range(1, randrange(1, density * 2) + 1)])
    return node


def dfs(node: Node):
    yield node.content
    for child in node.children:
        yield from dfs(child)


def bfs(node):
    nodes = [node]
    while nodes:
        node = nodes.pop(0)
        nodes.extend(node.children)
        yield node.content


if __name__ == "__main__":
    tree = generate(3, 2)
    print("DFS: ", end='')
    for element in dfs(tree):
        print(element, end=" ")
    print()
    print("BFS: ", end='')
    for element in bfs(tree):
        print(element, end=" ")