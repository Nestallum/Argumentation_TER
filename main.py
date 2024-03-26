# main.py

"""
This Python script defines a main function that orchestrates the process of generating a debate graph, initializing agents, generating all possible agent order combinations, and running the protocol for each combination. 

This enables subsequent analysis of results based on the order of agents.

Authors: Mohamed AZZAOUI, Nassim LATTAB
Date of Creation: 20/03/2024
"""

from src.IO_graph_apx import *
from src.agent import *
from src.game import *
from src.util import *

def main():
    # Generate the debate graph as a networkx.classes.digraph.DiGraph
    generated_graph = debate_graph_generation()
    
    # Folder to export results about the debate.
    folder_results = "debate2"

    # Export the networkx.classes.digraph.DiGraph to an APX file
    export_apx(folder_results, "universe_graph", generated_graph)

    # Read the universe graph from the APX file
    universe_graph = read_UG_from_apx("results/"+ folder_results +"/universe_graph.apx")
    
    # Initialize agents with the universe graph
    agents = initialize_agents(universe_graph, 4)
    
    # Generate all agent order combinations
    agent_combinations = agent_order_combinations(agents)
    
    # Run the protocol for each agent order combination
    for agent_order in agent_combinations:
        vp, public_graph = run_protocol(universe_graph, agent_order)
        # enregistrer chaque vp et son public_graph associé quelque part...

if __name__ == "__main__":
    main()

