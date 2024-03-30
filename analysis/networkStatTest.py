import pandas as pd
import networkx as nx

# Load data from CSV files
edges_df = pd.read_csv('new_edges.csv')
nodes_df = pd.read_csv('new_nodes.csv')

# Create the graph
G = nx.Graph()

# Mapping from id to name
id_to_name = {}

# Add nodes with attributes
for _, row in nodes_df.iterrows():
    G.add_node(row['id'], name=row['name'], popularity=row['popularity'], followers=row['followers'])
    id_to_name[row['id']] = row['name']

# Add edges
for _, row in edges_df.iterrows():
    G.add_edge(row['source'], row['target'], weight=row['weight'])

# Calculate centrality measures
degree_centrality = nx.degree_centrality(G)
betweenness_centrality = nx.betweenness_centrality(G, weight='weight')

# Prepare the data for output
# Convert centrality measures to DataFrame
centrality_df = pd.DataFrame({
    "Name": [id_to_name[node_id] for node_id in G.nodes()],
    "Degree Centrality": [degree_centrality[node_id] for node_id in G.nodes()],
    "Betweenness Centrality (normalized)": [betweenness_centrality[node_id] for node_id in G.nodes()]
})

# Write the complete centrality measures to a CSV file
centrality_df.to_csv('centrality_measures.csv', index=False)

# Sort and select the top 10 for Degree Centrality
top_10_degree = centrality_df.sort_values(by='Degree Centrality', ascending=False).head(10)
top_10_degree_file_path = 'top_10_degree_centrality.csv'
top_10_degree.to_csv(top_10_degree_file_path, index=False)

# Sort and select the top 10 for Betweenness Centrality
top_10_betweenness = centrality_df.sort_values(by='Betweenness Centrality (normalized)', ascending=False).head(10)
top_10_betweenness_file_path = 'top_10_betweenness_centrality.csv'
top_10_betweenness.to_csv(top_10_betweenness_file_path, index=False)


print("Top 10 Degree Centrality:")
print(top_10_degree, '\n')
print("Top 10 Betweenness Centrality:")
print(top_10_betweenness)
