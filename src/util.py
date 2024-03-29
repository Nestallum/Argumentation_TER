# util.py

"""
This Python script contains utility methods for processing and analyzing debate data.

Authors: Mohamed AZZAOUI, Nassim LATTAB
Creation Date: 19/03/2024
"""

from itertools import permutations

def build_attackers_adjacency_list(OG, UG) -> dict:
    """
    Builds and returns the adjacency list of attackers for arguments in OG based on UG.

    Args:
        OG (dict): The subgraph represented as a dictionary.
        UG (dict): The universe graph represented as a dictionary.

    Returns:
        dict: The adjacency list of attackers for arguments in OG.
        Key : attacking argument, Value : list of attacked arguments (may be empty).
    """

    attackers_adjacency_list = {}

    for OG_key in OG.keys():
        attackers_adjacency_list[OG_key] = []
        for UG_key, UG_value in UG.items() :
            if(OG_key in UG_value):
                attackers_adjacency_list[OG_key].append(UG_key)
                
    return attackers_adjacency_list

import networkx as nx
# Variables for the star graphs
nb_branch_star_min = 6
nb_branch_star_max = 15

# Variables for the random trees
nb_arg_tree_min = 1
nb_arg_tree_max = 6

def debate_graph_generation():
    """
    Generates a graph in the form of an online debate. This type of graph is characterised by a target 
    argument and several branches converging towards this argument. 
    In order to build such a graph, a directed star graph is first created (via networkx) where the 
    central node is the target argument. For each branch of the star, a random tree is generated 
    (also via networkx) containing a random number of nodes.
    """

    nb_branch_star = random.randrange(nb_branch_star_min, nb_branch_star_max+1)
    cpt = nb_branch_star #allows for a gradual increase in the number of arguments

    star = nx.generators.star_graph(nb_branch_star)
    star = nx.DiGraph([(u,v) for (u,v) in star.edges()]).reverse()


    for nodes_star in range(1, nb_branch_star+1):
        nb = random.randrange(nb_arg_tree_min, nb_arg_tree_max)
        labels = {i: cpt+i for i in range(1, nb)}
        labels[0] = nodes_star
        
        random_tree = nx.generators.trees.random_tree(nb, create_using=nx.DiGraph).reverse()
        random_tree = nx.relabel_nodes(random_tree,labels)
        star.add_nodes_from(random_tree)
        star.add_edges_from(random_tree.edges)
        cpt += nb-1

    return star

def generate_subgraph(UG: dict, arguments: list) -> dict:
    """
    Generates a subgraph (opinion graph OG) from the given universe graph (UG)
    composed of the specified list of arguments.

    Args:
        UG (dict): The universe graph represented as a dictionary.
        arguments (list): The list of arguments to include in the subgraph.

    Returns:
        dict: The subgraph (OG) containing only the specified arguments and their relations from UG.
    """
    OG = {}

    # Create the subgraph of UG composed of the list of arguments in parameters.
    for arg in arguments:
        # Find the common arguments (intersection) between the specified arguments and the arguments in UG[arg].
        common_args = list(set(arguments) & set(UG[arg]))
        OG[arg] = common_args

    return OG

import random

def auto_generate_OG(UG: dict) -> dict:
    """
    Automatically generates a subgraph (OG) from the given universe graph (UG) 
    by randomly selecting a subset of arguments from UG.

    Args:
        UG (dict): The universe graph represented as a dictionary.

    Returns:
        dict: The subgraph (OG) containing a randomly selected subset of arguments from UG, 
              including the issue argument '0'.
    """

    # Extract all arguments we want to randomly select except for the issue argument.
    args = list(UG.keys()) 
    args.remove('0')

    # Randomly pick a number of args to add for our OG.
    nb_args_to_add = random.randint(1, len(args))

    # Choose random arguments to add to the subgraph.
    selected_args = random.sample(args, nb_args_to_add)

    # Once we have our random args, add the issue arg.
    selected_args.append('0') 

    return generate_subgraph(UG, selected_args)

def Hbs(graph: dict, argument: str) -> float:
    """ 
    Calculates and returns the Belief Strength (Hbs) of an argument.

    Args:
        graph (dict): The graph represented as a dictionary.
        argument (str): The argument for which to calculate the Belief Strength (Hbs).

    Returns:
        float: The Belief Strength (Hbs) of the argument.
    """
    
    # If nobody attacks the argument, the value is of its Hbs is 1.
    if len(graph[argument]) == 0: 
        return 1
    
    else:
        # Sum the Belief Strengths (Hbs) of all attacking arguments.
        total_hbs = 0                  
        for a in range(len(graph[argument])):
            total_hbs += Hbs(graph, graph[argument][a])
            
        # Calculate and return the Belief Strength (Hbs) of the argument.
        return 1 / (1 + total_hbs)
    
def agent_order_combinations(agents: list) -> list:
    """
    Generates all possible permutations of agent orderings from the given list of agents.

    Args:
        agents (list): A list of agent objects.

    Returns:
        list: A list containing all possible permutations of agent orderings.
    """

    # Generate all possible permutations of agent indices.
    agent_indices = range(len(agents))
    permutations_indices = permutations(agent_indices)

    # For each permutation of indices, create a corresponding list of agents.
    agent_combinations = []
    for perm_indices in permutations_indices:
        agent_order = [agents[i] for i in perm_indices]
        agent_combinations.append(agent_order)

    return agent_combinations

def Hbs2(graph: dict, argument: str) -> float:
    """
    Implements the Harmony-based System (Hbs) algorithm to compute the harmony score for a given argument in a debate graph.

    Args:
        graph (dict): The debate graph represented as a dictionary.
        Keys represent arguments, and values represent lists of attacking arguments.
        argument (str): The argument for which the harmony score is to be computed.

    Returns:
        float: The harmony score for the specified argument.
    """

    # Initialize previous steps dictionary with initial harmony scores for each argument
    prev_steps = {k: [1] for k in graph.keys()}

    # Define convergence threshold
    diff = 10**(-1)

    # Initialize variables
    prev_score = len(graph.keys())
    score = 0
    boolean = True
    step = 0

    # Main iteration loop until convergence
    while(boolean):
        # Compute harmony scores for all arguments
        for key, value in graph.items():
            if len(value) == 0:
                prev_steps[key].append(1)
            else:
                sum = 0
                for j in value:
                    sum += prev_steps[j][step]
                prev_steps[key].append(1 / (1 + sum))

        # Calculate total harmony score
        sum = 0
        for value in prev_steps.values():
            sum += value[step]
        score = sum

        # Check convergence
        if abs(score - prev_score) <= diff:
            boolean = False
            
        prev_score = score
        step += 1

    # Return the harmony score for the specified argument
    return prev_steps[argument][step]

