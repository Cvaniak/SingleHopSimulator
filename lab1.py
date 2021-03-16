import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import random
import numpy as np
from collections import defaultdict
from math import log, e, prod, sqrt
#  -------------------------------------------------------------------------
# Matplot style taken from:
# https://towardsdatascience.com/cyberpunk-style-with-matplotlib-f47404c9d4c5
plt.style.use("dark_background")
for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
    plt.rcParams[param] = '0.9'  # very light grey
for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
    plt.rcParams[param] = '#212946'  # bluish dark grey
colors = [
    '#08F7FE',  # teal/cyan
    '#FE53BB',  # pink
    '#F5D300',  # yellow
    '#00ff41',  # matrix green
]
n_shades = 10
diff_linewidth = 0.6/10
alpha_value = 0.6 / n_shades
#  -------------------------------------------------------------------------

def draw_bar(a, b):
    plt.bar(a, b, color=colors, width=0.2)
    for i in range(n_shades):
        plt.bar(a, b,
                        width=0.2+(0.1+diff_linewidth*i),
                        color=colors,
                        alpha=alpha_value
                        )
    plt.xticks(a, a)


class Node():
    def __init__(self, index, nodes_number):
        self.index = index
        self.nodes_number = nodes_number
        self.last_vote = -1

    def vote(self, number):
        pass


class Node_scenario_2(Node):
    def __init__(self, index, nodes_number):
        super().__init__(index, nodes_number)

    def vote(self, number):
        self.last_vote = self.index if random.randint(1, self.nodes_number+1) == self.index else 0
        return self.last_vote


class Node_scenario_3(Node):
    def __init__(self, index, nodes_number):
        super().__init__(index, nodes_number)
        self.L = int(log(nodes_number, 2))
    
    def vote(self, number):
        self.last_vote = self.index if random.randint(1, 2**(number%self.L + 1)) == 1 else 0
        return self.last_vote


def create_nodes_scenario_2(nodes_number):
    return [Node_scenario_2(index, nodes_number) for index in range(1, nodes_number+1)]

def create_nodes_scenario_3(nodes_number, u_number):
    return [Node_scenario_3(index, u_number) for index in range(1, nodes_number+1)]


def exercise_2():
    loop_counter = 1000
    u_v = 1024

    nodes = create_nodes_scenario_2(u_v) 
    symulation(loop_counter, nodes, 1)
    nodes = create_nodes_scenario_3(u_v, u_v) 
    symulation(loop_counter, nodes[:2], 1)
    symulation(loop_counter, nodes[:u_v//2], 1)
    symulation(loop_counter, nodes, 1)

    plt.show() 

def exercise_3():
    loop_counter = 1000
    n = 1024
    nodes =  create_nodes_scenario_2(n)
    symulation(loop_counter, nodes, ex_3=1)

def exercise_4():
    min1 = 2
    max1 = -1
    nodes = create_nodes_scenario_3(1024, 1024) 
    for i in range(2,1024, 256):
        r = symulation(1000, nodes[:i], 0, ex_4=1)
        min1 = min(r, min1)
        max1 = max(r, max1)
    print(min1,max1)


def choose_lider(nodes):
    counter = 0
    while True:
        slot = len([node.last_vote for node in nodes if node.vote(counter)])
        if slot == 1:
            return counter + 1
        counter += 1


def symulation(number_of_experiments, nodes_list, plotting=0, ex_3=0, ex_4=0):
    print((f"Symulation for {number_of_experiments:5} tries"
            f", type of node is {type(nodes_list[0]).__name__}"
            f", with {len(nodes_list):5} nodes, plotting is {plotting}"
            f", ex_3 is {ex_3} and ex_4 is {ex_4}"
            ))
    lider_slot = defaultdict(int)

    for i in range(number_of_experiments):
       lider_slot[choose_lider(nodes_list)] += 1 

    if plotting:
        lider_slot = dict(sorted(lider_slot.items(), key=lambda item: item[0]))
        plt.figure()
        draw_bar(list(lider_slot.keys()), list(lider_slot.values()))
        
    if ex_3:
        expected = sum([v*k for k,v in lider_slot.items()])/number_of_experiments
        variance = sqrt(sum([(expected - v*k/number_of_experiments)**2
                    for k,v in lider_slot.items()])/(number_of_experiments-1))
        print(f"Expected value: {expected} , Variance value: {variance}")

    if ex_4:
        g = prod([1-(v)/number_of_experiments for k, v in lider_slot.items()])
        print(f"{len(nodes_list)} ")
        lider_slot = dict(sorted(lider_slot.items(), key=lambda item: item[0]))
        print(1-g)
        return 1-g 


if __name__ == '__main__':
    exercise_2()
    exercise_3()
    exercise_4()

