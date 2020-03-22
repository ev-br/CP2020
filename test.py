import networkx as nx
import re

import numpy as np

g = nx.Graph()


s = input()
s = re.split(" ", s)
array = []

for i in range(0, len(s), 2):
    array.append ((s[i], s[i + 1]))

g.add_edges_from(array)
ans = nx.number_connected_components(g)
print(ans)

