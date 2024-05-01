# src/game.py

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

def run_protocol(UG: dict, agents: list) -> float | dict:
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
    historical = []

    # Run the debate until no arguments are presented in a turn.
    while(PG != previous_PG):
        
        nb_turn += 1
        previous_PG = PG

        # Iterate through each agent to make their move.
        for k in range(number_of_agents):
            
            PG = agents[k].best_next_move(PG, UG, nb_turn)

    for k in range(number_of_agents):
        historical.append(agents[k].historical)

    # Debate conclusion.
    final_Vp = Hbs(PG, "0")
    
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
    debate_results_folder_name = export_DiGraph_as_apx("universe_graph", generated_graph)

    # Read the universe graph from the APX file
    universe_graph = read_graph_from_apx("results/"+ debate_results_folder_name +"/universe_graph.apx")
    
    # Initialize agents with the universe graph
    number_of_agents = numberOfAgents
    agents = initialize_agents(universe_graph, number_of_agents)
    
    # Generate all agent order combinations
    agent_combinations = agent_order_combinations(agents)

    # Initialize csv columns
    data = {"order":[], "Vp":[], "numberOfTurn":[]}

    j = 0
    results_folder = "results/"
    for a in agents:
        export_apx(results_folder+debate_results_folder_name, f"opinion_graph_{j}", a.OG)
        data[a.get_number()] = []
        j += 1

    # Data for csv2
    data_2 = {"order":[], "Vp":[], "numberOfTurn":[], "turnHistory":[]}

    # Run the protocol for each agent order combination
    for agent_order in agent_combinations:
        
        vp, public_graph, order, agents, nb_turn = run_protocol(universe_graph, agent_order)

        # Export results in apx and csv
        export_apx(results_folder+debate_results_folder_name, order, public_graph)
        exported_data = export_results(data, public_graph, order, vp, nb_turn, agents)
        exported_data_2 = export_results_2(data_2, order, vp, nb_turn, agents)

        # Reset agent historical for next debate orders
        for a in agent_order:
            a.historical = dict()
    
    # Create csv files
    df = pd.DataFrame(exported_data)
    df2 = pd.DataFrame(exported_data_2)

    # Main csv folder which will contain every other csv folders
    csv_folder = "csv"
    if not os.path.exists(csv_folder):
        os.mkdir("csv")

    # Subfolder for csv_1 and csv_2
    csv_1_pathname = csv_folder + "/csv_1"
    csv_2_pathname = csv_folder + "/csv_2"
    if not os.path.exists(csv_1_pathname):
        os.mkdir(csv_1_pathname)
    if not os.path.exists(csv_2_pathname):
        os.mkdir(csv_2_pathname)

    debate_number = debate_results_folder_name.split("_")[1]
    df.to_csv(f"{csv_1_pathname}/debate_{debate_number}_data.csv", index=False)
    df2.to_csv(f"{csv_2_pathname}/debate_{debate_number}_data_2.csv", index=False)

