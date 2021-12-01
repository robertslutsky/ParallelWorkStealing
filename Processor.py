from collections import deque
import random


class Processor:
    def __init__(self, id, method='random', current=None, cluster = 0):
        self.deque = deque()
        self.current = None
        self.method = method
        self.id = id
        self.active = False
        self.cluster = cluster
        self.delay = 0
        self.victim = None
        if method == "revenge":
            self.last_stole_from_id = id-1 # initialize to processor to the left. Can be -1, will be taken care of when choosing the processor

        if method == "revenge":
            self.last_stole_from_id = id-1 # initialize to processor to the left. Can be -1, will be taken care of when choosing the processor

    # def activate(self):
    #     if self.deque:
    #         self.current = self.deque.pop()
    #         self.active = True
    #         return True
    #     else:
    #         self.active = False
    #     return self.active

    def is_active(self):
        return self.active

    def complete(self):
        print('processor:'+str(self.id) +' completed', end=" ")
        self.current.complete()

        # update states of children after completing node because might become ready if all parents are completed
        for c in self.current.children:
            c.update_state()

        # depending on number of nodes the processor enables, choose what to do
        ready_children = [n for n in self.current.children if n.is_ready()]
        if len(ready_children) > 0:
            # enables at least 1
            self.current = ready_children[0]
            if len(ready_children) == 2:
                self.deque.appendleft(ready_children[1])

            if len(ready_children)==1:
                print("enabled1: ", self.current.id)
            if len(ready_children)==2:
                print("enable2: ", ready_children[0].id, ready_children[1].id)
        else:
            # doesn't enable any
            if len(self.deque)==0:
                # nothing on deque to take from
                print("enable0: none on deque")
                self.active = False
                self.current = None
            else:
                # can pop from bottom of deque
                self.current = self.deque.popleft()
                print("enable0: pop from deque:", self.current.id)
            

    def steal(self, processors):
        # choosing processor to steal from
        # needs to be implemented for each option
        if self.delay == 0:
            if self.method == 'random':
                #need to mod so won't choose itself?
                self.victim = random.choice(processors)

            elif self.method == 'right':
                num_processors = len(processors)
                steal_index = (self.id + 1) % num_processors
                self.victim = processors[steal_index]

            elif self.method == 'revenge':
                # steal from processor that stole from you last (can try different ways of initializing who to take from first if never been stolen from)
                num_processors = len(processors)
                steal_index = (self.last_stole_from_id) % num_processors # handles if id is -1
                self.victim = processors[steal_index]
                self.victim.last_stole_from_id = self.id # tell processor you are stealing from to steal from you

            elif self.method == 'last_pusher':
                # steal from the processor that pushed to its deque latest
                assert NotImplemented("oof")

            elif self.method == 'last_mover':
                # steal from the processor that pushed to its deque or stole from another deque latest (idk how this could be better, but whatever)
                assert NotImplemented("oof")

            #delay for which processor stole from
            if self.victim.cluster == self.cluster:
                self.delay = 1
            else:
                self.delay = 2
            # actually stealing from processor
            print(f"proc {str(self.id)} sent steal attempt to {str(self.victim.id)}, w/ delay {self.delay}", end=", ")

        if self.delay == 1 and self.victim.deque:
            self.current = self.victim.deque.pop()

        self.delay -= 1

        if self.delay == 0:
            print('processor ' + str(self.id) + ' delay has ended', end=", ")
            if self.current is not None:
                self.active = True
                print('processor '+str(self.id)+' got response and stole: '+str(self.current.id))
                return True
            else:
                print('processor ' + str(self.id) + ' got response and failed steal')
                return False
        print()

    def startup(self, n):
        self.active = True
        self.current = n
