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

def run_tests(num_iterations, tree_generator_objs, systems, min_tree_depth, min_tree_nodes):
    blockPrint()
    data = []
    for i in range(num_iterations):
        for tree_generator_obj in tree_generator_objs:
            tree = tree_generator_obj.generate_tree()
            depth, num_nodes = tree_count(tree.root)

            # generate tree until up to standards
            while depth < min_tree_depth or num_nodes < min_tree_nodes:
                tree = tree_generator_obj.generate_tree()
                depth, num_nodes = tree_count(tree.root)

            for system in systems:
                # get the exec dag
                execution_dag_start = generate_dag(tree.root)

                # run the dag on the system
                steps, steal_attempts, successful_steals = system.run(execution_dag_start)
                data.append((i, str(tree_generator_obj), depth, num_nodes, tree_to_string(tree.root), str(system), steps, steal_attempts, successful_steals))

    df = pd.DataFrame(data, columns=["iteration", "tree_type", "t_height", "t_nodes", "tree", "system_type", "steps", "steal_attempts", "successful_steals"])
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

tree_gen_objs = [BinomialTreeGenerator(3, 0.2), GeometricTreeGenerator(2, 3)]
systems = [System(num_processors=100, method='random'), System(num_processors=4, method='right')]

df = run_tests(100, tree_gen_objs, systems, 3, 0)
save_results(df, "test")