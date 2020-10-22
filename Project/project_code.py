# ENGSCI233: Project
# Alex Chen
# 500193517
# ache934

from project_utils import *
import networkx as nx
from time import time
import numpy as np

# start time
t0 = time()

# initial reading of files
auckland = read_network('network.graphml')
rest_homes = get_rest_homes('rest_homes.txt')


# function for finding shortest length of the shortest path
def closest_node(network, start, destinations):
	''' Find the shortest length of the shortest path between a starting node and possible destinations.
		
		Parameters
		----------
		network : networkx.Graph
            The graph that contains the node and edge information

        start : str
		    Name of the starting node.

        destinations : list
		    List of possible destinations from the starting node.
			
		Returns
		-------
		closest_node : str
			Name of node from the list of destinations that is closes to the starting node in the network.
		roads : list
			List of shortest path to take to get form the start node to the closest node.

	'''
	# find the nearest node to the starting node
	closest_node = destinations[0]
	for i in destinations:
		if nx.shortest_path_length(network, start, i, weight='weight') < nx.shortest_path_length(network, start, closest_node, weight='weight'):
			closest_node = i
		
	roads = nx.shortest_path(network, start, closest_node, weight='weight')

	return closest_node, roads


def nearest_neighbour_algorithm(network, start, destinations):
	''' Algorithm which returns a list of nodes visited and the total path length
		
		Parameters
		----------
		network : networkx.Graph
            The graph that contains the node and edge information

        start : str
		    Name of the starting node.

        destinations : list
		    List of possible destinations from the starting node.
			
		Returns
		-------
		nodes_visited : list
			Name of node from the list of destinations that is closes to the starting node in the network.
		total_path_length: int
			Length of the path in hours
		roads_list : list
			List of all the roads taken from start to finish in the path.


	'''
	# initialise path list and total path length tracker
	nodes_visited = [start, ]
	total_path_length = 0
	roads_list = []
	
	while len(destinations) != 0:
		# find nearest node to starting node
		x, roads = closest_node(network, start, destinations)
		# remove this node from dest. list and add to path list
		destinations.remove(x)
		nodes_visited.append(x)
		# add roads to roads list
		roads_list.extend(roads)
		# add distance to running total of path length
		total_path_length = total_path_length + nx.shortest_path_length(network, start, x, weight='weight')
		start = x
	
	# return to airport
	nodes_visited.append('Auckland Airport')
	# add final distance
	total_path_length = total_path_length + nx.shortest_path_length(network, start, 'Auckland Airport', weight='weight')
	roads_list.extend(nx.shortest_path(network, start, 'Auckland Airport', weight='weight'))
	
	return nodes_visited, total_path_length, roads_list


def text_map_gen(filename, nodes_visited, network, roads):
	''' This function generates a .txt file of a path and a .png map of a path including the roads in-between.
		
		Parameters
		----------
		filename : str
            The filename of the generated output.

        nodes_visited : list
		    A list of the nodes visited to form the path.
		
		network : networkx.Graph
            The graph that contains the node and edge information

		roads : list
			A list of the roads taken.

	'''

	np.savetxt(filename+'.txt', nodes_visited, delimiter = "", newline = "\n", fmt="%s")

	plot_path(auckland, roads, save=filename)


	
def list_splitter(list, network, longitude, latitude):
	''' This function splits a list into four sub-lists based on longitude and latitude of the nodes within.
		
		Parameters
		----------
		list : list
            Original list to be split.
		
		network : networkx.Graph
            The graph that contains the node and edge information.
		
		longitude : float
			Longitude value to split east and west.

		latitude : float
			Latitude value to split north and south.

		Returns
		-------
		list_1-4 : list
			Four separate lists 

	'''	
	list_east = []
	list_west = []
	# split into east and west
	for i in rest_homes:
		if network.nodes[i]['lng'] < 174.78:
			list_west.append(i)
		else:
			list_east.append(i)
	
	# split into east and west lists into north and west
	list_1 = []
	list_2 = []
	list_3 = []
	list_4 = []
	for i in list_west:
		if network.nodes[i]['lat'] < -36.87:
			list_1.append(i)
		else:
			list_2.append(i)
	for i in list_east:
		if network.nodes[i]['lat'] < -36.95:
			list_3.append(i)
		else:
			list_4.append(i)

	return list_1, list_2, list_3, list_4


route_1, route_2, route_3, route_4 = list_splitter(rest_homes, auckland, 174.7, -36.9)

# route 1
n1, l1, r1 = nearest_neighbour_algorithm(auckland, 'Auckland Airport', route_1)
print(l1)
text_map_gen('path_1', n1, auckland, r1)

# route 2
n2, l2, r2 = nearest_neighbour_algorithm(auckland, 'Auckland Airport', route_2)
print(l2)
text_map_gen('path_2', n2, auckland, r2)

# route 3
n3, l3, r3 = nearest_neighbour_algorithm(auckland, 'Auckland Airport', route_3)
print(l3)
text_map_gen('path_3', n3, auckland, r3)

# route 4
n4, l4, r4 = nearest_neighbour_algorithm(auckland, 'Auckland Airport', route_4)
print(l4)
text_map_gen('path_4', n4, auckland, r4)

# end time
t1 = time()

print('Completion time: {:3.2f} seconds'.format(t1-t0))