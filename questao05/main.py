class Node:
    def __init__(self, value):
        self.value = value
        self.parent = None
        self.children = []


class Tree:
    def __init__(self):
        self.root = None

    def add_node(self, value, parent=None):
        new_node = Node(value)
        if parent is None:
            self.root = new_node
        else:
            parent.children.append(new_node)
            new_node.parent = parent

    def remove_node(self, node):
        if node == self.root:
            self.root = None
        else:
            parent = node.parent
            parent.children.remove(node)


def test_tree():
    tree = Tree()

    # Adicionando alguns nós à árvore
    tree.add_node(1)
    tree.add_node(2, tree.root)
    tree.add_node(3, tree.root)
    tree.add_node(4, tree.root.children[0])
    tree.add_node(5, tree.root.children[0])
    tree.add_node(6, tree.root.children[1])
    tree.add_node(7, tree.root.children[1])

    # Percorrendo a árvore
    assert tree.root.value == 1
    assert tree.root.children[0].value == 2
    assert tree.root.children[1].value == 3
    assert tree.root.children[0].children[0].value == 4
    assert tree.root.children[0].children[1].value == 5
    assert tree.root.children[1].children[0].value == 6
    assert tree.root.children[1].children[1].value == 7


if __name__ == '__main__':
    test_tree()
