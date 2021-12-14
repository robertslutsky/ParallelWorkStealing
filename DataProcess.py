import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("./runs/all_12-14-21-21/data.csv")
df["avg_frac_active"] = (df["t_nodes"] / df["steps"]) / df["processors"]

# print(df)
for cluster in df["clusters"].unique():
    mask = (df["clusters"]==cluster)
    data1 = df[mask]
    for tree in data1["tree_type"].unique():
        mask = (data1["tree_type"]==tree)
        data2 = data1[mask]
        figure = plt.figure()
        axis = figure.add_subplot()
        axis.set_title(f"Active Processors When Exploring {tree} vs Num Processors for {cluster} Clusters")
        axis.set_ylabel("Average Fraction of Active Processors")
        axis.set_xlabel("Number of Processors")
        axis.set_xticks([4,8,16,32,64])
        axis.grid()
        for method in data2["method"].unique():
            mask = (data2["method"]==method) & (data2["method"]!="revenge")
            data3 = data2[mask]
            for steal_half in data3["steal_half"].unique():
                mask = data3["steal_half"]==steal_half
                # print(mask)
                data = data3[mask]
                h = "(half)" if steal_half else "(one)"
                axis.plot(data["processors"], data["avg_frac_active"], label=method + h, linestyle=None, marker='o')
                axis.legend()
        # handles, labels = axis.get_legend_handles_labels()
        # print(handles, labels)

plt.show()

# print(df)

# plt.plot(data["processors"], data["steps"])
# plt.plot(data["processors"], data["avg_frac_active"])
# plt.show()