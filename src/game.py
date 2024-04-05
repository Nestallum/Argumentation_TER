# game.py

"""
This Python script simulates a debate game.

Authors: Mohamed AZZAOUI, Nassim LATTAB
Creation Date: 21/03/2024
"""

from src.agent import *
from src.util import *
import csv
from src.IO_graph_apx import *
from src.agent import *
from src.game import *
from src.util import *
import pandas as pd

def initialize_agents(UG, number_of_agents) -> list:
    """
    Initializes a list of agents to participate in the debate.

    Args:
    - UG (dict): The universe graph representing the entire argumentation framework.
    - number_of_agents (int): The number of agents participating in the debate.

    Returns:
    - list: A list of initialized agents with automatically generated argument graphs (AGs).
    """
    
    # Initialize agents.
    agents = []
    
    # Create agents with automatically generated OG.
    for k in range(number_of_agents):
        OG = auto_generate_OG(UG)
        agents.append(agent(k, OG, UG))

    return agents

def run_protocol(UG, agents) -> float | dict:
    """
    Simulates a debate game with automatically generated agents and argumentation frameworks.
    
    Args:
    - UG (dict) : The universe graph representing the entire argumentation framework.
    - agents (list) : The list of the agents participating in the debate.

    Returns:
    - float: The final value of the issue of the debate.
    - dict : The final PG.
    - str : The names of the agents
    - list : The list of agents
    - int : number of turn needed to end the debate.
    """

    nb_turn = 0 
    PG = {"0":[]} # Initialize public graph.
    previous_PG = {}
    number_of_agents = len(agents)
    historic = []

    # Run the debate until no arguments are presented in a turn.
    while(PG != previous_PG):
        print("\n" + "-"*60)
        nb_turn += 1
        previous_PG = PG

        print(f"\n* TURN NUMBER {nb_turn}:")

        # Iterate through each agent to make their move.
        for k in range(number_of_agents):
            print(f"\n{'- Turn of ' + agents[k].name + ' :':^40}")
            PG = agents[k].best_next_move(PG, UG, nb_turn)

    for k in range(number_of_agents):
        historic.append(agents[k].historic)
    print(historic)

    # Debate conclusion.
    print("\nSince none of the agents presented any arguments throughout an entire turn, the debate concludes.")
    final_Vp = Hbs(PG, "0")
    print(f"final value of the issue Vp : {final_Vp}\n")
    
    agent_names = []
    for a in agents:     
        agent_names.append(f"A{a.get_number()}")
            
    agent_names = ",".join(agent_names)   
    return final_Vp, PG, agent_names, agents, nb_turn

def find_all_combinations(agents) -> list:
    """
    Generates all possible combinations of agent orderings from the given list.

    Args:
    - agents (list): A list of agents.

    Returns:
    - list: A list containing all possible combinations of agent orderings.
    """
     # Generate all possible permutations of agent indices.
    agent_indices = range(len(agents))
    permutations_indices = permutations(agent_indices)

    # For each permutation of indices, create a corresponding list of agents.
    agent_combinations = []
    for perm_indices in permutations_indices:
        agent_order = [agents[i] for i in perm_indices]
        agent_combinations.append(agent_order)

    return agent_combinations

def generate_debate(numberOfAgents: int) -> None:
    """
    Generate a debate based on the given number of agents.

    Args:
        numberOfAgents (int): The number of agents participating in the debate.

    Returns:
        None
    """

    # Generate the debate graph as a networkx.classes.digraph.DiGraph
    generated_graph = debate_graph_generation()
    
    # Export the networkx.classes.digraph.DiGraph to an APX file into a subfolder of the results folder and returns it
    debate_results = export_apx_UG("universe_graph", generated_graph)

    # Read the universe graph from the APX file
    universe_graph = read_UG_from_apx("results/"+ debate_results +"/universe_graph.apx")
    
    # Initialize agents with the universe graph
    number_of_agents = numberOfAgents
    agents = initialize_agents(universe_graph, number_of_agents)
    
    # Generate all agent order combinations
    agent_combinations = agent_order_combinations(agents)

    j = 0
    data={"order":[], "Vp":[], "numberOfTurn":[]}
    for a in agents:
        export_apx(debate_results, f"opinion_graph_{j}", a.OG)
        data[a.get_number()]=[]
        j+=1

    # Run the protocol for each agent order combination
    for agent_order in agent_combinations:
        
        vp, public_graph, order, agents, nb_turn = run_protocol(universe_graph, agent_order)

        # Export results in apx and csv
        export_apx(debate_results, order, public_graph)
        data["order"].append(order)
        data["Vp"].append(vp)
        data["numberOfTurn"].append(nb_turn)
        for a in agents:
            historic_data = []
            historic_data.append(a.name)
            historic_data.append(a.in_comfort_zone(public_graph))
            historic_data.append(a.historic)
            data[a.get_number()].append(historic_data)
            a.historic = dict()
    
    df = pd.DataFrame(data)
    df.to_csv("results/"+ debate_results +"/data.csv", index=False)


