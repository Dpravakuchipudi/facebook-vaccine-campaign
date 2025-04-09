# ----------------------------------------
# 06_network_deepdive.py
# Step 5+: Extended Network Analysis & Visualization
# ----------------------------------------

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import os
import random
from scipy.stats import ttest_ind
from networkx.algorithms.community import greedy_modularity_communities

# ----------------------------------------
# Setup
# ----------------------------------------

# Create outputs folder
os.makedirs("outputs", exist_ok=True)

# Load merged participant data
merged = pd.read_csv("outputs/merged_full_data.csv")
n = len(merged)

# ----------------------------------------
# Build Social Network (Erdős–Rényi Model)
# ----------------------------------------

# Simulate 1% chance of connection between any two participants
G = nx.erdos_renyi_graph(n=n, p=0.01, seed=42)

# Map node labels to participant IDs
id_map = dict(zip(range(n), merged["participant_id"]))
G = nx.relabel_nodes(G, id_map)

# ----------------------------------------
# Assign Node Attributes
# ----------------------------------------

# Attach participant attributes to graph nodes
nx.set_node_attributes(G, merged.set_index("participant_id")["vaccine_uptake"].to_dict(), "vaccine_uptake")
nx.set_node_attributes(G, merged.set_index("participant_id")["ad_group"].to_dict(), "ad_group")

# ----------------------------------------
# Degree Centrality
# ----------------------------------------

# Compute centrality and merge into data
centrality = nx.degree_centrality(G)
merged["degree_centrality"] = merged["participant_id"].map(centrality)
merged.to_csv("outputs/merged_with_centrality.csv", index=False)

# ----------------------------------------
# Boxplot: Centrality vs Vaccine Uptake
# ----------------------------------------

plt.figure(figsize=(8, 5))
sns.boxplot(data=merged, x="vaccine_uptake", y="degree_centrality", palette="Set2")
plt.title("Network Centrality vs Vaccine Uptake")
plt.xlabel("Vaccine Uptake (0 = No, 1 = Yes)")
plt.ylabel("Degree Centrality")
plt.tight_layout()
plt.savefig("outputs/network_centrality_vs_uptake.png")
plt.close()

# ----------------------------------------
# T-test: Are central participants more likely vaccinated?
# ----------------------------------------

group_0 = merged[merged["vaccine_uptake"] == 0]["degree_centrality"]
group_1 = merged[merged["vaccine_uptake"] == 1]["degree_centrality"]
t_stat, p_val = ttest_ind(group_1, group_0)

with open("outputs/network_centrality_ttest.txt", "w") as f:
    f.write(f"T-test on centrality:\nt = {t_stat:.4f}, p = {p_val:.4f}\n")

print(f"\n📊 T-test on centrality:\nt = {t_stat:.4f}, p = {p_val:.4f}")

# ----------------------------------------
# Community Detection using Greedy Modularity
# ----------------------------------------

print("\n🔍 Detecting communities using modularity optimization...")
communities = list(greedy_modularity_communities(G))
community_map = {node: i for i, group in enumerate(communities) for node in group}
merged["community_id"] = merged["participant_id"].map(community_map)
merged.to_csv("outputs/merged_with_communities.csv", index=False)

print(f"📎 Detected {len(communities)} communities.")

# ----------------------------------------
# Histogram: Vaccine Uptake by Community
# ----------------------------------------

comm_summary = merged.groupby("community_id")["vaccine_uptake"].mean().reset_index()

plt.figure(figsize=(10, 5))
sns.histplot(comm_summary["vaccine_uptake"], bins=20, kde=True)
plt.title("Distribution of Vaccine Uptake by Community")
plt.xlabel("Average Uptake Rate per Community")
plt.ylabel("Number of Communities")
plt.tight_layout()
plt.savefig("outputs/vaccine_uptake_by_community.png")
plt.close()

# ----------------------------------------
# Sample Network Visualization
# ----------------------------------------

# Draw a sample of 100 nodes from the network
sample_nodes = random.sample(list(G.nodes()), 100)
subG = G.subgraph(sample_nodes)

# Color nodes by vaccine uptake
colors = ["skyblue" if G.nodes[n]["vaccine_uptake"] == 1 else "lightgray" for n in subG.nodes()]

plt.figure(figsize=(10, 8))
nx.draw(subG, with_labels=False, node_size=50, node_color=colors)
plt.title("Vaccination Uptake in Random Subnetwork")
plt.tight_layout()
plt.savefig("outputs/network_graph_sample.png")
plt.close()

# ----------------------------------------
# Done
# ----------------------------------------

print("\n✅ Full network analysis complete.")
print("Check your 'outputs/' folder for:")
print("• Centrality boxplot")
print("• T-test results")
print("• Community uptake histogram")
print("• Subnetwork visualization")
