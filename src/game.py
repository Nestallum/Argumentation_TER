# game.py

"""
This Python script simulates a debate game.

Authors: Mohamed AZZAOUI, Nassim LATTAB
Creation Date: 21/03/2024
"""

from src.agent import *
from src.util import *

def initialize_agents(UG, number_of_agents) -> list:
    """
    Initializes a list of agents to participate in the debate.

    Args:
    - UG (dict): The universe graph representing the entire argumentation framework.
    - number_of_agents (int): The number of agents participating in the debate.

    Returns:
    - list: A list of initialized agents with automatically generated argument graphs (AGs).
    """
    
    # Initialize agents.
    agents = []
    
    # Create agents with automatically generated OG.
    for k in range(number_of_agents):
        OG = auto_generate_OG(UG)
        agents.append(agent(k, OG, UG))

    return agents

def run_protocol(UG, agents) -> float | dict:
    """
    Simulates a debate game with automatically generated agents and argumentation frameworks.
    
    Args:
    - UG (dict) : The universe graph representing the entire argumentation framework.
    - agents (list) : The list of the agents participating in the debate.

    Returns:
    - float: The final value of the issue of the debate.
    - dict : The final PG.
    - str : The names of the agents
    - list : The list of agents
    - int : number of turn needed to end the debate.
    """

    nb_turn = 0 
    PG = {"0":[]} # Initialize public graph.
    previous_PG = {}
    number_of_agents = len(agents)
    historic = []

    # Run the debate until no arguments are presented in a turn.
    while(PG != previous_PG):
        print("\n" + "-"*60)
        nb_turn += 1
        previous_PG = PG

        print(f"\n* TURN NUMBER {nb_turn}:")

        # Iterate through each agent to make their move.
        for k in range(number_of_agents):
            print(f"\n{'- Turn of ' + agents[k].name + ' :':^40}")
            PG = agents[k].best_next_move(PG, UG, nb_turn)


    for k in range(number_of_agents):
        historic.append(agents[k].historic)
    print(historic)
    # Debate conclusion.
    print("\nSince none of the agents presented any arguments throughout an entire turn, the debate concludes.")
    final_Vp = Hbs(PG, "0")
    print(f"final value of the issue Vp : {final_Vp}\n")
    
    agent_names = []
    for a in agents:     
        agent_names.append(f"A{a.get_number()}")
            
    agent_names = ",".join(agent_names)   
    return final_Vp, PG, agent_names, agents, nb_turn

def find_all_combinations(agents) -> list:
    """
    Generates all possible combinations of agent orderings from the given list.

    Args:
    - agents (list): A list of agents.

    Returns:
    - list: A list containing all possible combinations of agent orderings.
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