def replay_debate(debate_path: str, numberOfAgents: int) -> None:
    """
    Replays the debate with the given debate number.

    Args:
        debate_path (str): The path of the debate to replay.
        numberOfAgents (int): The number of agents participating in the debate.

    Returns:
        None
    """
    new_val = 1
    if not os.path.exists(debate_path):
        print(f"The file {debate_path} does not exist.")
        sys.exit(1)
    
    # Create replays folder if it does not already exist.
    replays_folder = "replays/"
    if not os.path.exists(replays_folder):
        os.mkdir(replays_folder)

    # Create new sub folder
    last_debate_name = debate_path.split("/")[len(debate_path.split("/"))-1]
    if not os.path.exists(replays_folder+last_debate_name+"-1"):
        os.mkdir(replays_folder+last_debate_name+"-1")
        new_sub_folder = last_debate_name+"-1"
    else :
        last_subfolder = 1
        for sub_folder in (glob.glob(r'replays\*')) :
            if(last_subfolder < int((sub_folder.split("\\"))[1].split("-")[1]) and (last_debate_name in sub_folder)):
                last_subfolder = int((sub_folder.split("\\"))[1].split("-")[1])
        new_val = last_subfolder + 1
        os.mkdir(replays_folder+f"/{last_debate_name}-{new_val}")
        new_sub_folder = f"/{last_debate_name}-{new_val}"
        
    # Get UG from the debate to replay.
    universe_graph_name = "universe_graph"
    UG = read_graph_from_apx(debate_path+"/"+universe_graph_name+".apx")

    # export UG as apx file in the replay path.
    export_apx(replays_folder+new_sub_folder, universe_graph_name, UG)

    # Initialize agent list and their opinion graph
    agents = []
    for i in range(int(numberOfAgents)):
        opinion_graph_file = f"{debate_path}/opinion_graph_{i}.apx"
        agents.append(agent(i, read_graph_from_apx(opinion_graph_file), UG))
        export_apx(replays_folder+new_sub_folder, f"opinion_graph_{i}", agents[i].OG)

    # Initialize csv columns
    data = {"order":[], "Vp":[], "numberOfTurn":[]}

    j = 0
    for a in agents:
        data[a.get_number()] = []
        j += 1
    
    combinations = find_all_combinations(agents)
    data_2 = {"order":[], "Vp":[], "numberOfTurn":[], "turnHistory":[]}

    # Run the protocol for each agent order combination
    for agent_order in combinations:
        
        vp, public_graph, order, agents, nb_turn = run_protocol(UG, agent_order)

        # Export results in apx and csv
        export_apx(replays_folder+new_sub_folder, order, public_graph)
        data = export_results(data, public_graph, order, vp, nb_turn, agents)
        exported_data_2 = export_results_2(data_2, order, vp, nb_turn, agents)
        for a in agent_order:
            a.historical = dict()
    
    df = pd.DataFrame(data)
    df2 = pd.DataFrame(exported_data_2)

    # Main csv folder which will contain every other csv folders
    csv_folder = "csv"
    if not os.path.exists(csv_folder):
        os.mkdir("csv")

    # Subfolder for csv_1 and csv_2
    csv_1_pathname = csv_folder + "/csv_1"
    csv_2_pathname = csv_folder + "/csv_2"
    if not os.path.exists(csv_1_pathname):
        os.mkdir(csv_1_pathname)
    if not os.path.exists(csv_2_pathname):
        os.mkdir(csv_2_pathname)

    df.to_csv(f"{csv_1_pathname}/{new_sub_folder}_data.csv", index=False)
    df2.to_csv(f"{csv_2_pathname}/{new_sub_folder}_data_2.csv", index=False)
    
