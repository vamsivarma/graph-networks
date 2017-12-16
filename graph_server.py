
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
    
)

render = web.template.render('ui/')

class graph_ui:
  def GET(self):
    return render.graph_ui()

class get_conferences:        
    def GET(self):

        output = {
                'conferences_map': gim.gw.get_conferences()
                }

        web.header('Content-Type', 'application/json')
        return json.dumps(output)

class get_authors:        
    def GET(self):
        
        output = {
                'authors_list': gim.gw.get_conferences()
                }
        
        web.header('Content-Type', 'application/json')
        return json.dumps(output)

app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()
    