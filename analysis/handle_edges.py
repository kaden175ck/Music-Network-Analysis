import pandas as pd

# Read the files edges_v1.csv and new_nodes.csv
edges_df = pd.read_csv('edges_v1.csv')
new_nodes_df = pd.read_csv('new_nodes.csv')

# Convert the id column from new_nodes.csv file to a set
valid_ids = set(new_nodes_df['id'])

# Filter the data in edges_df where both source and target columns are in the valid_ids set
filtered_data = edges_df[(edges_df['source'].isin(valid_ids)) & (edges_df['target'].isin(valid_ids))]

# Write the filtered data to a new CSV file
filtered_data.to_csv('new_edges.csv', index=False)

print("The filtered data has been saved to the new_edges.csv file")