def replay_debate_with_new_agents(debate_path: str, number_agents: int, csv_folder="csv") -> None:
    """
    Replays the debate with the given debate number.

    Args:
        debate_path (str): The path of the debate to replay.
        number_agents (int): The number of agents.

    Returns:
        None
    """
    new_val = 1
    if not os.path.exists(debate_path):
        print(f"The file {debate_path} does not exist.")
        sys.exit(1)
    
    # Create replays folder
    replays_folder = "replays/"
    if not os.path.exists(replays_folder):
        os.mkdir(replays_folder)

    # Create new sub folder
    last_debate_name = debate_path.split("/")[len(debate_path.split("/"))-1]
    if not os.path.exists(replays_folder+last_debate_name+"-1"):
        os.mkdir(replays_folder+last_debate_name+"-1")
        new_sub_folder = last_debate_name+"-1"
    else :
        last_subfolder = 1
        for sub_folder in (glob.glob(r'replays\*')) :
            if(last_subfolder < int((sub_folder.split("\\"))[1].split("-")[1]) and (last_debate_name in sub_folder)):
                last_subfolder = int((sub_folder.split("\\"))[1].split("-")[1])
        new_val = last_subfolder + 1
        os.mkdir(replays_folder+f"/{last_debate_name}-{new_val}")
        new_sub_folder = f"/{last_debate_name}-{new_val}"
        
    # Get UG from the debate to replay.   
    UG = read_graph_from_apx(debate_path+"/universe_graph.apx")

    # export UG as apx file in the replay path.
    export_apx(replays_folder+new_sub_folder, "universe_graph", UG)

    # Create a new agent list from the given UG.
    agents = initialize_agents(UG, number_agents)
    
    for i in range(len(agents)) :
        export_apx(replays_folder+new_sub_folder, f"opinion_graph_{i}", agents[i].OG)
    
    data = {"order":[], "Vp":[], "numberOfTurn":[]}

    j = 0
    for a in agents:
        data[a.get_number()] = []
        j += 1
    
    combinations = find_all_combinations(agents)
    data_2 = {"order":[], "Vp":[], "numberOfTurn":[], "turnHistory":[]}

    # Run the protocol for each agent order combination
    for agent_order in combinations:
        
        vp, public_graph, order, agents, nb_turn = run_protocol(UG, agent_order)
        
        # Export results in apx and csv
        export_apx(replays_folder+new_sub_folder, order, public_graph)
        data = export_results(data, public_graph, order, vp, nb_turn, agents)
        exported_data_2 = export_results_2(data_2, order, vp, nb_turn, agents)
        for a in agent_order:
            a.historical = dict()
    
    df = pd.DataFrame(data)
    df2 = pd.DataFrame(exported_data_2)

    # Main csv folder which will contain every other csv folders
    if not os.path.exists(csv_folder):
        os.mkdir(csv_folder)

    # Subfolder for csv_1 and csv_2
    csv_1_pathname = csv_folder + "/same_ug_new_agents_csv_1"
    csv_2_pathname = csv_folder + "/same_ug_new_agents_csv_2"
    if not os.path.exists(csv_1_pathname):
        os.mkdir(csv_1_pathname)
    if not os.path.exists(csv_2_pathname):
        os.mkdir(csv_2_pathname)

    df.to_csv(f"{csv_1_pathname}/{new_sub_folder}_data.csv", index=False)
    df2.to_csv(f"{csv_2_pathname}/{new_sub_folder}_data_2.csv", index=False)
    
