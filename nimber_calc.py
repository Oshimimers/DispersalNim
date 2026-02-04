from functools import reduce
import networkx as nx
import pprint
import random
import numpy as np

def read_vertex_weighted_graph():
    """
    Reads a vertex-weighted graph from user input.
    Returns a NetworkX graph with vertex weights stored as node attributes.
    """
    G = nx.Graph()
    
    print("Enter the vertex weights (space-separated):")
    state = tuple(map(int, input().split()))
    
    for i in range(len(state)):
        G.add_node(i, weight=state[i])
    
    print("Enter the edges (adjacent vertices separated by comma, format: u,v w,z):")
    edges = input().split()
    for edge in edges:
        u, v = map(int, edge.split(","))
        G.add_edge(u, v)
    
    return G

def mex(set_of_nimbers):
    """Calculates the Minimum Excludant (mex) of a set of nimbers."""
    i = 0
    # Search for the smallest non-negative integer not in the set
    while i in set_of_nimbers:
        i += 1
    return i

def compositions(tokens, parts):
    """
    Generates all ways to distribute 'tokens' indistinguishable items into 'parts' distinguishable boxes.
    
    Args:
        tokens (int): Number of indistinguishable items (tokens).
        parts (int): Number of distinguishable boxes (neighbors).
        
    Returns:
        list: A list of distributions of tokens into parts.
    """
    comps = []

    if parts == 1:
        comps.append([tokens])
        return comps
    for i in range(tokens + 1):
        for comp in compositions(tokens - i, parts - 1):
            comps.append([i] + comp)
    return comps

def get_next_states(G, current_state):
    """
    Generates all possible next game states from the current_state.

    Args:
        G (nx.Graph): The underlying graph.
        current_state (tuple): Token count on each vertex (must match G's node order).

    Yields:
        tuple: A reachable next game state.
    """

    # Iterate over every vertex v that has at least one token
    for v, tokens_on_v in enumerate(current_state):
        if tokens_on_v == 0:
            continue

        neighbors = list(G.neighbors(v))

        for distribution in compositions(tokens_on_v-1, len(neighbors)+2):
            # remove at least one token from v
            # distribution is a list of length len(neighbors)+2
            # The second to last element is the number of tokens removed from v (k)
            # The last element is the number of tokens left on v
            # The middle elements correspond to the neighbors in order
            
            # Create the next state
            next_state_list = list(current_state)
            
            for nbr_idx, nbr in enumerate(neighbors):
                next_state_list[nbr] += distribution[nbr_idx]
            
            next_state_list[v] = distribution[-1]

            yield tuple(next_state_list)

       
def grundy(G, current_state, memo, moves):
    """
    Calculates the Grundy number (nimber) of a game state.
    
    Args:
        G (nx.Graph): The underlying graph.
        current_state (tuple): The game state (must be hashable for memoization).
        memo (dict): Dictionary for memoization: {state: nimber}.
        
    Returns:
        int: The Grundy number of the state.
    """
    
    # 1. Check Memoization Table
    if current_state in memo:
        return memo[current_state]

    # 2. Base Case: Terminal State
    # If a state is terminal (no tokens left), its Grundy number is 0.
    if sum(current_state) == 0:
        memo[current_state] = 0
        return 0

    # 3. Recursive Step: Find Grundy numbers of next states
    nimbers_of_next_states = set()
    
    # Iterate over all reachable next states
    for next_state in get_next_states(G, current_state):
        # Recursively find the Grundy number of the next state

        # moves.add_edge(current_state, next_state)
        next_nimber = grundy(G, next_state, memo, moves)
        nimbers_of_next_states.add(next_nimber)

    # 4. Calculate the Grundy number for the current state (mex)
    current_nimber = mex(nimbers_of_next_states)
    
    # 5. Store result and return
    memo[current_state] = current_nimber
    return current_nimber

