
"""
Created on Mon Nov 27 15:21:38 2017

@author: User
"""

import web
import json
import graph_index_module as gim

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

class get_conferences:        
    def GET(self):

        output = {
                'conferences_list': gim.gw.get_conferences()
                }

        web.header('Content-Type', 'application/json')
        return json.dumps(output)

class get_authors:        
    def GET(self):
        
        output = {
                'authors_list': gim.gw.get_authors()
                }
        
        web.header('Content-Type', 'application/json')
        return json.dumps(output)
    
    
class find_centralities:
    def GET(self):
        
        cData = web.input()
        conf_id = int(cData['conf_id'])
        
        output = {
                'conf_id': conf_id,
                'cDataset': gim.gw.find_centralities(conf_id)
                }
        
        web.header('Content-Type', 'application/json')
        return json.dumps(output)

class find_proximity:
    def GET(self):
        
        pData = web.input()
        author_id = int(pData['author_id'])
        
        print("In Find Proximity...")
        print(author_id)
        
        '''
        output = {
                'authors_list': gim.gw.find_proximity(author_id)
                }
        
        web.header('Content-Type', 'application/json')
        return json.dumps(output)
        '''
    
class find_shortest_path:
    def GET(self):
        
        sData = web.input()
        author1_id = int(sData['author1_id'])
        author2_id = int(sData['author2_id'])
        
        
        print("In Shortest Path...")
        print(author1_id)
        print(author2_id)
        
        '''
        output = {
                'authors_list': gim.gw.find_shortest_path(author1_id, author2_id)
                }
        
        web.header('Content-Type', 'application/json')
        return json.dumps(output)
        '''
    
class find_author_group_numbers:
    def GET(self):
        
        gData = web.input()
        authors_subset = [int(author) for author in gData['authors_subset'].split(',')]
        print('Inside Group Numbers...')
        print(authors_subset)
        
        
        '''
        output = {
                'authors_list': gim.gw.find_author_group_numbers(authors_subset)
                }
        
        web.header('Content-Type', 'application/json')
        
        return json.dumps(output)
        '''

app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()
    