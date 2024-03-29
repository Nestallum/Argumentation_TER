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
import numpy as np 
import pandas as pd

def main():
    # Generate the debate graph as a networkx.classes.digraph.DiGraph
    generated_graph = debate_graph_generation()
    
    # Export the networkx.classes.digraph.DiGraph to an APX file into a subfolder of the results folder and returns it
    debate_results = export_apx_UG("universe_graph", generated_graph)

    # Read the universe graph from the APX file
    universe_graph = read_UG_from_apx("results/"+ debate_results +"/universe_graph.apx")
    
    # Initialize agents with the universe graph
    number_of_agents = 4
    agents = initialize_agents(universe_graph, number_of_agents)
    
    # Generate all agent order combinations
    agent_combinations = agent_order_combinations(agents)

    j = 0
    data={"order":[], "Vp":[], "numberOfTurn":[]}
    for a in agents:
            export_apx_OG(debate_results, f"opinion_graph {j}", a.OG)
            data[a.get_number()]=[]
            j+=1
    
    # Run the protocol for each agent order combination
    for agent_order in agent_combinations:
        
        vp, public_graph, order, agents, nb_turn = run_protocol(universe_graph, agent_order)

        # Export results in apx and csv
        export_apx_OG(debate_results, order, public_graph)
        data["order"].append(order)
        data["Vp"].append(vp)
        data["numberOfTurn"].append(nb_turn)
        for a in agents:
            data[a.get_number()].append(a.in_comfort_zone(public_graph))
    
    df = pd.DataFrame(data)
    df.to_csv("results/"+ debate_results +"/data.csv", index=False)

if __name__ == "__main__":
    main()

