# Import necessary libraries
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load the nodes data from newnodes.csv
nodes = pd.read_csv('newnodes.csv')

# Initialize an empty graph
G = nx.Graph()

# Add nodes with attributes to the graph
for index, row in nodes.iterrows():
    G.add_node(row['id'], 
               name=row['name'], 
               popularity=row['popularity'], 
               followers=row['followers'])

# As an example, this part would visualize the graph with nodes only
# Since we don't have edge data, this will not show connections between nodes
pos = nx.spring_layout(G)  # Positions for all nodes

# Drawing nodes and using 'popularity' to define the node size for visualization purposes
node_sizes = [100 * G.nodes[node]['popularity'] for node in G.nodes]
nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color='blue', alpha=0.6)

# Drawing labels
labels = nx.get_node_attributes(G, 'name')
nx.draw_networkx_labels(G, pos, labels, font_size=8)

plt.title('Graph Visualization based on newnodes.csv')
plt.axis('off')  # Turn off the axis
plt.show()
