# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 11:53:17 2017

@author: Matteo
"""
# =============================================================================
# PART 1
# =============================================================================
# In[ ]:
#Import json file

import itertools
import networkx as nx
import json
import matplotlib.pyplot as plt

data = json.load(open('C:/Users/Matteo/Desktop/Data Mining with aris/Homework4/reduced_dblp.json'))
## In[ ]:
#sum1=0
#for conference in range(len(data)):
#    sum1 += len(data[0]['authors'])
# In[ ]:
# Here we will parse informations
conference=[]
publications={} #dict of authors, key is id_plublication if u want to extract more informations from file modify this part
for publication in range(len(data)):
    publications[data[publication]['id_publication']]={}
    publications[data[publication]['id_publication']]['authors']=[]
# Im extracting only authors_id
    for author in data[publication]['authors']:
        try:
            publications[data[publication]['id_publication']]['authors'].append(author['author_id'])
        except:
            pass 
    publications[ data[publication]['id_publication']]['conference']=data[publication]['id_conference']  
    conference.append(data[publication]['id_conference'] )
conference1= list(set(conference))
# In[ ]:
#i=0
#create graph
G=nx.Graph()
authorlist=[]
#i=0
for author_id in publications.keys():
#    if i<100:
        #For each publications, I linked all author that share this publication
        #If u want to see how im adding nodes u can start creating graph for only 1 publication and draw the graph, after u draw graph for 5-6 publications to see how nodes are linked      
        G.add_nodes_from(publications[author_id]['authors'])
        edges = itertools.permutations(publications[author_id]['authors'],2)
        G.add_edges_from(edges)    
#        print(publications[author_id])
#        print(publication)
        authorlist+= publications[author_id]['authors']
#        i+=1
 #List of authors, we use set because we will use this list to build an inverted_index
author_id=list(set(authorlist))
# In[ ]:
#creating inverted_index:authors_id are keys, publications will be  values
## Im not sure we need author_id or author name
#inverted_index.keys() . i will use this dict to calculate Weights
inverted_index={} 
for publication in publications.keys():
    for author in author_id:
        for aut in publications[publication]['authors']:
            #confronto lauthor che l' autore con il quale sto lavorando con tutti gli aut (autori della pubblicazione) se sono uguali aggiungo la pubblicazione tra i valori del dizionario
            if aut== author: 
               if author not in inverted_index.keys():
                    inverted_index[author]=[]
                    inverted_index[author].append(publication)
               else:
                    inverted_index[author].append(publication)
# In[ ]:
#Calculating Weight
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
#print(G[163842])
## In[ ]: #if u want to draw a little simple graph , this graph will be very bad with a lot of nodes
#nx.draw_circular(G)            
# In[ ]:
# =============================================================================
# PART 2
# =============================================================================      
# In[ ]:
inverted_index2={} 
#i=0
for publication in publications.keys():
#    if i<10:
#        print(publication)
        for conference in conference1:
#            print(conference)
#            try:
            if publications[publication]['conference']== conference: 
                if conference not in inverted_index.keys():
                    inverted_index2[conference]=[]
                    for aut in publications[publication]['authors']:
                        inverted_index2[conference].append(aut)
                    
                else:
                    for aut in publications[publication]['authors']:
                        inverted_index2[conference].append(aut)#            except:
#                pass
#        i+=1
# In[ ]:
#(['conf/pkdd/2011-1', 'conf/sigmod/2015', 'conf/wsdm/2011', 'conf/wsdm/2010', 'conf/icwsm/2016', 'conf/innovations/2012', 'conf/icdm/2015', 'conf/www/2015c', 'conf/www/2012', 'conf/icalp/2010-1', 'conf/ipco/2013', 'conf/soda/2014', 'conf/kdd/2014', 'conf/sigir/2016', 'conf/nips/2016', 'conf/sagt/2013', 'conf/cikm/2010', 'conf/wine/2016', 'conf/atal/2015'])
#print( "Give me an id_conference and i will return a sugraph of authors.")
#import matplotlib.pyplot as plt
#pos = nx.spring_layout(G)  #setting the positions with respect to G, not k.
conference= 'conf/sigmod/2015'
k = G.subgraph(inverted_index2[conference])  
#
#plt.figure()
#nx.draw(G)
#
#othersubgraph = G.subgraph(range(6,G.order()))
nx.draw_circular(k, node_color = 'b')
#plt.show()
#
#nx.draw(k)











