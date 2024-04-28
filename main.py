# main.py

"""
This Python script defines a main function that orchestrates the process of generating a debate graph, initializing agents, generating all possible agent order combinations, and running the protocol for each combination. 

This enables subsequent analysis of results based on the order of agents.

Authors: Mohamed AZZAOUI, Nassim LATTAB
Date of Creation: 20/03/2024
"""

from src.game import *

def main():

    generate_debate(1)
    # replay_debate("results/debate_2", 6)
    for agents in range(2,9):
        for _ in range(4):
          replay_debate_with_new_agents("results/debate_2", agents)
            
    
if __name__ == "__main__":
    main()

