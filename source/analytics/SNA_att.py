import matplotlib.pyplot as plt
import networkx as nx
import csv

G=nx.Graph()

#extract and add COLUMN1 nodes in graph
f1 = csv.reader(open("att_tab.csv","rb"))
for row in f1:
    G.add_nodes_from(row, color = 'blue')

#extract and add COLUMN2 nodes in graph
f2 = csv.reader(open('user_country.txt','rb')) #We would fetch from the same file/table
for row in f2:
    G.add_nodes_from(row, color = 'red')

#extract and add COLUMN3 nodes in graph
f3 = csv.reader(open('user_id.txt','rb'))
for row in f3:
    G.add_nodes_from(row, color = 'yellow')

#extract and add COLUMN4 nodes in graph
f4 = csv.reader(open('id,agegroup.txt','rb'))
for row in f4:
    if len(row) == 2 : # add an edge only if both values are provided
        G.add_edge(row[0],row[1])

f5 = csv.reader(open('id,country.txt','rb'))

for row in f5:
    if len(row) == 2 : # add an edge only if both values are provided
        G.add_edge(row[0],row[1])
# Remove empty nodes
for n in G.nodes():
    if n == '':
        G.remove_node(n)
# color nodes according to their color attribute
color_map = []
for n in G.nodes():
    color_map.append(G.node[n]['color'])
nx.draw_networkx(G, node_color = color_map, with_labels = True, node_size = 500)

plt.show()