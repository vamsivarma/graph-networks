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




class Graph_Index:
    
    G = nx.Graph()
    publications_dict = {}
    conferences_list = []
    authors_list = []
    inverted_index = {}
    
    conferences_map = {}
    publications_map = {}
    authors_map = {}
    data = []
    
    authors_list_ui = [] 
    conferences_list_ui = []
    
    def fetch_data(self):     
        self.data = json.load(open('reduced_dblp.json'))
    
    def build_graph(self):
        
        #POINT 1
        for i in range(100):
            cur_conference = self.data[i]
            
            cur_conference_id = cur_conference['id_conference_int']
            cur_conference_name = cur_conference['id_conference'] 
            
            cur_publication_id = cur_conference['id_publication_int']
            cur_publication_name = cur_conference['id_publication']
            
            self.publications_dict[cur_publication_id]={}
            self.publications_dict[cur_publication_id]['authors']=[]
            
            #Build Conferences Map => Conference Name to Conference ID
            if cur_conference_name not in self.conferences_map.keys():
                self.conferences_map[cur_conference_name] = []
                self.conferences_map[cur_conference_name].append(cur_conference_id)
                self.conferences_map[cur_conference_name].append([])
            
            #Build Publications Map => Publication Name to Publication ID
            if cur_publication_name not in self.publications_map.keys():
                self.publications_map[cur_publication_name] = cur_publication_id
            
            cur_authors = []
            for author in cur_conference['authors']:
                
                cur_author_id = author['author_id']
                cur_author_name = author['author']
                
                cur_authors.append(cur_author_id)
                
                if cur_author_id not in self.inverted_index.keys():
                    self.inverted_index[cur_author_id]=[]
                    self.inverted_index[cur_author_id].append(cur_publication_id)
                else:
                    self.inverted_index[cur_author_id].append(cur_publication_id)
                    
                #Build Authors map => Author Name to Author ID
                if cur_author_name not in self.authors_map.keys():
                    self.authors_map[cur_author_name] = cur_author_id        
            
            
            #Build Conferences To Authors Map => Connference Name to Authors
            if cur_conference_name in self.conferences_map.keys():
                self.conferences_map[cur_conference_name][1].extend(cur_authors)
            
            #Updating the graph    
            self.G.add_nodes_from(cur_authors)
            edges = itertools.combinations(cur_authors, 2)
            self.G.add_edges_from(edges)
            
            self.authors_list += cur_authors
            
            self.publications_dict[cur_publication_id]['id_conference_int'] = cur_conference_id
            self.conferences_list.append(cur_conference_id)
            
    def formatAuthorListForUI(self):
        
        authors_ui = []
        
        for author in self.authors_map:
            cur_author_dict = {
                    "id": self.authors_map[author],
                    "text": author.title()
                    }
            authors_ui.append(cur_author_dict)
            
        return authors_ui
            

    def remove_duplicates(self):
       
        #Removing the duplicate entries
        self.conferences_list = list(set(self.conferences_list))
        self.authors_list = list(set(self.authors_list))   
        
        self.authors_list_ui = self.formatAuthorListForUI()
        
        self.conferences_list_ui = []
        
        


        for conf in self.conferences_map:
            cur_conf_dict = {
                    "id": self.conferences_map[conf][0],
                    "text": conf.title()  
                    }
            self.conferences_map[conf][1] = list(set(self.conferences_map[conf][1]))
            self.conferences_list_ui.append(cur_conf_dict)
            

    def create_indexes(self):

        #Assigning weights to the edges
        for author in self.authors_list:
            b= set(self.inverted_index[author])
            for author_edge in self.G.edge[author]:
                self.G[author][author_edge] = {}
                a = set(self.inverted_index[author_edge])
                num = list(set(a.intersection(b)))
                den = list(set(a.union(b))) 
                
                self.G[author][author_edge]['weight']= 1-( len(num) / len(den) )   
               
        #nx.draw(G)

    def __init__(self):
        
        self.fetch_data()
        self.build_graph()
        self.remove_duplicates()
        self.create_indexes()

gi = Graph_Index()



