import random
import networkx as nx
import matplotlib.pyplot as plt

class TreeNode:
    # maybe reset?
    counter = 0

    def __init__(self):
        self.children = []
        # self.parents =[]
        self.id = TreeNode.counter
        TreeNode.counter += 1

    def __str__(self):
        return str(self.id)

    def graph(self):
        g = nx.DiGraph()
        g.add_node(self)
        self.graph_help(g)
        nx.draw_planar(g, with_labels=True)
        plt.show()

    def graph_help(self, g):
        for n in self.children:
            if n.id>10:
                return
            g.add_node(n)
            g.add_edge(self, n)
            n.graph_help(g)

class BinomialTree:
    def __init__(self, m, q):
        self.root = TreeNode()
        self.gen_tree(self.root, m, q)

    def gen_tree(self, root, m, q):
        if random.random() < q:
            for i in range(m):
                t = TreeNode()
                root.children.append(t)
                self.gen_tree(t,m,q)

    def graph(self):
        self.root.graph()

bt = BinomialTree(10,.01)
bt.graph()