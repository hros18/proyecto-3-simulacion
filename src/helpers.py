import random as rnd

class Kid:
    def __init__(self):
        pass

    def __str__(self):
        return "k"    

    def __hash__(self):
        return self.x ** self.y

class Corral:
    def __init__(self):
        self.kid = None

    @property
    def with_kid(self):
        return self.kid != None

    def __str__(self):
        return "C"

class Obstacle:
    def __init__(self):
        pass

    def __str__(self):
        return "X"

class Cell:
    def __init__(self, x, y, obj = None, agent = None, dirty = False):
        self.x = x
        self.y = y
        self.obj = obj
        self.agent = agent
        self.dirty = dirty

    def set_obj(self, obj):
        self.obj = obj
        self.obj.x = self.x
        self.obj.y = self.y

    def set_agent(self, agent):
        self.agent = agent
        self.agent.x = self.x
        self.agent.y = self.y

    def free_obj(self):
        self.obj = None

    def free_agent(self):
        self.agent = None

    @property
    def is_dirty(self):
        return self.dirty

    @property
    def is_empty(self):
        return self.obj == None and self.agent == None and not self.dirty

    def __str__(self):
        if self.agent:
            return str(self.agent)
        elif self.obj:
            return str(self.obj)
        elif self.dirty:
            return "*"
        else:
            return "_"

def rnd(l, pred=None, count=1):
    nl = l
    if pred:
        nl = list(filter(pred, l))
    elem = rnd.choice(nl)
    l.remove(elem)
    return elem
    
def rnd_many(l, count):
    seq = []
    while count and l:
        seq.append(rnd_choice(l))
        count -= 1
    return seq