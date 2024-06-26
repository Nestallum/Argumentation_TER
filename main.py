# main.py

"""
This Python script defines a main function that orchestrates the process of generating a debate graph, initializing agents, generating all possible agent order combinations, and running the protocol for each combination. 

This enables subsequent analysis of results based on the order of agents.

Authors: Mohamed AZZAOUI, Nassim LATTAB
Date of Creation: 20/03/2024
"""

from src.game import *

def main():
    for i in range(1, 11):
        generate_debate(1)
        for agents in range(2, 8):
            for _ in range(20):
                replay_debate_with_new_agents(f"results/debate_{i}", agents, f"csv_iteration_{i}")
            
    
if __name__ == "__main__":
    main()

