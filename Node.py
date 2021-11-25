import networkx as nx
import matplotlib.pyplot as plt


class Node:
    counter = 0

    # state: 0: not ready, 1: ready, 2:completed
    def __init__(self, parents=None, children=None, state=0):
        self.id = Node.counter
        Node.counter += 1
        self.parents = []
        if parents:
            self.parents = parents
        self.children = []
        if children:
            self.children = children
        self.state = state

    def update_state(self):
        if self.state == 0:
            for c in self.parents:
                if c.state != 2:
                    return
            self.state = 1

    def is_ready(self):
        return self.state == 1

    def complete(self):
        print(self)
        self.state = 2

    def __str__(self):
        parentString = 'parents: '
        for p in self.parents:
            parentString += str(p.id) + ' '
        childrenString = 'children: '
        for c in self.children:
            childrenString += str(c.id) + ' '
        # return str(self.id) + ' ' + parentString + childrenString
        return str(self.id)

    def spawn(self):
        spawn = Node([self])
        c1 = Node([spawn])
        c2 = Node([spawn])
        sync = Node([c1, c2], [self.children[0]])
        self.children[0].parents = [sync]
        self.children = [spawn]
        c1.children = [sync]
        c2.children = [sync]
        spawn.children = [c1, c2]
        return c1, c2

    #node both spawn/sync would cause problems
    def be_a_spawn(self):
        c1 = Node([self])
        c2 = Node([self])
        sync = Node([c1, c2], [self.children[0]])
        self.children[0].parents = [sync]
        self.children = [c1,c2]
        c1.children = [sync]
        c2.children = [sync]
        return c1, c2

    def continuation(self):
        c = Node([self], self.children)
        self.children[0].parents.remove(self)
        self.children[0].parents.append(c)
        self.children = [c]
        return c

    def recur(self):
        print(self)
        for c in self.children:
            c.recur()

    def graph(self):
        g = nx.DiGraph()
        g.add_node(self)
        self.graph_help(g)
        nx.draw_planar(g, with_labels=True)
        plt.show()

    def graph_help(self, g):
        for n in self.children:
            g.add_node(n)
            g.add_edge(self, n)
            n.graph_help(g)

    def graph_p(self):
        g = nx.DiGraph()
        g.add_node(self)
        self.graph_help_p(g)
        nx.draw(g, with_labels=True)
        plt.show()

    def graph_help_p(self, g):
        for n in self.parents:
            g.add_node(n)
            g.add_edge(n, self)
            n.graph_help_p(g)
