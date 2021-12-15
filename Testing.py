from TreeGen import *
from System import System
from typing import Type
import pandas as pd
import os, sys
from pathlib import Path
import sys, os
from datetime import datetime

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')
# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

def run_tests(num_iterations, trees, systems):
    blockPrint()
    data = []
    for i in range(num_iterations):
        for tree in trees:
            depth, num_nodes = tree_count(tree.root)

            for system in systems:
                # get the exec dag
                execution_dag_start = generate_dag(tree.root)

                # run the dag on the system
                steps, steal_attempts, successful_steals = system.run(execution_dag_start)
                data.append((i, system.num_clusters, tree.name, depth, num_nodes, tree_to_string(tree.root), system.num_processors, system.method, system.steal_half, steps, steal_attempts, successful_steals))

    df = pd.DataFrame(data, columns=["iteration", "clusters", "tree_type", "t_height", "t_nodes", "tree", "processors", "method", "steal_half", "steps", "steal_attempts", "successful_steals"])
    enablePrint()
    return df

def tree_to_string(tree_root):
    # TODO
    return "idk"

def get_date_time():
    dateTimeObj = datetime.now()
    return str(dateTimeObj.month) + "-" + str(dateTimeObj.day) + "-" + str((dateTimeObj.hour-5)%24) + "-" + str(dateTimeObj.minute)

def save_results(df: pd.DataFrame, name):
    path = os.path.join("runs", name + "_" + get_date_time())
    Path(path).mkdir(parents=True, exist_ok=True)
    data_file = os.path.join(path, "data.csv")
    df.to_csv(data_file, index=False)
    print("saved results to", data_file)

# tree_gen_objs = [BinomialTreeGenerator(3, 0.2), GeometricTreeGenerator(2, 3)]
# systems = [System(num_processors=100, method='random'), System(num_processors=4, method='right')]

# df = run_tests(100, tree_gen_objs, systems, 3, 0)
# save_results(df, "test")

# max_index = None
# max_count = 0
# for i in range(1000, 10000):
#     # print("i", i)
#     random.seed(i)
#     btGen = BinomialTreeGenerator(2, 0.49999)
#     # bt2 = btGen.generate_tree()
#     try:
#         bt1 = btGen.generate_tree()
#         depth, count = tree_count(bt1.root)
#     except:
#         pass
#     if count > max_count:
#         max_index = i
#         max_count = count
#     # print("bt2 stats", tree_count(bt2.root))
# print(max_index, max_count)

random.seed(7)
btGen = BinomialTreeGenerator(2, 0.499)
bt1 = btGen.generate_tree("BT1")
print("bt1 stats", tree_count(bt1.root))

random.seed(3077)
btGen = BinomialTreeGenerator(2, 0.49999)
bt2 = btGen.generate_tree("BT2")
print("bt2 stats", tree_count(bt2.root))

trees = [bt1, bt2]

systems = []
for np in [4, 8, 16, 32, 64]:
    for steal_half in [True, False]:
        # 1 cluster tests
        for policy in ["random", "revenge", "right", "push_stack"]:
            systems.append(System(num_processors=np, method=policy, num_clusters=1, steal_half=steal_half))

        # 2 cluster tests
        for policy in ["random", "revenge", "random_within_cluster_small_crossover", "push_stack"]:
            systems.append(System(num_processors=np, method=policy, num_clusters=2, steal_half=steal_half))

df = run_tests(1, trees, systems)
save_results(df, "all")