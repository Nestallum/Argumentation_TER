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

def main(numberOfagent,numberDebate="ALL",combinaison="ALL"):
    if (numberDebate=="ALL" and combinaison=="ALL"):
        # Generate the debate graph as a networkx.classes.digraph.DiGraph
        generated_graph = debate_graph_generation()
        
        # Export the networkx.classes.digraph.DiGraph to an APX file into a subfolder of the results folder and returns it
        debate_results = export_apx_UG("universe_graph", generated_graph)

        # Read the universe graph from the APX file
        universe_graph = read_UG_from_apx("results/"+ debate_results +"/universe_graph.apx")
        
        # Initialize agents with the universe graph
        number_of_agents = numberOfagent
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
                historic_data = []
                historic_data.append(a.in_comfort_zone(public_graph))
                historic_data.append(a.historic)
                data[a.get_number()].append(historic_data)
        
        df = pd.DataFrame(data)
        df.to_csv("results/"+ debate_results +"/data.csv", index=False)
        
    elif (numberDebate!="ALL" and combinaison=="ALL"):
        
        extension = ".apx"
        early_path = "replays/"

        if not os.path.exists(early_path):
            os.mkdir(early_path)

        if not os.path.exists(early_path+"/debate_1"):
            os.mkdir(early_path+"/debate_1")
            folder_name = "debate_1"
        else :
            last_subfolder = 1
            for sub_folder in (glob.glob('replays\*')) :
                if(last_subfolder < int((sub_folder.split("\\"))[1].split("_")[1])):
                    last_subfolder = int((sub_folder.split("\\"))[1].split("_")[1])
            new_val = last_subfolder + 1
            os.mkdir(early_path+f"/debate_{new_val}")
            folder_name = f"debate_{new_val}"
            
        # Create the right subfolder where to put results    
        UG=read_UG_from_apx("results/debate_"+numberDebate+"/universe_graph.apx")
        export_apx_OG(folder_name, f"univers_graph", UG,early_path="replays/")
        agents=[]
        
        for i in range(int(numberOfagent)) :
            new=f"results/debate_{numberDebate}/opinion_graph {i}.apx"
            agents.append(agent(i,read_UG_from_apx(new),UG))
            export_apx_OG(folder_name, f"opinion_graph {i}", agents[i].OG,early_path="replays/")
    
        j = 0
        data={"order":[], "Vp":[], "numberOfTurn":[]}
        for a in agents:
                data[a.get_number()]=[]
                j+=1
        
        agentry=find_all_combinations(agents)
        # Run the protocol for each agent order combination
        for agent_order in agentry:
            
            vp, public_graph, order, agents, nb_turn = run_protocol(UG, agent_order)

            # Export results in apx and csv
            export_apx_OG(folder_name, order, public_graph,early_path="replays/")
            data["order"].append(order)
            data["Vp"].append(vp)
            data["numberOfTurn"].append(nb_turn)
            for a in agents:
                data[a.get_number()].append(a.in_comfort_zone(public_graph))
        
        df = pd.DataFrame(data)
        df.to_csv("replays/"+ folder_name +"/data.csv", index=False)
    
    elif(numberDebate!="ALL" and combinaison!="ALL") :
        
        early_path = "replays/"

        if not os.path.exists(early_path):
            os.mkdir(early_path)

        if not os.path.exists(early_path+"/debate_1"):
            os.mkdir(early_path+"/debate_1")
            folder_name = "debate_1"
        else :
            last_subfolder = 1
            for sub_folder in (glob.glob('replays\*')) :
                if(last_subfolder < int((sub_folder.split("\\"))[1].split("_")[1])):
                    last_subfolder = int((sub_folder.split("\\"))[1].split("_")[1])
            new_val = last_subfolder + 1
            os.mkdir(early_path+f"/debate_{new_val}")
            folder_name = f"debate_{new_val}"
            
        # Create the right subfolder where to put results    
        
        UG=read_UG_from_apx("results/debate_"+numberDebate+"/universe_graph.apx")
        export_apx_OG(folder_name, f"univers_graph", UG,early_path="replays/")
        agents=[]
        
        for i in range(int(numberOfagent)) :
            new=f"results/debate_{numberDebate}/opinion_graph {i}.apx"
            agents.append(agent(i,read_UG_from_apx(new),UG))
            export_apx_OG(folder_name, f"opinion_graph {i}", agents[i].OG,early_path="replays/")
    
        j = 0
        data={"order":[], "Vp":[], "numberOfTurn":[]}
        for a in agents:
                data[a.get_number()]=[]
                j+=1
        
        agentry=find_all_combinations(agents)
        agent_order=""
        for i in agentry:
            word=""
            for j in i :
                print(j.get_number())
                number=f"{j.get_number()}"
                word=word+","+number
            print(word)
            if(word[1:len(word)]==combinaison):
                print(word[1:len(word)])
                agent_order=i
        # Run the protocol for each agent order combination
        
            
        vp, public_graph, order, agents, nb_turn = run_protocol(UG, agent_order)

        # Export results in apx and csv
        export_apx_OG(folder_name, order, public_graph, early_path="replays/")
        data["order"].append(order)
        data["Vp"].append(vp)
        data["numberOfTurn"].append(nb_turn)
        for a in agents:
                data[a.get_number()].append(a.in_comfort_zone(public_graph))
        
        data["debateReplay"]=numberDebate
        df = pd.DataFrame(data)
        df.to_csv("replays/"+ folder_name +"/data.csv", index=False)
    
if __name__ == "__main__":
    main(3)

