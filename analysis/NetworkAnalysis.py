import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl

# Set up matplotlib configurations
mpl.rc('xtick', labelsize=14, color="#222222") 
mpl.rc('ytick', labelsize=14, color="#222222") 
mpl.rc('font', **{'family':'sans-serif','sans-serif':['Arial']})
mpl.rc('font', size=16)
mpl.rc('xtick.major', size=6, width=1)
mpl.rc('xtick.minor', size=3, width=1)
mpl.rc('ytick.major', size=6, width=1)
mpl.rc('ytick.minor', size=3, width=1)
mpl.rc('axes', linewidth=1, edgecolor="#222222", labelcolor="#222222")
mpl.rc('text', usetex=False, color="#222222")

# Read node and edge data from CSV files
nodes_df = pd.read_csv('new_nodes.csv')
edges_df = pd.read_csv('new_edges.csv')

# Create a new Graph
G = nx.Graph()

# Add nodes with attributes
for index, row in nodes_df.iterrows():
    G.add_node(row['id'], name=row['name'], popularity=row['popularity'], followers=row['followers'])

# Add edges with weights
for index, row in edges_df.iterrows():
    G.add_edge(row['source'], row['target'], weight=row['sum'])

# Compute degree centrality
degree_centrality = nx.degree_centrality(G)
# Filter out zero degree nodes and get a list of degrees for each node
degrees = [val for (node, val) in degree_centrality.items() if val > 0]

# Get the minimum and maximum degree
kmin = max(min(degrees), 1e-5)  # Prevents log(0) by ensuring kmin is > 0
kmax = max(degrees)

# Get 10 logarithmically spaced bins between kmin and kmax
# Ensure there's a range for log-spacing, otherwise set a default range
if kmin == kmax:
    bin_edges = np.logspace(np.log10(kmin), np.log10(kmin + 1), num=10)
else:
    bin_edges = np.logspace(np.log10(kmin), np.log10(kmax), num=10)

# Histogram the data into these bins
density, _ = np.histogram(degrees, bins=bin_edges, density=True)

# Create the figure
fig = plt.figure(figsize=(6,4))

# "x" should be midpoint (in log space) of each bin
log_be = np.log10(bin_edges)
x = 10**((log_be[1:] + log_be[:-1])/2)

# Plot the degree centrality
plt.loglog(x, density, marker='o', linestyle='none')
plt.xlabel(r"degree $k$", fontsize=16)
plt.ylabel(r"$P(k)$", fontsize=16)

# Remove right and top boundaries because they're considered ugly by some
ax = plt.gca()
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')

# Show the plot
plt.show()
