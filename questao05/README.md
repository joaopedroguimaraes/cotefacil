# Questão 5

Uma _Árvore_ é uma estrutura de dados não linear que consiste em um conjunto de nós conectados por arestas. Cada nó tem um pai (exceto a raiz) e pode ter vários filhos.

Em Python, podemos criar uma árvore usando uma classe que representa o nó da árvore e suas conexões com outros nós.

A seguir, descrevo os passos para criar uma árvore em Python:

## 1. Definir a classe Node

A classe Node representa um nó da árvore e contém as seguintes informações:
	
- um valor (ou dados) armazenados no nó
- uma referência ao nó pai
- uma lista de referências aos nós filhos

```python
class Node:
    def __init__(self, value):
        self.value = value
        self.parent = None
        self.children = []
```

## 2. Definir a classe Tree

A classe Tree representa a árvore e contém uma referência ao nó raiz. A árvore também pode ter métodos que permitem adicionar e remover nós, assim como tais respectivas validações.

```python
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
```

O método _add_node_ permite adicionar um nó à árvore especificando seu valor e o nó pai. Se o nó pai não for especificado, o novo nó será definido como a raiz da árvore.

O método _remove_node_ permite remover um nó da árvore.

## 3. Testar a árvore
	
Podemos testar a árvore criando alguns nós e adicionando-os à árvore. Depois, podemos então percorrer a árvore para verificar se os nós foram adicionados corretamente.

```python
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
```

Este teste cria uma árvore com sete nós e verifica se os nós foram adicionados corretamente.

## 4. Executar os testes

Para executar os testes, basta chamar a função test_tree():

```python
test_tree()
```

Se todos os testes passarem, a árvore foi criada corretamente e está pronta para ser usada.