class Graph_Operations:
    
    subset_nodes = list(set([270587, 270585, 524503, 365179, 33951, 112985, 364898, 255487, 166813, 250148]))
    #subset_nodes = list(set([270587, 270585]))    

    subset_nodes_len = len(subset_nodes)

    #Build a 2 dimentional matrix based on total number of vertexes and subset
    group_matrix = []

    author_dist_status_map = {}    
    
    authors_len = len(gi.authors_list)

    def calculate_centralities(self):
        
        #POINT 2.1
        conference_name = 'conf/pkdd/2011-1' #'conf/acmdis/2010'
        conf_details = gi.conferences_map[conference_name]
        conference_id = conf_details[0] 
        conf_authors = conf_details[1]
        
        k = gi.G.subgraph(conf_authors)
        
        degree = nx.degree_centrality(k)
        
        closeness = nx.closeness_centrality(k)
        
        betweenness = nx.betweenness_centrality(k)
        # modify this part adding a dictonary
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
    
    def calculate_subgraph(self):
        #POINT 2.2
        author_name = "michel verleysen"
        #author_name = "paulo costa"
        
        author_id = gi.authors_map[author_name]
        
        d=1 #if d>1 doesn't work
        
        #path=nx.single_source_shortest_path_length(G=G,source= author_id,cutoff=d)
        kk=nx.ego_graph(G= gi.G, n= author_id, radius= d, undirected= True, center= True)
        
        nx.draw(kk)


    #POINT 3.1
    #@TODO: Need to improve the number of iterations here...
    def shortest_path_advanced(self, G, start, end):
        
        dict1 = defaultdict(list)
        for author1 in gi.authors_list:
            for author2 in G[author1].keys():
                    dict1[author1].append((author2, G[author1][author2]['weight']))
            
            
        pathList = [[0,[start,0],()]]
        seen = set()
        
        pathInfoList = {}
        
        while pathList:
            (cost, [vertex1, cur_cost], path) = heappop( pathList )
            
            pathInfoList[vertex1] = cur_cost
            
            if vertex1 not in seen:
                seen.add(vertex1)
                path = (vertex1, path)
                if vertex1 == end: 
                    #return (cost, path)
                    break
                    
                for vertex2, weight in dict1[vertex1]:
                        heappush(pathList, [cost+weight, [vertex2, cost+weight], path])
                        
        pathList= list(pathList)
        
        return pathInfoList


    def find_path_given_author(self):
        aris_id = gi.authors_map["aris anagnostopoulos"]
        #aris_id = authors_map["daniel hackenberg"]
        
        author_name = "george brova"
        #author_name = "damien djaouti"
        
        author_id = gi.authors_map[author_name]
        
        
        try:
            
            path = self.shortest_path_advanced(gi.G, author_id, aris_id)  
            
            print(path)
        
            '''
            if(len(path.keys())):
                if path[aris_id]:
                    print(path[aris_id])
                else:
                   print('No path') 
            else:
                print('No path')
            '''
        
        except nx.NetworkXNoPath:
        
            print('No path')
    
    def update_the_neighbour_nodes(self, author_id, author_index):
    

        for na in gi.G[author_id].keys():
            if gi.G[author_id][na]['weight'] == 0.0 and not self.author_dist_status_map[na]:
                
                na_index = gi.authors_list.index(na)
                
                for i in range(self.subset_nodes_len):
                    
                    cur_dist = self.group_matrix[author_index][i]
                    
                    if(cur_dist != author_id):
                        self.group_matrix[na_index][i] = self.group_matrix[author_index][i]
                
                self.author_dist_status_map[na] = True

    def init_group_matrix(self):
        
        for author in gi.authors_list:
    
            author_list = []
            self.author_dist_status_map[author] = False
            
            for i in range(self.subset_nodes_len):    
                author_list.append(author)
            
            self.group_matrix.append(author_list)

    #POINT 3.2
    #@TODO: Check if using Numpy arrays will make this effiecient    
    def find_graph_number(self):
            self.init_group_matrix()
            

            iterations = 0
            for i in range(self.authors_len):
                cur_author = gi.authors_list[i]
                self.cur_author_dist_dict = {}
                
                if not self.author_dist_status_map[cur_author]:
                
                    for j in range(self.subset_nodes_len):
                         
                        cur_subset_node = self.subset_nodes[j]
                        cur_node_dist = cur_author
                        
                        if(cur_author != cur_subset_node):
                            
                            if cur_subset_node not in self.cur_author_dist_dict:
                                
                                iterations += 1
                                
                                s_p = self.shortest_path_advanced(gi.G, cur_author, cur_subset_node)
                            
                                if(len(s_p.keys())):
                                    self.cur_author_dist_dict.update(s_p)
                                    
                                    if cur_subset_node in self.cur_author_dist_dict:
                                        cur_node_dist = self.cur_author_dist_dict[cur_subset_node]
                                        
                            else:
                                cur_node_dist =  self.cur_author_dist_dict[cur_subset_node]
                            
                            self.group_matrix[i][j] = cur_node_dist
                    
                    self.author_dist_status_map[cur_author] = True
                    
                self.update_the_neighbour_nodes(cur_author, i)



            for i in range(self.authors_len):
                cur_grp_list = self.group_matrix[i]
                
                cur_grp_number = min(cur_grp_list)
                
                if(cur_grp_number == gi.authors_list[i]):
                    cur_grp_number = 0
                
                print("Group Number for: " + str(gi.authors_list[i]) + ' is: ' + str(cur_grp_number))
    
                
    def __init__(self):
        
        self.calculate_centralities()
        self.calculate_subgraph()
        self.find_path_given_author()
        self.find_graph_number()
        
        
#go = Graph_Operations()


class Graph_Web:
    
    #Returns the authors list based on the data stored in G
    def get_authors(self):
        return gi.authors_list_ui
    
    #Returns the conferences list based on the data stored in G
    def get_conferences(self):
        return gi.conferences_list_ui
    

gw = Graph_Web()
    

#print(gw.get_authors()) 
#print(gw.get_conferences()) 





