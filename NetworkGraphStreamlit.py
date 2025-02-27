import streamlit as st
import networkx as nx
from pyvis.network import Network
import pandas as pd
import tempfile

# Sample data
nodes_data = {
    'name': ["Paper 1", "Paper 2", "Paper 3", "Paper 4", "Paper 5", 
             "Yale", "Mass General Hospital", "Company X", "CDC", "MN DOH"],
    'type': ["Project", "Project", "Project", "Project", "Project", 
             "Institution", "Institution", "Institution", "Institution", "Institution"],
    'supercategory1': ["BAA_2020_Yale", "BAA_2020_Yale", "BAA_2020_Yale", "BAA_2020_Broad", "BAA_2020_Broad",
                       "Academic", "Healthcare", "Industry", "Federal", "State PH"],
    'supercategory2': ["BAA", "BAA", "BAA", "BAA", "BAA", 
                       "Academic", "Healthcare", "Industry", "Federal", "State"]
}

edges_data = {
    'from': ["Author 1", "Author 2", "Author 3", "Author 4", "Author 5", 
             "Author 6", "Author 7", "Author 8", "Author 9", "Author 10", 
             "Author 11", "Author 12", "Author 13", "Author 14", "Author 15", 
             "Author 16", "Author 17", "Author 18", "Author 19", "Author 20", 
             "Author 20", "Author 21"],
    'to': ["Institution 1", "Institution 1", "Institution 2", "Institution 3", "Institution 4", 
           "Institution 4", "Institution 4", "Institution 5", "Institution 6", "Institution 7", 
           "Institution 8", "Institution 9", "Institution 9", "Institution 10", "Institution 10", 
           "Institution 10", "Institution 11", "Institution 12", "Institution 13", "Institution 14", 
           "Institution 15", "Institution 16"],
    'publication': ["Paper 1", "Paper 1", "Paper 1", "Paper 1", "Paper 2", 
                    "Paper 2", "Paper 2", "Paper 2", "Paper 2", "Paper 3", 
                    "Paper 3", "Paper 3", "Paper 4", "PGCOE_VA", "PGCOE_VA", 
                    "PGCOE_VA", "PGCOE_WA", "PGCOE_WA", "PGCOE_WA", "PGCOE_WA", 
                    "PGCOE_WA", "PGCOE_WA"]
}

# Create a pandas DataFrame from the data
nodes_df = pd.DataFrame(nodes_data)
edges_df = pd.DataFrame(edges_data)

# Create a NetworkX graph
G = nx.Graph()
for index, row in nodes_df.iterrows():
    G.add_node(row['name'], type=row['type'], supercategory1=row['supercategory1'], supercategory2=row['supercategory2'])
for index, row in edges_df.iterrows():
    G.add_edge(row['from'], row['to'], publication=row['publication'])

# Create a PyVis network
net = Network(notebook=True)
net.from_nx(G)

# Save to temporary HTML file
with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
    net.save_graph(tmp_file.name)
    tmp_file.close()

# Read the HTML file
with open(tmp_file.name, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Streamlit app
st.title("Interactive Network Graph")
st.components.v1.html(html_content, height=600)
