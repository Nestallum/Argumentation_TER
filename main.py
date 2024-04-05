# main.py

"""
This Python script defines a main function that orchestrates the process of generating a debate graph, initializing agents, generating all possible agent order combinations, and running the protocol for each combination. 

This enables subsequent analysis of results based on the order of agents.

Authors: Mohamed AZZAOUI, Nassim LATTAB
Date of Creation: 20/03/2024
"""

from src.game import *

def main():
    choice = input("Generate or Replay a debate? (G/R): ")
    if choice == 'G':
        nb_agents = int(input("How many agents?")) 
        generate_debate(nb_agents)
    elif choice == 'R':
        debate_number = input("Number of the debate to replay?: ")
        replay_debate(debate_number)
    else:
        print("error.")
        sys.exit(1)
    
if __name__ == "__main__":
    main()

