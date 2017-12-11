# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 02:06:17 2017

@author: Matteo
"""
import itertools
import networkx as nx
import json
#import matplotlib.pyplot as plt
data = json.load(open('C:/Users/Matteo/Desktop/Data Mining with aris/Homework4/reduced_dblp.json'))
# In[ ]: parse data
#POINT 1
publications_dict={}
conference1=[]
for i in range(len(data)):
    publications_dict[data[i]['id_publication']]={}
    publications_dict[data[i]['id_publication']]['authors']=[]
    for author in data[i]['authors']:
        publications_dict[data[i]['id_publication']]['authors'].append(author)
    publications_dict[data[i]['id_publication']]['id_conference']=data[i]['id_conference']
    conference1.append(publications_dict[data[i]['id_publication']]['id_conference'])

conference1=list(set(conference1))
# In[ ]:
G=nx.Graph()
authorlist=[]
#i=0
for publication in publications_dict.keys():
#    if i<100:
        list1=[]
        for author in publications_dict[publication]['authors']:
             list1.append(author['author_id'])   
        
        G.add_nodes_from(list1)
        edges = itertools.combinations(list1,2)
        
        G.add_edges_from(edges)    
        for author in  publications_dict[publication]['authors']:
            authorlist.append( author['author_id'])
#        i+=1
authorlist= list(set(authorlist))    
# In[ ]:


#Calculating Weight
# In[ ]:
inverted_index={} 
for publication in publications_dict.keys():
    for author in authorlist:
        for aut in publications_dict[publication]['authors']:
            if aut['author_id']== author: 
               if author not in inverted_index.keys():
                    inverted_index[author]=[]
                    inverted_index[author].append(publication)
               else:
                    inverted_index[author].append(publication)
# In[ ]:
for author in G.edge.keys():
    b= set(inverted_index[author])
    for author2 in G.edge[author]:
        G[author][author2]={}
        a= set(inverted_index[author2])
        num=list(set(a.intersection(b)))
        den= list(set(a.union(b))) 
        G[author][author2]['Weight']= 1-(len(num)/len(den))
# In[ ]:
# PART 2- a
#print('Give me a conference in input')
conference='conf/atal/2015' 
authorsss=[]
for publication in publications_dict.keys():
    if publications_dict[publication]['id_conference']== conference:
        for author in  publications_dict[publication]['authors']:
            authorsss.append( author['author_id'])
# In[ ]: 
k = G.subgraph(authorsss)
degree=nx.degree_centrality(k)
closeness=nx.closeness_centrality(k)
betweenness=nx.betweenness_centrality(k)
print('Some centralities measures for nodes selected in our subgraph!')
for author in authorsss:
    print('author_id: ' + str(author))
    print()
    print('degree centrality: ' +str(degree[author]))
    print('closeness centrality: ' +str(closeness[author]))
    print('betweenness centrality: ' +str(betweenness[author]))
    print()
#nx.draw(k)
#nx.info(k)
# In[ ]:
# PART 2- b
### Point 2 b
author_id=12364
d=1 #if d>1 doesn't work
#path=nx.single_source_shortest_path_length(G=G,source= author_id,cutoff=d)
kk=nx.ego_graph(G=G,n= author_id, radius= d, undirected= True, center= True)

nx.draw(kk)
    