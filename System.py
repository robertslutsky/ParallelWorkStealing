import random
from Node import Node
from Processor import Processor


class System:
    def __init__(self, start, num_processors=1, method='random'):
        self.num_processors = num_processors
        self.method = method
        self.processors = [Processor(i, method) for i in range(num_processors)]
        self.processors[0].startup(start)

    def step(self):
        to_steal = [p for p in self.processors if not p.is_active()]
        to_complete = [p for p in self.processors if p.is_active()]
        # random so order/winner isn't always set
        random.shuffle(to_steal)
        random.shuffle(to_complete)
        for p in to_steal:
            p.steal(self.processors)
        for p in to_complete:
            p.complete()


start = Node()
end = Node([start])
start.children = [end]
x, y = start.spawn()
x.continuation()
y.continuation().continuation().continuation()
start.graph()
s = System(start)
s.step()
s.step()
s.step()
s.step()
s.step()
s.step()
s.step()
s.step()
s.step()
s.step()
s.step()
s.step()