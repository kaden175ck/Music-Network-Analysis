import pandas as pd

# Read CSV file
data = pd.read_csv('nodes_-_Copy.csv')

# Filtering condition: popularity >= 50 AND followers >= 1000
filtered_data = data[(data['popularity'] >= 50) & (data['followers'] >= 1000)]

# Delete rows where any field is blank
filtered_data = filtered_data.dropna()

# In the 'name' column, keep only names in English, delete other strange fields
filtered_data = filtered_data[filtered_data['name'].str.match(r'^[A-Za-z\s]+$')]

# Save the filtered results to a new CSV file
filtered_data.to_csv('new_nodes.csv', index=False)

print("The filtered results have been saved to the 'new_nodes.csv' file.")