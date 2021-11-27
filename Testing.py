from TreeGen import *
from System import System
from typing import Type
import pandas as pd

def run_tests(num_iterations, tree_generator_objs, systems, min_tree_depth, min_tree_nodes):
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
                data.append((i, str(tree_generator_obj), tree_to_string(tree.root), str(system), steps, steal_attempts, successful_steals))

    df = pd.DataFrame(data, columns=["iteration", "tree_type", "tree", "system_type", "steps", "steal_attempts", "successful_steals"])
    return df

def tree_to_string(tree_root):
    # TODO
    return "idk"


tree_gen_objs = [BinomialTreeGenerator(3, 0.2), GeometricTreeGenerator(2, 3)]
systems = [System(num_processors=4, method='random'), System(num_processors=4, method='right')]

df = run_tests(3, tree_gen_objs, systems, 3, 0)
print(df)