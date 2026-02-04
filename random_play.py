
from nimber_calc import read_vertex_weighted_graph as read_graph
import networkx as nx
import random

if __name__ == "__main__":
    if input("Read graph from input? (y/n): ").lower() == 'y':
        graph = read_graph()
        config = tuple(data['weight'] for _, data in graph.nodes(data=True))
    else:
        config = tuple(map(int, input("Enter the initial config (space-separated): ").split()))
        graph = nx.complete_graph(len(config))
        for i in range(len(config)):
            graph.nodes[i]['weight'] = config[i]

    weight = sum(config)
    size = len(config)
    while weight > 0:
        print(f'Current config: {config}, total weight: {weight}')

        nonzero_indices = [i for i, w in enumerate(config) if w > 0]
        node = nonzero_indices[random.randint(0, len(nonzero_indices) - 1)]

        
        
        remove = random.randint(1, config[node])
        config = list(config)
        config[node] -= remove
        config = tuple(config)
        weight -= remove