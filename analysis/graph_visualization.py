import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import collections


# Load the nodes and edges data
nodes = pd.read_csv('newnodes.csv')
edges = pd.read_csv('edges.csv')

# Initialize an empty graph
G = nx.Graph()

# Add nodes to the graph
for index, row in nodes.iterrows():
    G.add_node(row['id'], name=row['name'], popularity=row['popularity'], followers=row['followers'])

# Add edges to the graph
for index, row in edges.iterrows():
    G.add_edge(row['id_1'], row['id_2'])
# Calculate basic statistics
num_nodes = G.number_of_nodes()
num_edges = G.number_of_edges()
num_connected_components = nx.number_connected_components(G)
degree_sequence = sorted([d for n, d in G.degree()], reverse=True)
degreeCount = collections.Counter(degree_sequence)
deg, cnt = zip(*degreeCount.items())
avg_clustering_coefficient = nx.average_clustering(G)

# Print basic statistics
print(f"Number of nodes: {num_nodes}")
print(f"Number of edges: {num_edges}")
print(f"Number of connected components: {num_connected_components}")
print(f"Degree distribution: {degreeCount}")
print(f"Average clustering coefficient: {avg_clustering_coefficient}")