# game.py

"""
This Python script simulates a debate game.

Authors: Mohamed AZZAOUI, Nassim LATTAB
Creation Date: 21/03/2024
"""

from agent import *
from util import *

def auto_generated_game(UG, number_of_agents) -> float:
    """
    Simulates a debate game with automatically generated agents and argumentation frameworks.
    
    Args:
    - UG (dict): The Universe Graph representing the argumentation framework.
    - number_of_agents (int): The number of agents participating in the debate.

    Returns:
    - float: The final value of the issue of the debate.
    """
    
    # Initialize agents and public graph.
    agents = []
    PG = {"i":[]}
    previous_PG = {}
    
    # Create agents with automatically generated OG.
    for i in range(number_of_agents):
        OG = auto_generate_OG(UG)
        agents.append(agent(i, OG, UG))
        
    nb_turn = 0 

    # Run the debate until no arguments are presented in a turn.
    while(PG != previous_PG):
        print("\n" + "-"*60)
        nb_turn += 1
        previous_PG = PG

        print(f"\n* TURN NUMBER {nb_turn}:")

        # Iterate through each agent to make their move.
        for i in range(number_of_agents):
            print(f"\n{'- Turn of ' + agents[i].name + ' :':^40}")
            PG = agents[i].best_next_move(PG, UG)

    # Debate conclusion.
    print("\nSince none of the agents presented any arguments throughout an entire turn, the debate concludes.")
    final_Vp = Hbs(PG, "i")
    print(f"final value of the issue Vp : {final_Vp}\n")

    return final_Vp


def self_generated_game(UG, agents) -> float:
    """
    Simulates a debate game with user-defined agents and argumentation frameworks.
    
    Args:
    - UG (dict): The Universe Graph representing the argumentation framework.
    - agents (list): List of agent objects representing participants in the debate.

    Returns:
    - float: The final value of the issue of the debate.
    """
    
    nb_turn = 0 

    # Run the debate until no arguments are presented in a turn.
    while(PG != previous_PG):
        nb_turn = +1
        previous_PG = PG

        print(f"\n* TURN NUMBER {nb_turn}:")

        # Iterate through each agent to make their moves.
        for i in range(len(agents)):
            print(f"\n{'- Turn of ' + agents[i].name + ' :':^40}")
            PG = agents[i].best_next_move(PG, UG)
        
    # Debate conclusion.
    print("\nSince none of the agents presented any arguments throughout an entire turn, the debate concludes.")
    final_Vp = Hbs(PG, "i")
    print(f"final value of the issue Vp : {final_Vp}\n")

    return final_Vp

universe_graph={"i":["a","b","c"], "b":["e"], "a":["d"], "c":[], "e":[], "d":[]}
auto_generated_game(universe_graph, 4)