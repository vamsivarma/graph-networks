#This file contains 3 sub-modules

#Graph_Index - For fetching data, initializing Graph and created required meta data
#Graph_Operations - For all the operations on the graph like finding Graph centrality, Node proximity, Shortest path and Group Nummber
#Graph_Web - Wrappers to Graph_Operation which act as API's exposed to web
#And the rest is Web Server making use of Python Web Package to send and receive data from Browser


from collections import defaultdict
from heapq import *

import itertools
import networkx as nx
import matplotlib.pyplot as plt
import web
import json

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
    
    #Preparing authors list and conferences list to send as API response to UI
    authors_list_ui = [] 
    conferences_list_ui = []
    
    #Conference ID to Conference Name map
    conf_rev_map = {}
    
    #Author ID to Author Name
    authors_rev_map = {}
    
    nodes_len = 500
    
    def fetch_data(self):     
        self.data = json.load(open('reduced_dblp.json'))
    
    def build_graph(self):
        
        #POINT 1
        for i in range(self.nodes_len):
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
            
            cur_author_id = self.authors_map[author]
            
            cur_author_dict = {
                    "id": cur_author_id,
                    "text": author.title()
                    }
            authors_ui.append(cur_author_dict)
            
            self.authors_rev_map[cur_author_id] = author.title()
            
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
            
            self.conf_rev_map[cur_conf_dict['id']] = conf        

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
        
        self.nodes_len = len(self.data)
        
        self.build_graph()
        self.remove_duplicates()
        self.create_indexes()

gi = Graph_Index()

