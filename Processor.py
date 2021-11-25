from collections import deque
import random


class Processor:
    def __init__(self, id, method='random', current=None):
        self.deque = deque()
        self.current = None
        self.method = method
        self.id = id
        self.active = False

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
        print('processor:'+str(self.id) +' completed')
        self.current.complete()
        for c in self.current.children:
            c.update_state()
        ready_children = [n for n in self.current.children if n.is_ready()]
        if len(ready_children) > 0:
            self.current = ready_children[0]
            if len(ready_children) == 2:
                self.deque.appendleft(ready_children[1])
        else:
            self.active = False

    def steal(self, processors):
        # needs to be implemented for each option
        if self.method == 'random':
            #need to mod so won't choose itself?
            p = random.choice(processors)
            if p.deque:
                self.current = p.deque.pop()
                print('processor '+str(self.id)+' stole: '+str(self.current.id))
                self.active = True
                return True
        print('processor ' + str(self.id) + ' failed steal')
        return False

    def startup(self, n):
        self.active = True
        self.current = n
