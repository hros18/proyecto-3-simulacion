from helpers import *
import random as rnd
cardinals = [
    (0, 0),
    (-1, 0),
    (0, -1),
    (0, 1),
    (1, 0),
]

directions = [
    (0, 0),
    (-1,-1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
]

class Environment:
    def __init__(self, N, M, t, dp, bp, kidn, agent=None):
        self.N = N
        self.M = M
        self.t = t
        self.agent = agent
        self.env = []
        self.corrals = [ Corral() for _ in range(kidn) ]
        self.kids = [ Kid() for _ in range(kidn) ]
        self.obstacles = [ Obstacle() for _  in range(int( (bp*N*M)/100 )) ]
        self.dirty = int( (dp*N*M)/100 )

        self.reset()

    def reset(self):
        self.env = [ [ Cell(i, j) for j in range(self.M) ] for i in range(self.N) ]
        cells = [ (r, c) for r in range(self.N) for c in range(self.M) ]
        rnd.shuffle(cells)

        x, y = rnd_choice(cells)
        for corral in self.corrals: 
            self.env[x][y].set_obj(corral)
            try:
                x, y = rnd_choice(cells, pred= lambda z: z in self.adj((x, y)))
            except:
                self.reset()
                return

        if self.agent:
            x, y = rnd_choice(cells)
            self.env[x][y].set_agent(self.agent)
        else:
            self.agent = rnd_choice(cells)

        for obj in self.kids + self.obstacles:
            x, y = rnd_choice(cells)
            self.env[x][y].set_obj(obj)

        for _ in range(self.dirty):
            x, y = rnd_choice(cells)
            self.env[x][y].dirty = True

    def next(self):
        def can_move_obstacle(x, y, dir):
            bx, by = x + dir[0], y + dir[1]
            if not self.is_inside(bx, by):
                return False
            
            if self.env[bx][by].is_empty or (isinstance(self.env[bx][by].obj, Obstacle) and can_move_obstacle(bx, by, dir)):
                blk = self.env[x][y].obj
                self.env[x][y].free_obj()
                self.env[bx][by].set_obj(blk)
                return True
            else:
                return False

        dirs = []

        for kid in self.kids:
            x = kid.x
            y = kid.y

            adjs = self.directions(x, y)
            pkid = list(filter(lambda z: isinstance(self.env[z[0]][z[1]].obj, Kid), adjs))
            empties = list(filter(lambda z: self.env[z[0]][z[1]].is_empty, adjs))
            count = len(pkid)
            new_trash = rnd.randint(0, (count * (count == 1) + 3 * (count == 2) + 6*(count >= 3)))
            
            dirs.append((empties, new_trash))

            nx, ny = rnd.choice(self.adj((x, y), not_stay=False))

            if x == nx and y == ny:
                continue

            if self.env[nx][ny].is_empty or (isinstance(self.env[nx][ny].obj, Obstacle) and can_move_obstacle(nx, ny, (nx - x, ny - y))):
                self.env[x][y].free_obj()
                self.env[nx][ny].set_obj(kid)
            else:
                pass

        for pos, cnt in dirs:
            for tx, ty in rnd_many(pos, cnt):
                if self.env[tx][ty].is_empty: 
                    self.env[tx][ty].dirty = True
                    self.dirty += 1

    def directions(self, x, y):
        adjs = []
        for d in directions:
            nx = x + d[0]
            ny = y + d[1]

            if self.is_inside(nx, ny):
                adjs.append((nx, ny))

        return adjs

    def adj(self, pos, pred=None, not_stay=True):
        adjs = []
        # print('pos=',pos)
        for d in directions[not_stay:]:
            x = pos[0] + d[0]
            y = pos[1] + d[1]
            if self.is_inside(x, y):
                adjs.append((x, y))
        if pred:
            adjs = list(filter(pred, adjs))
        return adjs

    def insert_agent(self, x, y, agent):
        self.env[x][y].set_agent(agent)
        self.agent = self.env[x][y].agent

    def set_rnd_agent(self, agent):
        x, y = self.agent
        self.insert_agent(x, y, agent)

    def move_agent(self, x, y):
        self.env[self.agent.x][self.agent.y].free_agent()
        self.insert_agent(x, y, self.agent)

    def remove_kid(self, kid):
        self.kids.remove(kid)

    def is_inside(self, x, y):
        return 0 <= x < self.N and 0 <= y < self.M

    def is_clean(self):
        return self.dirty == 0 and all(c.with_kid for c in self.corrals)
    
    def garbage_pc(self):
        return round((self.dirty / ((self.N * self.M) - len(self.corrals) - len(self.kids) - len(self.obstacles) - 1)), 2)

    def __str__(self):
        return '\n'.join(' '.join(str(self.env[i][j]) for j in range(self.M)) for i in range(self.N))

def gen_env(agent):
    N = rnd.randint(5, 12)
    M = rnd.randint(5, 12)
    t = rnd.randint(5, 8)
    dp = rnd.randint(15, 35)
    # print('dp ', dp)
    bp = rnd.randint(10, 15)
    kidn = rnd.randint(2, 6)

    return Environment(N, M, t, dp, bp, kidn, agent)