class Graph_Operations:
    
    #Metadata containing list of configuration options to do operations on Graph
    operations_meta = {
                'subset_nodes':  [255395, 208976],
                'conference_name': '', #'conf/iccs/2010',
                'hop_distance': 2,
                'author_proximity_id': 24568,#gi.authors_map['wamberto weber vasconcelos'], 
                'sp_author_id_1': 24569, #gi.authors_map['aris anagnostopoulos'], 
                'sp_author_id_2': 24570 #gi.authors_map['george brova']
            }
    
       
    subset_nodes_len = len(operations_meta['subset_nodes'])

    #Two dimentional array based on total number of vertexes and subset
    group_matrix = []
    author_dist_status_map = {}    
    
    authors_len = len(gi.authors_list)
    
    #POINT 2.1
    def calculate_centralities(self, serverFlag):
        
        conf_name = self.operations_meta['conference_name']    
        
        conf_details = gi.conferences_map[conf_name] 
        conf_authors = conf_details[1]
        
        k = gi.G.subgraph(conf_authors)
        
        degree = nx.degree_centrality(k)
        closeness = nx.closeness_centrality(k)
        betweenness = nx.betweenness_centrality(k)
        
        if serverFlag:
            # modify this part adding a dictonary
            print('Some centralities measures for nodes selected in our subgraph!')
          
        authorsDataset = []    
        
        for author_id in conf_authors:
            
            if author_id in gi.authors_rev_map:
                
                cur_author_ary = [author_id, gi.authors_rev_map[author_id], degree[author_id], closeness[author_id], betweenness[author_id]]
                
                if serverFlag:
                    
                    print('Author_id: ' + str(cur_author_ary[0]))
                    print('')
                    print('Degree Centrality: ' + str(cur_author_ary[2]) )
                    print('Closeness Centrality: ' + str(cur_author_ary[3]))
                    print('Betweenness Centrality: ' + str(cur_author_ary[4]))
                    print('')
                else:
                    authorsDataset.append(cur_author_ary)
    
        
        nx.draw(k)
        
        if not serverFlag:
            plt.savefig("static/images/centrality/centrality_" + str(conf_details[0]))
            plt.clf()
        
        return authorsDataset
        
    
    #POINT 2.2 
    def calculate_subgraph(self, serverFlag):
        
        author_id = self.operations_meta['author_proximity_id']
        
        proximityDataset = []
        
        #path=nx.single_source_shortest_path_length(G=G,source= author_id,cutoff=d)
        kk=nx.ego_graph(G= gi.G, n= author_id, radius= self.operations_meta['hop_distance'], center= True, undirected= True)
        
        nx.draw(kk)
        
        if not serverFlag:
            
            plt.savefig("static/images/proximity/proximity_" + str(author_id))
            plt.clf()
            
            for sg_author_id in kk.edge.keys():
                
                if(sg_author_id != author_id):
                    
                    if sg_author_id in gi.authors_rev_map:
                        
                        cur_weight = 0.0
                        cur_weight_obj = self.shortest_path_advanced(kk, author_id, sg_author_id, True) 
                        
                        if sg_author_id in cur_weight_obj:
                            cur_weight = cur_weight_obj[sg_author_id]                        
                        
                        
                        cur_author_ary = [sg_author_id, gi.authors_rev_map[sg_author_id], cur_weight]
                        
                        proximityDataset.append(cur_author_ary)
                        
        return proximityDataset
                      

    #POINT 3.1
    #@TODO: Need to improve the number of iterations here...
    def shortest_path_advanced(self, G, start, end, partialFlag):
        
        authors_list = []
        
        if partialFlag:
            authors_list = G.edge.keys()
        else:
            authors_list = gi.authors_list
        
        dict1 = defaultdict(list)
        for author1 in authors_list:
            for author2 in G[author1].keys():
                    dict1[author1].append((author2, G[author1][author2]['weight']))
            
            
        pathList = [[0,[start,0],()]]
        seen = set()
        
        #Dictionary which contains total distance at every node in a path
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


    def find_path_given_author(self, serverFlag): 
        
        author_1 = self.operations_meta['sp_author_id_1']
        author_2 = self.operations_meta['sp_author_id_2']
        
        try:
            
            path = self.shortest_path_advanced(gi.G, author_1, author_2, False)  
            
            shortest_distance = 0
            
            if(len(path.keys())):
                if author_2 in path:
                    shortest_distance = path[author_2]
                    if serverFlag:
                        print(shortest_distance)
                        #kk = gi.G.subgraph(path.keys())
                        #nx.draw(kk)
                        
                else:
                   if serverFlag: 
                       print('No path')
            else:
                if serverFlag: 
                    print('No path')
        
        except nx.NetworkXNoPath:
            
            if serverFlag:
                print('No path')
                
        return shortest_distance
    
    #For updating neighbour nodes with the shortest path if the weight between the authors is 0.0
    #To reduce the no of times shortest path algoritm is invoked there by improving the response time for calculating the group numbers of a given graph
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
    def find_graph_number(self, serverFlag):
        
        self.init_group_matrix()
        
        #variable which holds no of times shortest path algoritm is invoked
        iterations = 0

        for i in range(self.authors_len):
            cur_author = gi.authors_list[i]
            self.cur_author_dist_dict = {}
            
            #Check if the node is already is updated with the shortest path values
            if not self.author_dist_status_map[cur_author]:
            
                for j in range(self.subset_nodes_len):
                     
                    cur_subset_node = self.operations_meta['subset_nodes'][j]
                    cur_node_dist = cur_author
                    
                    if(cur_author != cur_subset_node):
                        
                        if cur_subset_node not in self.cur_author_dist_dict:
                            
                            iterations += 1
                            
                            s_p = self.shortest_path_advanced(gi.G, cur_author, cur_subset_node, False)
                        
                            if(len(s_p.keys())):
                                self.cur_author_dist_dict.update(s_p)
                                
                                #Check if the shortest path between node and given node in the group is already present
                                #If yes then directly update the path value else invoke the shortest path algorithm
                                if cur_subset_node in self.cur_author_dist_dict:
                                    cur_node_dist = self.cur_author_dist_dict[cur_subset_node]
                                    
                        else:
                            cur_node_dist =  self.cur_author_dist_dict[cur_subset_node]
                        
                        self.group_matrix[i][j] = cur_node_dist
                
                self.author_dist_status_map[cur_author] = True
                
            self.update_the_neighbour_nodes(cur_author, i)

        groupDataset = []
        
        for i in range(self.authors_len):
            cur_author_id = gi.authors_list[i]
            cur_grp_list = self.group_matrix[i]
            
            #Finding the minimum of shortest paths    
            cur_grp_number = min(cur_grp_list)
            
            if(cur_grp_number == gi.authors_list[i]):
                cur_grp_number = 0
            
            if serverFlag:
                print("Group Number for: " + str(cur_author_id) + ' is: ' + str(cur_grp_number))
            else:
                if cur_author_id in gi.authors_rev_map: 
                    cur_author_name = gi.authors_rev_map[cur_author_id]
                    cur_node_grp = [cur_author_id, cur_author_name, cur_grp_number] 
                    groupDataset.append(cur_node_grp) 
            
        return groupDataset

    def __init__(self):

        pass
        
        #2.1
        #self.calculate_centralities(True)

        #2.2
        #self.calculate_subgraph(True)

        #3.1
        #self.find_path_given_author(True)
 
        #3.2
        #self.find_graph_number(True)
        
        
