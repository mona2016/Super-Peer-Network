'''
This program creates a real network wherein every node is 
'''


table={}
import util
for n in range(0,100,1):
	A = util.random_list(n,0,99)


import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt2
import random


def real_network(A):
	G=nx.Graph()
	list_of_nodes = []
	coordinates = []
	for i in range(100):
		x=random.choice(range(100))
		y=random.choice(range(100))
		while (x,y) in coordinates:
			x=random.choice(range(100))
			y=random.choice(range(100))
		coordinates=coordinates+[(x,y)]
		G.add_node(i, posxy=(coordinates[i][0],coordinates[i][1]))
		list_of_nodes=list_of_nodes+[i]
	G.add_cycle(list_of_nodes)
	
	#B = assign_neighbors()
	#G.add_edges_from(B)
	positions=nx.get_node_attributes(G,'posxy')
	
	return G

# returns a two dimentional array that represts the edges
def assign_neighbors():
	for i in range(len(A)):
		C=list(set([random.choice(A) for x in range(2)]))
		table[i]=C
	B=[]
	for i in range(len(table)):
		C=[]
		C=check_selfLoop([(i,x) for x in table[i]])
		B=B+C
	return B

#checks and removes the edges that are self loops and returns the list of edges without self loop
def check_selfLoop(C):
	D=[]
	for j in range(len(C)):
		if C[j][0]==C[j][1]:
			D=D+[(C[j][0],C[j][1])]
	for j in range(len(D)):
		C.remove(D[j])
	return C

def shortest_path(G,start_node,target_node):
	if start_node==target_node:
		return [start_node]
	path=nx.shortest_path(G,start_node,target_node)
	length=nx.shortest_path_length(G,start_node,target_node)
	print("path: ",path)
	print("length: ",length)
	return path


def create_superPeer(G, positions,key_set):
	
	print("superPeer nodes are: ",key_set)
	H=nx.Graph()
	H.add_nodes_from(G.nodes())
	edges=[]
	for n in G.nodes():
		length={}
		minimum=200
		for i in key_set:
			H.add_edges_from([i,x] for x in key_set if i!=x)
			length[i]=nx.shortest_path_length(G,i,n)
			if length[i]<minimum:
				minimum=length[i]
		for key in length.keys():
			if length[key]==minimum:
				H.add_edge(key,n)
				edges=edges+[(key,n)]
	#H.add_edges_from(edges)
	return H

	


def main():
	#plt.show()
	print("\n\nThis application uses Networkx and Matplotlib to create a real network and an \noverlay network to show the shortest path between nodes")
	print("\nIn the real network, each node is connected to only two other nodes. I have \nmade the program this way to make the UI more readable and avoid the mesh structure \nwith too many edges between nodes")
	print("\nThe matplotlib window can be maximized, minimized and has functionlities of \nzooming into the network graph")
	print("\n")
	G=real_network(A)
	positions = nx.get_node_attributes(G,'posxy')
	number = int(input("Enter the number of super peers: "))
	key_set=list(set([random.choice(G.nodes()) for x in range(number)]))
	H=create_superPeer(G,positions,key_set)
	still_going=True
	
	#show options: 1. draw real network 2. show super peer network 3. shortest path in real and super peer
	while(still_going==True):
		print("Please choose one of the following: ")
		print("1. view the real network")
		print("2. view the super peer overlay network")
		print("3. view the shortest path between two nodes on both network")
		choice = input("Enter your choice: ")
		if choice.strip()=='1':
			fig1 = plt.figure()
			ax1 = fig1.add_subplot()
			nx.draw(G,positions,node_size=500,with_labels=True, ax=ax1)
			#mng = plt.get_current_fig_manager()
			#mng.frame.Maximize(True)
			plt.show()
			contd = input("Do you want to continue?(y/n) ")
			if contd=="n":
				still_going=False

		#to display super peer network
		elif choice.strip()=='2':
			print("Two graph windows will appear, one on top of other, one will show real network and other will show super peer network")
			print("The colored nodes are super peer nodes")
			print("superPeer nodes are: ", key_set)
			path=key_set
			path_edge=[]
			for node in range(len(path)-1):
				path_edge=path_edge+[(path[node], path[node+1])]

			fig1 = plt.figure()
			ax1 = fig1.add_subplot()
			nx.draw(G,positions, node_size=500,with_labels=True,ax=ax1)

			fig2 = plt.figure()
			ax2 = fig2.add_subplot()
			nx.draw_networkx_edges(H,positions,
                    		   edgelist=path_edge,
                    		   width=5,edge_color="#00aa00")
			nx.draw(H,positions, node_size=500,with_labels=True,ax=ax2)
			nx.draw_networkx_nodes(H,positions,
                    		   nodelist=path,
                    		   node_color="#00aa00",
                    		   node_size=500)
			
			
			plt.show()

			contd = input("Do you want to continue?(y/n) ")
			if contd=="n":
				still_going=False

		# for showing shortest path
		elif choice.strip()=='3':
			print("Two graph windows will appear, one on top of other, one will show real network and other will show super peer network ")
			print("superPeer nodes are: ", key_set)
			s = int(input("Start: "))
			e = int(input("End: "))

			# for real network
			path=shortest_path(G,s,e)
			
			path_edge=[]
			
			for node in range(len(path)-1):
				path_edge=path_edge+[(path[node], path[node+1])]

			fig1 = plt.figure()
			ax1 = fig1.add_subplot()
			nx.draw_networkx_edges(G,positions,
                    		   edgelist=path_edge,
                    		   width=5,edge_color="#FFFF00")
			
			nx.draw(G,positions, node_size=500,with_labels=True,ax=ax1)
			nx.draw_networkx_nodes(G,positions,
                    		   nodelist=path,
                    		   node_color="#FFFF00",
                    		   node_size=500)

			# for overlay network
			path=shortest_path(H,s,e)
	
			path_edge=[]
			for node in range(len(path)-1):
				path_edge=path_edge+[(path[node], path[node+1])]

			
			fig2 = plt.figure()
			ax2 = fig2.add_subplot()
			nx.draw_networkx_edges(H,positions,
                    		   edgelist=path_edge,
                    		   width=5,edge_color="#FFFF00")
			
			nx.draw(H,positions, node_size=500,with_labels=True,ax=ax2)
			nx.draw_networkx_nodes(H,positions,
                    		   nodelist=key_set,
                    		   node_color="#00aa00",
                    		   node_size=500)
			plt.show()
			contd = input("Do you want to continue?(y/n) ")
			if contd=="n":
				still_going=False

if __name__ == '__main__':
	main()



