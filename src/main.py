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
        results = []
        for i in range(10):
            results.append([])
            current_agent = deepcopy(agent)
            current_env = deepcopy(envs[i])
            current_env.set_rnd_agent(current_agent)
            copy_env = deepcopy(current_env)
            stats = { "Fired": 0, "Clean": 0, "Garbage": []}
            for j in range(30):
                for turn in range(current_env.t*100):
                    current_env.agent.next(current_env)
                    current_env.next()
                    if (turn + 1) % current_env.t == 0:
                        current_env.reset()
                    if current_env.garbage_pc() >= 0.6:
                        stats["Fired"] += 1
                        break
                    elif current_env.is_clean():
                        stats["Clean"] += 1
                        # print("Beak")
                        break
                stats["Garbage"].append(current_env.dirty)
                # print('RESULT:   Garbage: ', current_env.dirty)
                current_env = copy_env
            stats["Garbage"] = round(sum(stats["Garbage"])/len(stats["Garbage"]), 2)
            results[i] = stats
            print('----------------------------------------------------------')
            print("i: {} Env {}x{}\n".format(i, current_env.N, current_env.M))
            print("Turn time: {} Garbage: {}% Objects: {} Kids: {}\n".format(current_env.t, 100*current_env.garbage_pc(), len(current_env.obstacles), len(current_env.corrals)))
        print('--------Agent {}-----------'.format(agent.name))
        for i in range(10):
            print('Results env: {}'.format(i))
            print(results[i])
        print()

if __name__ == "__main__":
    start()