from environment import *
from agents import *
import random as rnd
from copy import deepcopy

def start():
    envs = []
    agents = [ Reactive(), Proactive()]
    for _ in range(10):
        envs.append(gen_env(None))

    for agent in agents:
        print('Test {}\n'.format(agent.name))
        results = []*10
        for i in range(10):
            current_agent = deepcopy(agent)
            current_env = deepcopy(envs[i])
            current_env.set_rnd_agent(current_agent)
            stats = { "Fired": 0, "Clean": 0, "Garbage": 0}
            for j in range(30):
                for turn in range(current_env.t*100):
                    current_env.agent.next(env)
                    current_env.next()
                    if (turn + 1) % env.t == 0:
                        env.reset()
                    if env.garbage_pc() >= 0.6:
                        d["Fired"] += 1
                        break
                    elif env.is_clean():
                        d["Clean"] += 1
                        break
            d["Garbage"] = round(sum(d["Garbage"])/len(d["Garbage"]), 2)
            results[i] = stats
            print('----------------------------------------------------------')
            print("i: {} Env {}x{}\n".format(i, current_env.N, current_env.M))
            print("Turn time: {} Garbage: {}% Objects: {} Kids: {}\n".format(current_env.t, current_env.garbage_pc(), current_env.objs, current_env.corrals))
        print('--------Agent {}-----------'.format(agent.name))
        for i in range(10):
            print('Results env: {}'.format(i))
            print(results[i])

if __name__ == "__main__":
    start()