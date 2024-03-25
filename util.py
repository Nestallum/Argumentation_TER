# util.py
from itertools import permutations

"""
This Python script contains utility methods for processing and analyzing debate data.

Authors: Mohamed AZZAOUI, Nassim LATTAB
Creation Date: 19/03/2024
"""

universe_graph={"i":["a","b","c"],"b":["e"],"a":["d"],"c":[],"e":[],"d":[]}
opinion_graph={"i":["d"],"d":[]}
arguments=["a","i","b","d"]

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
              including the issue argument 'i'.
    """

    # Extract all arguments we want to randomly select except for the issue argument.
    args = list(UG.keys()) 
    args.remove('i')

    # Randomly pick a number of args to add for our OG.
    nb_args_to_add = random.randint(1, len(args))

    # Choose random arguments to add to the subgraph.
    selected_args = random.sample(args, nb_args_to_add)

    # Once we have our random args, add the issue arg.
    selected_args.append('i') 

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

    #print(universe_graph)
    #print(auto_generate_OG(universe_graph))
    #print(build_attackers_adjacency_list(opinion_graph, universe_graph))
    
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

def Hbs2(graph: dict, argument: str):
    
    prevSteps={k: [1] for k in graph.keys()}
    diff=10**(-4)
    prevscore=10
    score=0
    boolean=True
    step=0
    while(boolean):
        #etape 1 tout els arguments pas attaquer a 1
        for key,value in graph.items():
            if (len(value)==0):
                prevSteps[key].append(1)
            else:
                sum=0
                for j in value:
                    sum=sum+prevSteps[j][step]
                prevSteps[key].append(1/(1+sum))
        sum=0
        for value in prevSteps.values() : 
            sum=sum+value[step]
        score=sum
        if(abs(score-prevscore)<=diff):
            boolean=False
        prevscore=score
        step=step+1
    return prevSteps[argument][step]

print(Hbs2(universe_graph,"i"))
