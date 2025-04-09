# ----------------------------------------
# 05_network_analysis.py
# Step 5: Simulated Network Analysis
# ----------------------------------------

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ----------------------------------------
# Setup
# ----------------------------------------

# Ensure output folder exists
os.makedirs("outputs", exist_ok=True)

# Load merged participant dataset
merged = pd.read_csv("outputs/merged_full_data.csv")
n_participants = len(merged)

# ----------------------------------------
# Simulate Social Network (Erdős–Rényi Model)
# ----------------------------------------

# Generate random graph with ~1% connection probability
G = nx.erdos_renyi_graph(n=n_participants, p=0.01, seed=42)

# Map numeric nodes to participant IDs
id_map = dict(zip(range(n_participants), merged["participant_id"]))
G = nx.relabel_nodes(G, id_map)

# ----------------------------------------
# Add Participant Attributes to Graph
# ----------------------------------------

# Assign vaccine uptake and ad group as node attributes
nx.set_node_attributes(G, merged.set_index("participant_id")["vaccine_uptake"].to_dict(), "vaccine_uptake")
nx.set_node_attributes(G, merged.set_index("participant_id")["ad_group"].to_dict(), "ad_group")

# ----------------------------------------
# Compute Degree Centrality
# ----------------------------------------

# Calculate degree centrality and attach to DataFrame
centrality_scores = nx.degree_centrality(G)
merged["degree_centrality"] = merged["participant_id"].map(centrality_scores)

# Save updated merged dataset
merged.to_csv("outputs/merged_with_centrality.csv", index=False)

# ----------------------------------------
# Visualize Centrality vs Vaccine Uptake
# ----------------------------------------

plt.figure(figsize=(8, 5))
sns.boxplot(data=merged, x="vaccine_uptake", y="degree_centrality", palette="Set2")
plt.title("Network Centrality vs Vaccine Uptake")
plt.xlabel("Vaccine Uptake (0 = No, 1 = Yes)")
plt.ylabel("Degree Centrality")
plt.tight_layout()
plt.savefig("outputs/network_centrality_vs_uptake.png")
plt.close()

print("✅ Network analysis complete. Results saved in 'outputs/' folder.")
