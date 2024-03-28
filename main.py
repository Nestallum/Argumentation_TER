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
    
    
    # Export the networkx.classes.digraph.DiGraph to an APX file
    folder_results= export_apx_UG("universe_graph", generated_graph)
    print(folder_results)

    # Read the universe graph from the APX file
    universe_graph = read_UG_from_apx("results/"+ folder_results +"/universe_graph.apx")
    
    # Initialize agents with the universe graph
    agents = initialize_agents(universe_graph, 5)
    
    # Generate all agent order combinations
    agent_combinations = agent_order_combinations(agents)
    j = 0
    data={"ordre_agents":[],"Vp":[],"numberOfTurn":[]}
    for i in agents:
            export_apx_OG(folder_results,f"opinion_graph {j}", i.OG)
            data[i.get_number()]=[]
            j=j+1
    
    # Run the protocol for each agent order combination
    for agent_order in agent_combinations:
        
        vp, public_graph,ordre_names,agents,nb = run_protocol(universe_graph, agent_order)
        print(ordre_names)
        export_apx_OG(folder_results,ordre_names, public_graph)
        data["ordre_agents"].append(ordre_names)
        data["Vp"].append(vp)
        data["numberOfTurn"].append(nb)
        for i in agents :
            data[i.get_number()].append(i.in_comfort_zone(public_graph))
        
        # enregistrer chaque vp et son public_graph associé quelque part...
    df = pd.DataFrame(data)
    print(folder_results)
    df.to_csv("results/"+ folder_results+"/data.csv", index=False)
if __name__ == "__main__":
    main()

