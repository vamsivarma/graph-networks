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

for i in range(len(data)):
    cur_conference = data[i]
    cur_publication = cur_conference['id_publication_int']
    publications_dict[cur_publication]={}
    publications_dict[cur_publication]['authors']=[]
    
    
    cur_authors = []
    for author in cur_conference['authors']:
        cur_author = author['author_id']
        publications_dict[cur_publication]['authors'].append(author)
        cur_authors.append(cur_author)
        
        if cur_author not in inverted_index.keys():
            inverted_index[cur_author]=[]
            inverted_index[cur_author].append(cur_publication)
        else:
            inverted_index[cur_author].append(cur_publication)
    
    #Updating the graph    
    G.add_nodes_from(cur_authors)
    edges = itertools.combinations(cur_authors, 2)
    G.add_edges_from(edges)
    
    authors_list += cur_authors
    
    cur_conference = cur_conference['id_conference_int']
    
    publications_dict[cur_publication]['id_conference_int'] = cur_conference
    conferences_list.append(cur_conference)

#Removing the duplicate entries
conferences_list = list(set(conferences_list))
authors_list = list(set(authors_list))    

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