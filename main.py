# main.py

"""
This Python script defines a main function that orchestrates the process of generating a debate graph, initializing agents, generating all possible agent order combinations, and running the protocol for each combination. 

This enables subsequent analysis of results based on the order of agents.

Authors: Mohamed AZZAOUI, Nassim LATTAB
Date of Creation: 20/03/2024
"""

from src.game import *

def main():

    # generate_debate(6)
    replay_debate("results/debate_2", 1)
    # for agent in range(2,9):
    #     for _ in range(4):
    #         replay_debate_just_with_UG("results/debate_1", agent)
            
    
if __name__ == "__main__":
    main()

