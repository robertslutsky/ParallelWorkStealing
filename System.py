import random
from Node import Node
from Processor import Processor


class System:
    def __init__(self, num_processors=1, method='random', num_clusters=1):
        self.num_processors = num_processors
        self.method = method
        self.num_clusters = num_clusters
        self.processors = [Processor(i, method, cluster=i % num_clusters) for i in range(num_processors)]
        self.step_number = 0
        self.steal_attempts = 0
        self.successful_steals = 0
        Processor.counter = 0
        Node.counter = 0

    def run(self, start):
        self.processors[0].startup(start)
        x = [p for p in self.processors if p.is_active()]
        while x:
            self.step()
            x = [p for p in self.processors if p.is_active()]
        print("done")
        out = self.step_number, self.steal_attempts, self.successful_steals
        self.reset()
        return out

    def reset(self):
        self.step_number=0
        self.steal_attempts = 0
        self.successful_steals = 0

    def step(self):
        print('\nstep:'+str(self.step_number))
        self.step_number += 1
        to_steal = [p for p in self.processors if not p.is_active()]
        to_complete = [p for p in self.processors if p.is_active()]
        self.steal_attempts += len(to_steal)
        # random so order/winner isn't always set
        random.shuffle(to_steal)
        random.shuffle(to_complete)
        for p in to_steal:
            success = p.steal(self.processors)
            if success: self.successful_steals += 1
        for p in to_complete:
            p.complete()
        for p in to_steal:
            print(f"p{str(p.id)}'s current: {p.current}, deque:", [str(item) for item in p.deque])
        for p in to_complete:
            print(f"p{str(p.id)}'s current: {p.current}, deque:", [str(item) for item in p.deque])


    def __str__(self):
        return(f"#p={self.num_processors}, method={self.method}")

# moved this stuff to main
start = Node()
end = Node([start])
start.children = [end]

# x,y=start.spawn()
# start.be_a_spawn()
x, y = start.be_a_spawn()
# x, y = x.be_a_spawn()
x, y = x.be_a_spawn()
# end.graph_p()
s = System(2, method='random',num_clusters=2)
random.seed(6)
s.run(start)
start.graph()