def replay_debate(debate_path: str) -> None:
    """
    Replays the debate with the given debate number.

    Args:
        debate_number (int): The number of the debate to replay.

    Returns:
        None
    """
    if not os.path.exists(debate_path):
        print(f"The file {debate_path} does not exist.")
        return None
    
    early_path="replays/"
    print(debate_path.split("/"))
    debate_path_last=debate_path.split("/")[len(debate_path.split("/"))-1]
    if not os.path.exists(early_path):
        os.mkdir(early_path)

    if not os.path.exists(early_path+debate_path_last+".1"):
        os.mkdir(early_path+debate_path_last+".1")
        folder_name = debate_path_last+".1"
    else :
        last_subfolder = 1
        for sub_folder in (glob.glob(r'replays\*')) :
            if(last_subfolder < int((sub_folder.split("\\"))[1].split(".")[1])):
                last_subfolder = int((sub_folder.split("\\"))[1].split(".")[1])
        new_val = last_subfolder + 1
        os.mkdir(early_path+f"/{debate_path_last}.{new_val}")
        folder_name = f"/{debate_path_last}.{new_val}"
        
    # Create the right subfolder where to put results    
    UG = read_UG_from_apx(debate_path+"/universe_graph.apx")
    csv_path = (debate_path+"/data.csv")

    # Open CSV file to get the right number of agents to replay the debate.
    with open(csv_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        second_row = next(reader)
        first_column_value = second_row[0]
        numberOfAgents = len(first_column_value.split(","))

    export_apx(folder_name, f"univers_graph", UG, early_path)
    agents=[]
    
    for i in range(int(numberOfAgents)):
        new = f"{debate_path}/opinion_graph_{i}.apx"
        agents.append(agent(i,read_UG_from_apx(new),UG))
        export_apx(folder_name, f"opinion_graph_{i}", agents[i].OG, early_path="replays/")

    j = 0
    data={"order":[], "Vp":[], "numberOfTurn":[]}
    for a in agents:
            data[a.get_number()]=[]
            j+=1
    
    combinations = find_all_combinations(agents)

    # Run the protocol for each agent order combination
    for agent_order in combinations:
        
        vp, public_graph, order, agents, nb_turn = run_protocol(UG, agent_order)

        # Export results in apx and csv
        export_apx(folder_name, order, public_graph,early_path="replays/")
        data["order"].append(order)
        data["Vp"].append(vp)
        data["numberOfTurn"].append(nb_turn)
        for a in agents:
            historic_data = []
            historic_data.append(a.name)
            historic_data.append(a.in_comfort_zone(public_graph))
            historic_data.append(a.historic)
            data[a.get_number()].append(historic_data)
            a.historic = dict()
    
    df = pd.DataFrame(data)
    df.to_csv("replays/"+ folder_name +"/data.csv", index=False)

def replay_combination(debate_path: str, combination: str) -> None:
    early_path = "replays/"

    if not os.path.exists(debate_path):
        print(f"The file {debate_path} does not exist.")
        return None
    
    early_path="replays/"
    print(debate_path.split("/"))
    debate_path_last=debate_path.split("/")[len(debate_path.split("/"))-1]
    if not os.path.exists(early_path):
        os.mkdir(early_path)

    if not os.path.exists(early_path+debate_path_last+".1"):
        os.mkdir(early_path+debate_path_last+".1")
        folder_name = debate_path_last+".1"
    else :
        last_subfolder = 1
        for sub_folder in (glob.glob(r'replays\*')) :
            if(last_subfolder < int((sub_folder.split("\\"))[1].split(".")[1])):
                last_subfolder = int((sub_folder.split("\\"))[1].split(".")[1])
        new_val = last_subfolder + 1
        os.mkdir(early_path+f"/{debate_path_last}.{new_val}")
        folder_name = f"/{debate_path_last}.{new_val}"
    # Create the right subfolder where to put results    
    UG = read_UG_from_apx(debate_path+"/universe_graph.apx")
    csv_path = (debate_path+"/data.csv")

    # Open CSV file to get the right number of agents to replay the debate.
    with open(csv_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        second_row = next(reader)
        first_column_value = second_row[0]
        numberOfAgents = len(first_column_value.split(","))

    export_apx(folder_name, f"univers_graph", UG, early_path="replays/")
    agents=[]
    
    for i in range(int(numberOfAgents)) :
        new = f"{debate_path}/opinion_graph_{i}.apx"
        agents.append(agent(i,read_UG_from_apx(new),UG))
        export_apx(folder_name, f"opinion_graph_{i}", agents[i].OG, early_path="replays/")

    j = 0
    data={"order":[], "Vp":[], "numberOfTurn":[]}
    for a in agents:
            data[a.get_number()]=[]
            j+=1
    
    combinations = find_all_combinations(agents)
    agent_order=""
    for i in combinations:
        word=""
        for j in i :
            print(j.get_number())
            number=f"{j.get_number()}"
            word=word+","+number
        print(word)
        if(word[1:len(word)]==combination):
            print(word[1:len(word)])
            agent_order=i
    # Run the protocol for each agent order combination
    
        
    vp, public_graph, order, agents, nb_turn = run_protocol(UG, agent_order)

    # Export results in apx and csv
    export_apx(folder_name, order, public_graph, early_path="replays/")
    data["order"].append(order)
    data["Vp"].append(vp)
    data["numberOfTurn"].append(nb_turn)
    for a in agents:
        historic_data = []
        historic_data.append(a.name)
        historic_data.append(a.in_comfort_zone(public_graph))
        historic_data.append(a.historic)
        data[a.get_number()].append(historic_data)
        a.historic = dict()
    
    
    df = pd.DataFrame(data)
    df.to_csv("replays/"+ folder_name +"/data.csv", index=False)