from Node import Node
from System import System
import random
# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start = Node()
    end = Node([start])
    start.children = [end]

    # x,y=start.spawn()
    # start.be_a_spawn()
    x, y = start.be_a_spawn()
    x.continuation()
    # x.continuation().continuation().continuation()
    # y.continuation().continuation().continuation().continuation().spawn()
    # end.graph_p()
    s = System(start,3, method='random')
    random.seed(0)
    s.run()
    start.graph()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
