# game.py

"""
This Python script simulates a debate game.

Authors: Mohamed AZZAOUI, Nassim LATTAB
Creation Date: 21/03/2024
"""

from agent import *
from util import *

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
    """

    nb_turn = 0 
    PG = {"i":[]} # Initialize public graph.
    previous_PG = {}
    number_of_agents = len(agents)

    # Run the debate until no arguments are presented in a turn.
    while(PG != previous_PG):
        print("\n" + "-"*60)
        nb_turn += 1
        previous_PG = PG

        print(f"\n* TURN NUMBER {nb_turn}:")

        # Iterate through each agent to make their move.
        for k in range(number_of_agents):
            print(f"\n{'- Turn of ' + agents[k].name + ' :':^40}")
            PG = agents[k].best_next_move(PG, UG)

    # Debate conclusion.
    print("\nSince none of the agents presented any arguments throughout an entire turn, the debate concludes.")
    final_Vp = Hbs(PG, "i")
    print(f"final value of the issue Vp : {final_Vp}\n")

    return final_Vp, PG

def find_all_combinations(agents) -> list:
    """
    Generates all possible combinations of agent orderings from the given list.

    Args:
    - agents (list): A list of agents.

    Returns:
    - list: A list containing all possible combinations of agent orderings.
    """
    pass  # Placeholder for function implementation
    

universe_graph={"i":["a","b","c"], "b":["e"], "a":["d"], "c":[], "e":[], "d":[]}
agents = initialize_agents(universe_graph, 4)
#run_protocol(universe_graph, agents)
