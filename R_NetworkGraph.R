library(tidyverse)
library(viridis)
library(patchwork)
library(hrbrthemes)
library(ggraph)
library(igraph)
library(networkD3)

# Define nodes
nodes <- data.frame(
  name = c("Paper 1", "Paper 2", "Paper 3", "Paper 4", "Paper 5", 
           "Yale", "Mass General Hospital", "Company X", "CDC", "MN DOH"),
  type = c("Project", "Project", "Project", "Project", "Project", 
           "Institution", "Institution", "Institution", "Institution", "Institution"),
  supercategory1 = c("BAA_2020_Yale", "BAA_2020_Yale", "BAA_2020_Yale", "BAA_2020_Broad", "BAA_2020_Broad",
                     "Academic", "Healthcare", "Industry", "Federal", "State PH"),
  supercategory2 = c("BAA", "BAA", "BAA", "BAA", "BAA", 
                     "Academic", "Healthcare", "Industry", "Federal", "State")
)

# Define edges
edges <- data.frame(
  from = c("Author 1", "Author 2", "Author 3", "Author 4", "Author 5", 
           "Author 6", "Author 7", "Author 8", "Author 9", "Author 10", 
           "Author 11", "Author 12", "Author 13", "Author 14", "Author 15", 
           "Author 16", "Author 17", "Author 18", "Author 19", "Author 20", 
           "Author 20", "Author 21"),
  to = c("Institution 1", "Institution 1", "Institution 2", "Institution 3", "Institution 4", 
         "Institution 4", "Institution 4", "Institution 5", "Institution 6", "Institution 7", 
         "Institution 8", "Institution 9", "Institution 9", "Institution 10", "Institution 10", 
         "Institution 10", "Institution 11", "Institution 12", "Institution 13", "Institution 14", 
         "Institution 15", "Institution 16"),
  publication = c("Paper 1", "Paper 1", "Paper 1", "Paper 1", "Paper 2", 
                  "Paper 2", "Paper 2", "Paper 2", "Paper 2", "Paper 3", 
                  "Paper 3", "Paper 3", "Paper 4", "PGCOE_VA", "PGCOE_VA", 
                  "PGCOE_VA", "PGCOE_WA", "PGCOE_WA", "PGCOE_WA", "PGCOE_WA", 
                  "PGCOE_WA", "PGCOE_WA")
)

# Create the graph
g <- graph_from_data_frame(edges, vertices = nodes, directed = FALSE)

# Plot the graph using ggraph
ggraph(g, layout = "fr") +
  geom_edge_link(aes(color = publication), alpha = 0.8) +
  geom_node_point(aes(color = type), size = 5) +
  geom_node_text(aes(label = name), repel = TRUE, size = 3) +
  scale_color_viridis(discrete = TRUE) +
  theme_graph() +
  theme(legend.position = "bottom")

