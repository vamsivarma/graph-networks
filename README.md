Algorithmic Methods of Data Mining Homework 4

Vamsi Krishna Varma Gunturi, Matteo Manzari, Andrea Ferrara


How to use our application - 

Mandatory softwares: Python, Anaconda 3.x (If you want to check the code from back end otherwise not required) 

Mandatory Python packages required: web, networkx, matplotlib, itertools, collections, heapq, json


1) Open command prompt on the repository path

2) Exectute, "python Modules.py" on the command line and wait for python code to exectute, what this does is fetch the data from reduced_dblp.json or any json file given in the python file and build a graph and corresponding meta data which can be used while making operations on the graph that was built. This commands also loads required code to activate the api end points to make invocations from external environments like a web browser

3) Once you see the following message,
http://0.0.0.0:8080/ which means that server has started and it is listening for request on port number 8080

4) To view the web interface of the graph build, open a new browser tab and type in 'http://localhost:8080'

5) Now you will see 4 tabs for doing following 4 operations,
	
	(1) Finding author centrality of a selected conference - up on selecting a conference and clicking on search, you can see the information of a conference visualized as 2 variants  - 
		
		- as a graph which represents the authors of a conference and their corresponding connections
		
		- as a table which represent the centralities(degree, closeness and betweeness) of each author of that conference. You can even sort a particular criteria to see which authors have a greater and lesser centralities with in that conference. You can even find information of a specific author by entering his name in the search box given on top. Authors in the table are paginated. If you want to view more authors per page you can adjust the count per page from the drop down on top left

	(2) Finding author proximity based on selected author and hop distance - when user selects an author from drop down ( he can even search for a particular author from the search field present and filter out the authors who have a particular set of words in their names) and give the hop distance and enter search, you can see information about proximity of an author is visualized as 2 varients, 
		
		- as a graph, which included graph of author proximity
		
		- as a table, which represents all the author neighbors and their distance from a selected author, by which we can easily find the people who are very near and far to a given author and also search for a particular author to find his distance from the selected author

	(3) Find shortest path between 2 authors, In this tab user is provided 2 drop down lists to find 2 authors and find shortest path/distance between them

	(4) Find Group Number - here user is provided a "multi select" drop down to select a sub set of authors to find the group number of every node with respective of that subset


