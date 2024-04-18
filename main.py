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
        debate_number = input("Path of the debate?: ")
        choice_0 = input("Replay with just the Same UG Y/N ")
        if choice_0 == 'Y' :
            number=input("How many agents ? ")
            replay_debate_just_with_UG(debate_number,int(number))
        else :
            choice = input("Replay all combinations of agent order? (Y/N)")
            if choice == 'Y': 
                replay_debate(debate_number)
            elif choice == 'N':
                combination = input("Enter a valid combination (id_agent1,id_agent2,...): ")
                replay_combination(debate_number, combination)
            else:
                print("error.")
                sys.exit(1)
    else:
        print("error.")
        sys.exit(1)
    
if __name__ == "__main__":
    main()

