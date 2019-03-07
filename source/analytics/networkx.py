#Sample relationships from actions table

import networkx as nx

G_weighted = nx.Graph()
G_weighted.add_edge('IOT','IOT', weight=25) #Weight represents the amount of incidences
G_weighted.add_edge('IOT','Call', weight=8)
G_weighted.add_edge('IOT','Letter', weight=11)
G_weighted.add_edge('IOT','Mail', weight=1)
G_weighted.add_edge('IOT','Pedro', weight=4)
G_weighted.add_edge('IOT','Mail',weight=7)
G_weighted.add_edge('IOT','Disruption', weight=1)
G_weighted.add_edge('Mail','Call',weight=1)

nx.draw_networkx(G_weighted)

