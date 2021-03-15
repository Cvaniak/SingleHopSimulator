import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import random
import numpy as np
from collections import defaultdict
from math import log, e
#  -------------------------------------------------------------------------
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
HISTO_COUNTER = 1
# df = pd.DataFrame({'A': [1, 3, 9, 5, 2, 1, 1],
#                    'B': [4, 5, 5, 7, 9, 8, 6]})
# fig, ax = plt.subplots()
# df.plot(marker='o', color=colors, ax=ax)
# Redraw the data with low alpha and slighty increased linewidth:

# for n in range(1, n_shades+1):
#     df.plot(marker='o',
#             linewidth=2+(diff_linewidth*n),
#             alpha=alpha_value,
#             legend=False,
#             ax=ax,
#             color=colors)
# # Color the areas below the lines:
# for column, color in zip(df, colors):
#     ax.fill_between(x=df.index,
#                     y1=df[column].values,
#                     y2=[0] * len(df),
#                     color=color,
#                     alpha=0.1)
# ax.grid(color='#2A3459')
# ax.set_xlim([ax.get_xlim()[0] - 0.2, ax.get_xlim()[1] + 0.2])  # to not have the markers cut off
# ax.set_ylim(0)
# plt.show()
#  -------------------------------------------------------------------------

def draw_bar(fig, ax, a, b):
    plt.bar(a, b, color=colors, width=0.2)
    for i in range(n_shades):
        plt.bar(a, b,
                        width=0.2+(0.1+diff_linewidth*i),
                        color=colors,
                        alpha=alpha_value
                        )
    plt.xticks(a, a)
    # xpoints = np.array([0, 6])
    # ypoints = np.array(range())
    # ax.set_xlim([ax.get_xlim()[0] - 0.2, ax.get_xlim()[1] + 0.2])  # to not have the markers cut off
    # ax.set_ylim(0)


class Node():

    def __init__(self, index, nodes_number):
        self.index = index
        self.nodes_number = nodes_number
        self.last_vote = -1

    def vote(self):
        self.last_vote = self.index if random.randint(1, self.nodes_number+1) == self.index else 0
        return self.last_vote


class NodeSc2(Node):
    def __init__(self, index, nodes_number):
        super().__init__(index, nodes_number)
        self.L = log(nodes_number, 2)
        self.round = 1
    
    def vote(self):
        if self.round > self.L:
            self.round = 1
        
        self.last_vote = self.index if random.randint(1, 2**self.round) == self.round//2 else 0
        return self.last_vote

def create_nodes(nodes_number):
    return [Node(index, nodes_number) for index in range(1, nodes_number+1)]
    
def create_nodes_sc2(nodes_number, u_number):
    return [Node(index, u_number) for index in range(1, nodes_number+1)]

def main(loop_counter, nodes, nodes_number=100, is_plt=0):
    global HISTO_COUNTER
    counter = 0
    last_lider = 0
    d = defaultdict(int)
    d1 = defaultdict(int)
    d2 = []

    while counter < loop_counter:
        counter += 1 
        slot = [node.last_vote for node in nodes if node.vote()]
        if len(slot) == 1:
            # print(f"{slot[0]} \n", end="")
            d[last_lider] += 1
            d1[counter] = last_lider
            d2.append(last_lider)
            last_lider = 1
        else:
            # print(f"{'|' if len(slot) else '-'}{slot}", end="")
            d1[counter] = 0
            last_lider += 1

    elog = []
    # for i in range(max(d.keys())):
    #     # elog.append(e*log(i+1))
    #     if not d[i]:
    #         d[i] = 0

    if is_plt:
        d = dict(sorted(d.items(), key=lambda item: item[0]))
        plt.subplot(int(f'42{HISTO_COUNTER}'))
        draw_bar(None, None, list(d.keys()), list(d.values()))
        HISTO_COUNTER += 1
        plt.subplot(int(f'42{HISTO_COUNTER}'))
        HISTO_COUNTER += 1
        plt.bar(range(len(d1)), list(d1.values()), color=colors)

    temp = sum([k*v for k,v in d.items()])
    print(f"{temp} - {sum(d.values())}")
    print(temp/sum(d.values()))



if __name__ == '__main__':
    # random.seed(1234)
    loop_counter = 1000
    # nodes_number = input() or 100
    nodes = create_nodes(100) 
    main(int(loop_counter), nodes, 100, 1)
    nodes = create_nodes_sc2(2, 100) 
    main(int(loop_counter), nodes, 100, 1)
    nodes = create_nodes_sc2(50, 100) 
    main(int(loop_counter), nodes, 100, 1)
    nodes = create_nodes_sc2(100, 100) 
    main(int(loop_counter), nodes, 100, 1)
    plt.show()

    for i in range(0,20, 4):
        for j in range(i, 20, 4):
            nodes = create_nodes_sc2(i, j) 
            main(int(loop_counter), nodes, j)