def replay_combination(debate_path: str, combination: str) -> None:
    """
    Replay a debate based on a specific combination of agents.

    Parameters:
        debate_path (str): The path to the debate folder containing necessary files.
        combination (str): The combination of agent numbers separated by commas.

    Returns:
        None: This function doesn't return anything but replays the debate and saves results.
    """

    if not os.path.exists(debate_path):
        print(f"The file {debate_path} does not exist.")
        sys.exit(1)
    
    # Create replays folder
    replays_folder="replays/"
    if not os.path.exists(replays_folder):
        os.mkdir(replays_folder)

    # Create new sub folder
    last_debate_name=debate_path.split("/")[len(debate_path.split("/"))-1]
    if not os.path.exists(replays_folder+last_debate_name+"-1"):
        os.mkdir(replays_folder+last_debate_name+"-1")
        new_sub_folder = last_debate_name+"-1"
    else :
        last_subfolder = 1
        for sub_folder in (glob.glob(r'replays\*')) :
            if(last_subfolder < int((sub_folder.split("\\"))[1].split("-")[1]) and (last_debate_name in sub_folder)):
                last_subfolder = int((sub_folder.split("\\"))[1].split("-")[1])
        new_val = last_subfolder + 1
        os.mkdir(replays_folder+f"/{last_debate_name}.{new_val}")
        new_sub_folder = f"/{last_debate_name}.{new_val}"

    # Create the right subfolder where to put results    
    UG = read_graph_from_apx(debate_path+"/universe_graph.apx")
    csv_path = (debate_path+"/data.csv")

    # Open CSV file to get the right number of agents to replay the debate.
    with open(csv_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        second_row = next(reader)
        first_column_value = second_row[0]
        numberOfAgents = len(first_column_value.split(","))

    export_apx(new_sub_folder, f"univers_graph", UG, replays_folder="replays/")

    # Initialize agent list
    agents = []
    for i in range(int(numberOfAgents)) :
        new = f"{debate_path}/opinion_graph_{i}.apx"
        agents.append(agent(i,read_graph_from_apx(new), UG))
        export_apx(new_sub_folder, f"opinion_graph_{i}", agents[i].OG, replays_folder="replays/")

    # Initialize csv file
    j = 0
    data = {"order":[], "Vp":[], "numberOfTurn":[]}
    for a in agents:
        data[a.get_number()] = []
        j += 1
    
    combinations = find_all_combinations(agents)

    # Find the right combination to replay
    agent_order = ""
    for comb in combinations:
        word = ""
        for j in comb :
            number=f"{j.get_number()}"
            word += ","+number
        if(word[1:len(word)]==combination):
            agent_order = comb
    
    vp, public_graph, order, agents, nb_turn = run_protocol(UG, agent_order)
    data_2 = {"order":[], "Vp":[], "numberOfTurn":[], "turnHistory":[]}
    # Export results in apx and csv
    export_apx(new_sub_folder, order, public_graph, replays_folder="replays/")
    exported_data = export_results(data, public_graph, order, vp, nb_turn, agents)
    exported_data_2 = export_results_2(data_2, order, vp, nb_turn, agents)
    
    # Create csv file
    df = pd.DataFrame(exported_data)
    df.to_csv("replays/"+ new_sub_folder +"/data.csv", index=False)

    df2 = pd.DataFrame(exported_data_2)
    df2.to_csv("replays/"+ new_sub_folder +"/data_2.csv", index=False)

def export_results(data, public_graph, order, vp, nb_turn, agents) -> dict:
    """
    Export the results of the debate including order, Vp, number of turns, and agent historical data into a dictionary for dataframe.

    Parameters:
        data (dict): The dictionary containing the results data.
        public_graph (dict): The public opinion graph after the debate.
        order (str): The order in which the agents participated in the debate.
        vp (str): The winner of the debate.
        nb_turn (int): The total number of turns in the debate.
        agents (List[Agent]): A list of Agent objects representing participants in the debate.

    Returns:
        dict: A dictionary containing the updated results data.

    Notes:
        - The historical data of each agent is appended to the results data.
        - The historical data includes the agent's name, comfort zone status, and historical actions.
    """

    data["order"].append(order)
    data["Vp"].append(vp)
    data["numberOfTurn"].append(nb_turn)

    # Append historical data of each agent to data dictionary
    for a in agents:
        historical_data = []
        historical_data.append(a.name)
        historical_data.append(a.in_comfort_zone(public_graph))
        historical_data.append(a.historical)
        j=0
        for i in a.historical.values() :
            if i!=None :
                j=j+1
        
        historical_data.append(j)
        historical_data.append(a.nbArg)
        historical_data.append(a.nbAtt)
        data[a.get_number()].append(historical_data)

    return data

def export_results_2(data, order, vp, nb_turn, agents) -> dict:
    """
    Export the detailed results of the debate including order, Vp, number of turns, and agent historical data for each turn.

    Parameters:
        data (dict): The dictionary containing the results data.
        order (str): The order in which the agents participated in the debate.
        vp (str): The winner of the debate.
        nb_turn (int): The total number of turns in the debate.
        agents (List[Agent]): A list of Agent objects representing participants in the debate.

    Returns:
        dict: A dictionary containing the updated results data.

    Notes:
        - Each turn's historical data for all agents is appended to the results data.
        - The historical data includes the agent's name and actions for each turn.
        - The turns are indexed starting from 0.
    """

    data["order"].append(order)
    data["Vp"].append(vp)
    data["numberOfTurn"].append(nb_turn)

    # Create a dictionary to store historical data for all turns
    all_turn = dict()

    for i in range(nb_turn):
        turn = []
        dic = dict()

        # Gather historical data for each agent for the current turn
        for a in agents:
            dic[a.name] = a.historical[i+1]

        turn.append(dic)
        all_turn[f"turn {i}"] = turn

    # Append turn history to data dictionary
    data["turnHistory"].append(all_turn)

    return data