
# coding: utf-8

# In[ ]:


"""
Created on Mon Dec 11 02:06:17 2017

@author: Matteo
"""
import itertools
import networkx as nx
import json
#import matplotlib.pyplot as plt
data = json.load(open('C:/Users/Ferrara/PERSONAL/UNIV/First Semester/Algorithmic Methods of Data Mining/HW4/reduced_dblp.json'))
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


## Part 3.A
## author_ id as input()
from collections import defaultdict
from heapq import *

def shortest_path(G, start, end):
    dict1 = defaultdict(list)
    for author1 in G.edge.keys():
        for author2 in G[author1].keys():
            dict1[author1].append((author2,G[author1][author2]['Weight']))
    list111= [[0,start,()]]
    seen=set()
    while list111:
        (cost,vertex1,path) = heappop(list111)
        if vertex1 not in seen:
            seen.add(vertex1)
            path = (vertex1, path)
            if vertex1 == end: 
                return (cost, path)
            for vertex2, weight in dict1[vertex1]:
                if vertex2 not in seen:
                    heappush(list111, [cost+weight, vertex2, path])
    list111= list(list111)
    return list111

# In[ ]:
author_id=256177
Aris_id= 0
for publication in publications_dict.keys():
    for author in range(len(publications_dict[publication]['authors'])):
        if publications_dict[publication]['authors'][author]['author']=='aris anagnostopoulos':
            Aris_id=  publications_dict[publication]['authors'][author]['author_id']
        pass
    pass

# In[ ]: POINT 3.A
try:
    path=shortest_path(G,author_id,Aris_id)    
    print(path[0])
except nx.NetworkXNoPath:
    print('No path')
# In[ ]:

# Point 3.B
nodes = [143752, 143709]

#print(list(G.edge.keys()))
for k in G.edge.keys():
    for z in nodes:
        
        
        path111 = shortest_path(G,z,k)
        if path111 and z!=k:
            #print(path111[0])
        
            print(shortest_path(G,k,z)) ## Here calc s_p for each nodes
#TODO calc the min (group number) I think here paste the last part of Vamsi's code
        
     
        
        #print(path111)


#prova = shortest_path(G,143752,143709)
#print("prova: "+str(prova) )

    


# In[2]:

list(shortest_path(G,256176, 256177))[0]


# In[ ]:



