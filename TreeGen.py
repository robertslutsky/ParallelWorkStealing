import random
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from Node import Node


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
            g.add_node(n)
            g.add_edge(self, n)
            n.graph_help(g)


class SearchTree:
    def __init__(self):
        pass

    def graph(self):
        self.root.graph()


class BinomialTree(SearchTree):
    def __init__(self, m, q):
        self.root = TreeNode()
        self.gen_tree(self.root, m, q)
        super().__init__()
        TreeNode.counter = 0

    def gen_tree(self, root, m, q):
        if random.random() < q:
            for i in range(m):
                t = TreeNode()
                root.children.append(t)
                self.gen_tree(t, m, q)

class GeometricTree(SearchTree):
    # b is mean so inverse of normal geometric parameter
    def __init__(self, b, d=10):
        self.root = TreeNode()
        self.gen_tree(self.root, b, d)
        TreeNode.counter = 0
        super().__init__()

    def gen_tree(self, root, b, d):
        if d == 0:
            return
        branches = np.random.geometric(1 / b)
        for i in range(branches):
            t = TreeNode()
            root.children.append(t)
            self.gen_tree(t, b, d - 1)


def generate_dag(tree_root):
    Node.counter = 0
    start = Node()  # dag root
    end = Node([start])
    start.children = [end]
    c = start.continuation()
    pfor(tree_root, c)

    return start


def pfor(tree_node, dag_node):
    # generates the parallel_for "triangle" dag for the tree node based on how many children it has (how many iterations the parallel for loop should run for)
    # tree_node is the node in the tree that we want to generate the p_for dag for
    # dag_node is the node that we want the root of the parallel_for

    num_iterations = len(tree_node.children)
    leaves = pfor_helper(dag_node, 0,
                         num_iterations - 1)  # nodes in execution dag that are responsible for execution (leaves of the parallel_for "triangle" dag)
    if len(leaves) != num_iterations:
        assert ValueError("should be same number of leaves as there are iterations")

    for i in range(num_iterations):
        if tree_node.children[i].children:
            pfor(tree_node.children[i], leaves[i].continuation())
        else:
            pfor(tree_node.children[i], leaves[i])

def pfor_helper(node, min, max):
    # node: node in dag in the pfor tree
    # min: smallest iteration in for loop this node is responsible for
    # min: smallest iteration in for loop this node is responsible for
    # return: leaf nodes of the subdag from node
    if min >= max:
        # base case
        return [node]
    else:
        mid = int((min + max) / 2)
        left_child, right_child = node.be_a_spawn()
        left_leaves = pfor_helper(left_child, min, mid)
        right_leaves = pfor_helper(right_child, mid + 1, max)
        return left_leaves + right_leaves
      
def tree_count(root):
    # return signature: depth, count
    if len(root.children)==0:
        # base case, at a leaf node
        depth = 0
        count = 1
        return depth, count
    else:
        depths_counts = [tree_count(child) for child in root.children] # list of tuples (depth, num_nodes) for each of the subtree
        depths = [depth_count_pair[0] for depth_count_pair in depths_counts]
        counts = [depth_count_pair[1] for depth_count_pair in depths_counts]
        return max(depths)+1, sum(counts)+1


# i=20
# while True:
#     print(i)
#     random.seed(i)
#     bt = BinomialTree(5,.18)
#     bt.graph()
#     i+=1

random.seed(55)
bt = BinomialTree(3, .18)
bt.graph()

print("depth, count", tree_count(bt.root))

dag = generate_dag(bt.root)
dag.graph()


num_good_trees = 0
counts = []
num_trees = 0
while num_good_trees < 10:
    bt = BinomialTree(3,.18)
    dag = generate_dag(bt.root)
    dag.graph()
    depth, count = tree_count(bt.root)
    if depth>10:
        counts.append(count)
        num_good_trees += 1
        num_trees += 1
print(counts)
print(num_trees)


gt = GeometricTree(2, 3)
gt.graph()
dag2 = generate_dag(gt.root)
dag2.graph()
