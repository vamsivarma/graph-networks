Function in graph_index_module :
In graph_index_module there are 2 class
1) Graph_index
2) Graph_operations

In Graph_index there are several functions to create and manipulate data:

1.1) fetch_data
this function save json database into the variable data
1.2) build_graph
Here we create our graph and 2 usefull tools: Conference Map that link conference name to conference id
and publication map that link publication name with publication id
1.3)remove_duplicates
In this function we clean our variables removing duplicates
1.4)remove_unreachable_nodes that remove nodes without links
1.5) create_indexes
In this function we build the Weights for our edges.

In Graph_operations there are:
2.1) calculate_centralities
In this functions we analyze the subgraph induced by conference. 
2.2) calculate_subgraph
Here given in input an author and an integer we draw the subgraph induced by the nodes that
have hop distance at most equal to d with the input author.
2.3) node_hop_neighbors
function that returns the nodes at hop distance d
2.4) shortest_path_advanced
In this fucntion we calculate the shortest path between 2 authors
2.5) find_path_given_author 
retunr path given 2 authors
2.6)update_the_neighbour_nodes riga 383 da continuare
