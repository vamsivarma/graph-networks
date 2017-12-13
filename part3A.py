# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 18:34:04 2017

@author: Matteo
"""

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
    return list111[0]

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