go = Graph_Operations()


#Wrapper for exposing the graph operations with the web layer
class Graph_Web:
    
    #Returns the authors list based on the data stored in G
    def get_authors(self):
        return gi.authors_list_ui
    
    #Returns the conferences list based on the data stored in G
    def get_conferences(self):
        return gi.conferences_list_ui
    
    def find_centralities(self, conf_id):
        
        go.operations_meta['conference_name']  = gi.conf_rev_map[conf_id]
        
        return go.calculate_centralities(False)
    
    def find_proximity(self, proximity_id, hop_distance):
        
        go.operations_meta['author_proximity_id'] = proximity_id
        go.operations_meta['hop_distance'] = hop_distance
        
        return go.calculate_subgraph(False)
    
    def find_shortest_path(self, author1_id, author2_id):
        
        go.operations_meta['sp_author_id_1'] = author1_id
        go.operations_meta['sp_author_id_2'] = author2_id
        
        return go.find_path_given_author(False)
    
    def find_author_group_numbers(self, author_subset):
        
        go.operations_meta['subset_nodes'] = author_subset
        
        return go.find_graph_number(False)
        
gw = Graph_Web()


#Web Interface Package
urls = (
    '/', 'graph_ui',    
    '/get_conferences', 'get_conferences',
    '/get_authors', 'get_authors',
    '/find_centralities', 'find_centralities',
    '/find_proximity', 'find_proximity',
    '/find_shortest_path', 'find_shortest_path',
    '/find_author_group_numbers', 'find_author_group_numbers'  
)


render = web.template.render('ui/')

class graph_ui:
  def GET(self):
    return render.graph_ui()

#To get all the conferences as a key value pairs to be displayed on UI
class get_conferences:        
    def GET(self):

        output = {
                'conferences_list': gw.get_conferences()
                }

        web.header('Content-Type', 'application/json')
        return json.dumps(output)

#To get all the authors as a key value pairs to be displayed on UI
class get_authors:        
    def GET(self):
        
        output = {
                'authors_list': gw.get_authors()
                }
        
        web.header('Content-Type', 'application/json')
        return json.dumps(output)

class find_centralities:
    def GET(self):
        
        cData = web.input()
        conf_id = int(cData['conf_id'])
        conf_name = cData['conf_name']
        
        output = {
                'conf_id': conf_id,
                'conf_name': conf_name,
                'cDataset': gw.find_centralities(conf_id)
                }
        
        web.header('Content-Type', 'application/json')
        return json.dumps(output)

class find_proximity:
    def GET(self):
        
        pData = web.input()
        proximity_id = int(pData['proximity_id'])
        proximity_name = pData['proximity_name']
        hop_count = int(pData['hop_count'])
        
        
        output = {
                'proximity_id': proximity_id,
                'proximity_name': proximity_name,
                'pDataset': gw.find_proximity(proximity_id, hop_count)
                }
        
        web.header('Content-Type', 'application/json')
        return json.dumps(output)
    
class find_shortest_path:
    def GET(self):
        
        sData = web.input()
        author1_id = int(sData['author1_id'])
        author2_id = int(sData['author2_id'])
        author1_name = sData['author1_name']
        author2_name = sData['author2_name']
        
        output = {
                'shortest_distance': gw.find_shortest_path(author1_id, author2_id),
                'author1_name': author1_name,
                'author2_name': author2_name
                }
        
        web.header('Content-Type', 'application/json')
        
        return json.dumps(output)
    
class find_author_group_numbers:
    def GET(self):
        
        gData = web.input()
        authors_subset = [int(author) for author in gData['authors_subset'].split(',')]
        author_names = gData['author_names']
        
        output = {
                'author_names': author_names,
                'gDataset': gw.find_author_group_numbers(authors_subset),
                'authors_subset': authors_subset
                }
        
        web.header('Content-Type', 'application/json')
        
        return json.dumps(output)

app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()

    





