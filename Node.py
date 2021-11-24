import networkx as nx
import matplotlib.pyplot as plt
class Node:
    counter = 0
    def __init__(self, parents=None, children=None):
        self.value = Node.counter
        Node.counter += 1
        self.parents =[]
        if parents:
            self.parents = parents
        self.children =[]
        if children:
            self.children = children

    def __str__(self):
        parentString ='parents: '
        for p in self.parents:
            parentString += str(p.value) + ' '
        childrenString='children: '
        for c in self.children:
            childrenString += str(c.value) + ' '
        # return str(self.value) + ' ' + parentString + childrenString
        return str(self.value)

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
        return c1,c2

    def continuation(self):
        c = Node([self], self.children)
        self.children[0].parents.remove(self)
        print(self.children[0].parents)
        self.children[0].parents.append(c)
        print(self.children[0].parents)
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

    def graph_help(self,g):
        for n in self.children:
            g.add_node(n)
            g.add_edge(self,n)
            n.graph_help(g)

    def graph_p(self):
        g = nx.DiGraph()
        g.add_node(self)
        self.graph_help_p(g)
        nx.draw(g, with_labels=True)
        plt.show()

    def graph_help_p(self,g):
        for n in self.parents:
            g.add_node(n)
            g.add_edge(n,self)
            n.graph_help_p(g)


start = Node()
end = Node([start])
start.children = [end]
x,y=start.spawn()
x.continuation()
y.continuation().continuation().continuation()
start.recur()
start.graph()
# end.graph_p()

