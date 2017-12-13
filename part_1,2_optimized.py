# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 19:43:33 2017

@author: Vamsi Krishna Varma Gunturi
"""

import itertools
import networkx as nx
import json
#import matplotlib.pyplot as plt
data = json.load(open('reduced_dblp.json'))


#print(len(data))

#POINT 1

G = nx.Graph()
publications_dict = {}
conferences_list = []
authors_list = []
inverted_index = {}

conferences_map = {}
publications_map = {}
authors_map = {}

for i in range(len(data)):
    cur_conference = data[i]
    
    cur_conference_id = cur_conference['id_conference_int']
    cur_conference_name = cur_conference['id_conference'] 
    
    cur_publication_id = cur_conference['id_publication_int']
    cur_publication_name = cur_conference['id_publication']
    
    publications_dict[cur_publication_id]={}
    publications_dict[cur_publication_id]['authors']=[]
    
    #Build Conferences Map => Conference Name to Conference ID
    if cur_conference_name not in conferences_map.keys():
        conferences_map[cur_conference_name] = []
        conferences_map[cur_conference_name].append(cur_conference_id)
        conferences_map[cur_conference_name].append([])
    
    #Build Publications Map => Publication Name to Publication ID
    if cur_publication_name not in publications_map.keys():
        publications_map[cur_publication_name] = cur_publication_id
    
    cur_authors = []
    for author in cur_conference['authors']:
        
        cur_author_id = author['author_id']
        cur_author_name = author['author']
        
        cur_authors.append(cur_author_id)
        
        if cur_author_id not in inverted_index.keys():
            inverted_index[cur_author_id]=[]
            inverted_index[cur_author_id].append(cur_publication_id)
        else:
            inverted_index[cur_author_id].append(cur_publication_id)
            
        #Build Authors map => Author Name to Author ID
        if cur_author_name not in authors_map.keys():
            authors_map[cur_author_name] = cur_author_id        
    
    
    #Build Conferences To Authors Map => Connference Name to Authors
    if cur_conference_name in conferences_map.keys():
        conferences_map[cur_conference_name][1].extend(cur_authors)
    
    #Updating the graph    
    G.add_nodes_from(cur_authors)
    edges = itertools.combinations(cur_authors, 2)
    G.add_edges_from(edges)
    
    authors_list += cur_authors
    
    publications_dict[cur_publication_id]['id_conference_int'] = cur_conference_id
    conferences_list.append(cur_conference_id)

#Removing the duplicate entries
conferences_list = list(set(conferences_list))
authors_list = list(set(authors_list))   


for conf in conferences_map:
    conferences_map[conf][1] = list(set(conferences_map[conf][1]))

#nx.draw(G)

#Assigning weights to the edges
for author in authors_list:
    b= set(inverted_index[author])
    for author_edge in G.edge[author]:
        G[author][author_edge] = {}
        a = set(inverted_index[author_edge])
        num = list(set(a.intersection(b)))
        den = list(set(a.union(b))) 
        
        G[author][author_edge]['weight']= 1-( len(num) / len(den) )   
       
nx.draw(G)

conference_name = 'conf/pkdd/2011-1'
conf_details = conferences_map[conference_name]
conference_id = conf_details[0] 
conf_authors = conf_details[1]

k = G.subgraph(conf_authors)

degree=nx.degree_centrality(k)

closeness=nx.closeness_centrality(k)

betweenness=nx.betweenness_centrality(k)

print('Some centralities measures for nodes selected in our subgraph!')

for author in conf_authors:
    print('author_id: ' + str(author))
    print('')
    print('degree centrality: ' +str(degree[author]))
    print('closeness centrality: ' +str(closeness[author]))
    print('betweenness centrality: ' +str(betweenness[author]))
    print('')

#nx.draw(k)
#nx.info(k)
    
# PART 2- b
### Point 2 b
author_id=255206
d=1 #if d>1 doesn't work
#path=nx.single_source_shortest_path_length(G=G,source= author_id,cutoff=d)
kk=nx.ego_graph(G=G,n= author_id, radius= d, undirected= True, center= True)

nx.draw(kk)