def optimal_game(G, state, memo):
    current_state = state
    while sum(current_state) > 0:
        current_nimber = memo[current_state]
        print(f'Current state: {current_state}, Tokens: {sum(current_state)}, Nimber: {current_nimber}')
        previous_state = current_state
        if current_nimber == 0:
            current_state = list(get_next_states(G, current_state))[random.randint(0, len(list(get_next_states(G, current_state))) - 1)]
            # continue
        else:
            optimal_states = []
            for next_state in get_next_states(G, current_state):
                next_nimber = memo[next_state]
                if next_nimber == 0:
                    optimal_states.append(next_state)
            optimal_moves = [tuple(np.array(s) - np.array(previous_state)) for s in optimal_states]
            print(f'   Optimal states: {optimal_states} \n')
            print('   Optimal moves: ', optimal_moves)
            current_state = optimal_states[random.randint(0, len(optimal_states) - 1)]
        move = tuple(np.array(current_state) - np.array(previous_state))
        print(f'   Move made: {move} \n')

if __name__ == "__main__":
    if input("Read graph from input? (y/n): ").lower() == 'y':
        graph = read_vertex_weighted_graph()
        config = tuple(data['weight'] for _, data in graph.nodes(data=True))
    else:
        group1 = tuple(map(int, input("Enter the weights for group 1 (space-separated): ").split()))
        group2 = tuple(map(int, input("Enter the weights for group 2 (space-separated): ").split()))
        graph = nx.complete_bipartite_graph(len(group1), len(group2))
        config = group1 + group2
        # config = tuple(map(int, input("Enter the initial config (space-separated): ").split()))
        # graph = nx.complete_bipartite_graph(len(config))
        for i in range(len(config)):
            graph.nodes[i]['weight'] = config[i]

    print('\n', "Graph nodes with weights:", graph.nodes(data=True), '\n')
    print("Graph edges:", graph.edges(), '\n')
    
    memo = {}
    movesets = nx.DiGraph()

    result = grundy(graph, config, memo, movesets)

    print("Grundy number of the initial state:", result)
    print(f'{len(memo)} configurations analyzed.')

    with open(f'memo{str(config)}.txt', 'w') as f:
        f.write(graph.edges().__str__() + 2*'\n')
        for state, nimber in memo.items():
            f.write(f'{state}: {nimber}\n')

    # print(f'{len(movesets.nodes)} states in the game tree.')
    # for state in movesets.nodes():
    #     movesets.nodes[state]['label'] = str(state) + f'{memo[state]}'
    #     movesets.nodes[state]['tokens'] = sum(state)
    #     movesets.nodes[state]['grundy'] = memo[state]

    # differences = {}
    # agreements = {}
    p_positions = {}
    for state, nimber in memo.items():
    #     if reduce(lambda i, j: int(i) ^ int(j), state) != nimber:
    #         differences[state] = nimber
    #         movesets.nodes[state]['xor'] = 0
    #     else:
    #         agreements[state] = nimber
    #         movesets.nodes[state]['xor'] = 1
        if nimber == 0:
            p_positions[state] = nimber

    # print(f'{len(differences)} differences found:')
    # # pprint.pprint(differences, width=40)
    # # print(differences)
    # print(f'{len(agreements)} agreements found:')
    # # pprint.pprint(agreements, width=40)
    # # print(agreements)

    print(f'{len(p_positions)} P-positions found:')
    # print(list(p_positions.keys()), "\n")
    # pprint.pprint(p_positions, width=40)

    # if input("Write game tree to GEXF file? (y/n): ").lower() == 'y':
    #     print(" ")
    #     nx.write_gexf(movesets, f'movesets{str(config)}.gexf')
    
    g = 0
    play = True
    while play:
        print(f'   Game {g + 1}:')
        optimal_game(graph, config, memo)
        g += 1
        if input("Play another game? (y/n): ").lower() != 'y':
            play = False
