# In[ ]:
#Import json file

import itertools
import networkx as nx
import json
#import matplotlib.pyplot as plt

data = json.load(open('C:/Users/Matteo/Desktop/Data Mining with aris/Homework4/reduced_dblp.json'))
# In[ ]:
sum1=0
for conference in range(len(data)):
    sum1 += len(data[0]['authors'])
# In[ ]:
# Here we will parse informations
publications={} #dict of authors, key is id_plublication if u want to extract more informations from file modify this part
for publication in range(len(data)):
    publications[data[publication]['id_publication']]=[]
# Im extracting only authors_id
    for author in data[publication]['authors']:
        try:
            publications[ data[publication]['id_publication']].append(author['author_id'])
        except:
            pass       

# In[ ]:
i=0
#create graph
G=nx.Graph()
authorlist=[]
for author_id in publications.keys():
    if i<10:
        #For each publications, I linked all author that share this publication
        #If u want to see how im adding nodes u can start creating graph for only 1 publication and draw the graph, after u draw graph for 5-6 publications to see how nodes are linked      
        G.add_nodes_from(publications[author_id])
        edges = itertools.permutations(publications[author_id],2)
        G.add_edges_from(edges)    
#        print(publications[author_id])
#        print(publication)
        authorlist+= publications[author_id] 
        i+=1
 #List of authors, we use set because we will use this list to build an inverted_index
author_id=list(set(authorlist))
# In[ ]:
#creating inverted_index:authors_id are keys, publications will be  values
## Im not sure we need author_id or author name
#inverted_index.keys() . i will use this dict to calculate Weights
inverted_index={} 
for publication in publications.keys():
    for author in author_id:
        for aut in publications[publication]:
            #confronto lauthor che l' autore con il quale sto lavorando con tutti gli aut (autori della pubblicazione) se sono uguali aggiungo la pubblicazione tra i valori del dizionario
            if aut== author: 
               if author not in inverted_index.keys():
                    inverted_index[author]=[]
                    inverted_index[author].append(publication)
               else:
                    inverted_index[author].append(publication)
# In[ ]:
#Calculating Weight
import numpy as np
for author in G.edge.keys():
    b= set(inverted_index[author])
#    print(b)
    for author2 in G.edge[author]:
        G[author][author2]={}
        a= set(inverted_index[author2])
        num=a.intersection(b)
        den= a.union(b)
#            print(num)
#            print(den)
        #im not sure about how to calculate inteserction and union (there are various ways)
        G[author][author2]['Weight']= 1-(len(num)/len(den))
       
#                
            


            
# In[ ]:
print(G.edge)
# In[ ]: #if u want to draw a little simple graph , this graph will be very bad with a lot of nodes
nx.draw_circular(G)