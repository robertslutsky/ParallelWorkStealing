import random
from Node import Node
from Processor import Processor


class System:
    def __init__(self, start, num_processors=1, method='random', num_clusters=1):
        self.num_processors = num_processors
        self.method = method
        self.num_clusters = num_clusters
        self.processors = [Processor(i, method, cluster=i % num_clusters) for i in range(num_processors)]
        self.processors[0].startup(start)
        self.step_number = 0
        Processor.counter = 0
        Node.counter = 0

    def run(self):
        x = [p for p in self.processors if p.is_active()]
        while x:
            self.step()
            x = [p for p in self.processors if p.is_active()]
        print("done")

    def step(self):
        print('step:'+str(self.step_number))
        self.step_number += 1
        to_steal = [p for p in self.processors if not p.is_active()]
        to_complete = [p for p in self.processors if p.is_active()]
        # random so order/winner isn't always set
        random.shuffle(to_steal)
        random.shuffle(to_complete)
        for p in to_steal:
            p.steal(self.processors)
        for p in to_complete:
            p.complete()


# moved this stuff to main
start = Node()
end = Node([start])
start.children = [end]

# x,y=start.spawn()
# start.be_a_spawn()
x, y = start.be_a_spawn()
x, y = x.be_a_spawn()
x, y = x.be_a_spawn()
# end.graph_p()
s = System(start,2, method='random',num_clusters=1)
random.seed(6)
s.run()
start.graph()