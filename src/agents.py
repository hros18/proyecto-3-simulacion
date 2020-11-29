from helpers import *
import numpy as np

class Agent:
    def __init__(self):
        self.carry = None

    def see(self, env):
        pass

    def action(self, env):
        if env.env[self.x][self.y].is_dirty:
            env.env[self.x][self.y].dirty = False
            env.dirty -= 1
        elif isinstance(env.env[self.x][self.y].obj, Corral) and self.carry:
            env.env[self.x][self.y].obj.kid = self.carry
            self.carry = None
        else:
            if self.looked is None:
                return

            step = 1 + bool(self.carry)

            while step:
                if str(self.looked) == "k":
                    nx, ny = self.compute_next_move((self.looked.x, self.looked.y), env)
                    env.move_agent(nx, ny)
                    if str(env.env[self.x][self.y].obj) == "k":
                        self.carry = env.env[self.x][self.y].obj
                        env.env[self.x][self.y].obj = None
                        env.remove_kid(self.carry)
                else:
                    nx, ny = self.compute_next_move((self.looked.x, self.looked.y), env, obs=["O", "C", "k"])
                    env.move_agent(nx, ny)
                step -= 1

    def next(self, env):
        self.see(env)
        self.action(env)

    def compute_next_move(self, pos, env, obs=["O", "C"]):
        x, y = pos
        dx = np.sign(x - self.x)
        dy = np.sign(y - self.y)
        
        if str(env.env[self.x + dx][self.y + dy]) in obs:
            if str(env.env[self.x + dx][self.y + dy]) == "C" and not env.env[self.x + dx][self.y + dy].obj.with_kid:
                pass
            else:
                try:
                    return rnd_choice(env.map_adj((self.x, self.y)), pred=lambda z: env.env[z[0]][z[1]].obj == None)
                except:
                    return self.x, self.y

        return self.x + dx, self.y + dy

    def __str__(self):
        return "A"

class Reactive(Agent):
    def __init__(self):
        super().__init__()
        self.looked = None

    def see(self, env):
        pos = (self.x, self.y)
        if not self.carry and len(env.kids):
            self.looked = near_obj(pos, env, ["k"])
        else:
            self.looked = near_obj(pos, env, ["C", "X"])

    @property
    def name(self):
        return "Reactive"

    def __str__(self):
        return "R" if not self.carry else "r"

class Proactive(Agent):
    def __init__(self):
        super().__init__()
        self.looked = None

    def see(self, env):
        pos = (self.x, self.y)
        dp = env.garbage_pc()
        if not self.carry and len(env.kids):
            self.looked = near_obj(pos, env, ["k"])
        elif self.carry:
            self.looked = near_obj(pos, env, ["C"])
        else:
            self.looked = near_obj(pos, env, ["X"])

    @property
    def name(self):
        return "Proactive"

    def __str__(self):
        return "P" if not self.carry else "p"

def near_obj(pos, env, search):    
    queue = [pos]
    mark = [ [ False for _ in range(len(env.env[0]))] for _ in range(len(env.env)) ]
    obj = None
    while queue:
        x, y = queue.pop(0)
        if mark[x][y]:
            continue
        mark[x][y] = True
        if str(env.env[x][y]) in search:
            if str(env.env[x][y]) == "C" and env.env[x][y].obj.with_kid:
                pass     
            else:
                obj = env.env[x][y]
                break
        for ax, ay in env.directions(x, y):
            if not mark[ax][ay]:
                queue.append((ax, ay))
    return obj