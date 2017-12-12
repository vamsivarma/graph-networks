# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 18:34:04 2017

@author: Matteo
"""

## Part 3.A
## author_ id as input()
author_id=256177
Aris_id= 0
for publication in publications_dict.keys():
    for author in range(len(publications_dict[publication]['authors'])):
        if publications_dict[publication]['authors'][author]['author']=='aris anagnostopoulos':
            Aris_id=  publications_dict[publication]['authors'][author]['author_id']
        pass
    pass
# In[ ]:
#POINT 3.A
try:
#    path=[1,2,3,4,5]
    path=nx.dijkstra_path(G,author_id,Aris_id)
#    print(nx.dijkstra_path(G,author_id,Aris_id))
    sum1=0
    var=0
    prev= path[var]
    for vertex in range(len(path)-1):
        next1= path[var+1]
#        sum1+= prev+next1
        sum1+= G[prev][next1]['Weight']
        var+=1
        prev= path[var]
        
    print(sum1)
except nx.NetworkXNoPath:
    print('No path')
# In[ ]:
for author in inverted_index.keys():
    if author== Aris_id:
        print(inverted_index[author])
    
#for author in G:
#    for au in G[author]:
#        print(author,au, G[author][au])