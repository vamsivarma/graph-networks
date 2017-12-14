# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 19:43:33 2017

@author: Vamsi Krishna Varma Gunturi
"""

from collections import defaultdict
from heapq import *

import itertools
import networkx as nx
import json
#import matplotlib.pyplot as plt
data = json.load(open('reduced_dblp.json'))


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


#POINT 2.1

conference_name = 'conf/pkdd/2011-1' #'conf/acmdis/2010'
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

nx.draw(k)
#nx.info(k)
    
#POINT 2.2
    
author_name = "michel verleysen"
#author_name = "paulo costa"

author_id = authors_map[author_name]
d=1 #if d>1 doesn't work
#path=nx.single_source_shortest_path_length(G=G,source= author_id,cutoff=d)
kk=nx.ego_graph(G=G,n= author_id, radius= d, undirected= True, center= True)

nx.draw(kk)


#POINT 3.1

def shortest_path(G, start, end):
    
    dict1 = defaultdict(list)
    for author1 in authors_list:
        for author2 in G[author1].keys():
            dict1[author1].append((author2, G[author1][author2]['weight']))
    pathList = [[0,start,()]]
    seen = set()
    
    while pathList:
        (cost, vertex1, path) = heappop( pathList )
        if vertex1 not in seen:
            seen.add(vertex1)
            path = (vertex1, path)
            if vertex1 == end: 
                return (cost, path)
            for vertex2, weight in dict1[vertex1]:
                if vertex2 not in seen:
                    heappush(pathList, [cost+weight, vertex2, path])
                    
    pathList= list(pathList)
    
    return pathList



aris_id = authors_map["aris anagnostopoulos"]
#aris_id = authors_map["daniel hackenberg"]

author_name = "george brova"
#author_name = "damien djaouti"

author_id = authors_map[author_name]


try:

    path=shortest_path(G, author_id, aris_id)    

    if(len(path)):
        print(path)
    else:
        print('No path')

except nx.NetworkXNoPath:

    print('No path')


#POINT 3.2
group_nodes = [270587, 270585, 524503, 365179, 33951, 112985, 364898, 255487, 166813, 250148]
nodes_len = len(group_nodes)

#Build a 2 dimentional matrix based on number of vertexes
group_matrix = []
for node in group_nodes:
    
    node_list = []
    
    for i in range(nodes_len):    
        node_list.append(node)
    
    group_matrix.append(node_list)

for i in range(nodes_len):
    for j in range(i+1, nodes_len):
         
        s_p = shortest_path(G, group_nodes[i], group_nodes[j])
        
        if(len(s_p)):
            group_matrix[i][j] = s_p[0]
            group_matrix[j][i] = s_p[0]

for i in range(nodes_len):
    cur_grp_list = group_matrix[i]
    
    cur_grp_number = min(cur_grp_list)
    
    if(cur_grp_number == group_nodes[i]):
        cur_grp_number = 0
    
    print("Group Number for: " + str(group_nodes[i]) + ' is: ' + str(cur_grp_number))
