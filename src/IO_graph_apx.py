# src/graph_from_apx.py

"""
This Python script reads a .apx file and creates the associated graph.

Authors: Nassim LATTAB
Creation Date: 19/03/2024
"""

import os, sys, argparse, re
import glob
import networkx

def get_command_args() -> str:
    """ 
    Returns the .apx file provided in the command line.
    """
    
    # Add a description to our script.
    parser = argparse.ArgumentParser(description="Study the impact of agent order in argumentation protocols.")
    
    # Arguments for the command.
    parser.add_argument('-f', '--file', type=str, help='The .apx file to read, which contains the Universe Graph information.')
    
    # Read args in the command.
    command_args = parser.parse_args()

    # Get file arg.
    file_name = command_args.file # Recover the file containing the Universe Graph information to read (.apx).

    # Check if the file has the .apx extension using regex.
    if not re.match(r'.*\.apx$', file_name):
        print("Error: The provided file must have a .apx extension.")
        sys.exit(1)

    return file_name

def read_graph_from_apx(file_path: str) -> dict:
    """
    Returns the Graph read from the specified file as a dictionary.

    Args:
        file_name (str): The name of the file containing the Universe Graph.

    Returns:
        dict: The Graph represented as a dictionary.
        Key : attacked argument, Value : list of attacking arguments (may be empty).
    """

    if not os.path.exists(file_path):
        print(f"The file {file_path} does not exist.")
        sys.exit(1)

    graph = {}

    with open(file_path, 'r') as file:
        for line in file:

            # Get the line content
            content = line[line.find("(")+1 : line.find(")")]

            # Add arguments to the dict as attacked args.
            if line.startswith("arg"):
                argument = content
                graph[argument] = list()

            # For each attacker, add it to the list of attacking args.
            elif line.startswith("att"):
                attacker, attacked = content.split(',')[0], content.split(',')[1]                
                graph[attacked].append(attacker)
                
    return graph

def export_DiGraph_as_apx(file_name: str, graph: 'networkx.classes.digraph.DiGraph') -> None:
    """
    Writes the graph represented as a directed graph (DiGraph) to a file in the specified folder with the given file name.

    Args:
        folder_name (str): The name of the folder where the file will be saved.
        file_name (str): The name of the file to write the graph to.
        graph (networkx.classes.digraph.DiGraph): The graph represented as a directed graph (DiGraph).

    Returns:
        None.
    """

    extension = ".apx"
    folder = "results/"
    if not os.path.exists(folder):
        os.mkdir(folder)

    if not os.path.exists(folder+"/debate_1"):
        os.mkdir(folder+"/debate_1")
        debate_name = "debate_1"

    # Create the right subfolder where to put results    
    else :
        last_subfolder = 1
        for sub_folder in (glob.glob(r'results\*')) :
            if(last_subfolder < int((sub_folder.split("\\"))[1].split("_")[1])):
                last_subfolder = int((sub_folder.split("\\"))[1].split("_")[1])
        new_val = last_subfolder + 1
        os.mkdir(folder+f"/debate_{new_val}")
        debate_name = f"debate_{new_val}"
    
    debate_path = folder + debate_name + "/" + file_name + extension
    
    if os.path.exists(debate_path):
        print(f"You cannot write (export) into the file {file_name}{extension} because it already exists and contains a graph.")
        sys.exit(1)
        
    # Create and fill the file
    with open(debate_path, 'w') as file:
        for arg in graph:
            # Write arguments.
            file.write("arg(" + str(arg) + ").\n")
            
        for arg1, dicoAtt in graph.adjacency():
            if dicoAtt:
                for arg2, _ in dicoAtt.items():
                    # Fill with attack relations.
                    file.write("att(" + str(arg1) + "," + str(arg2) + ").\n")
                    
    return debate_name

def export_apx(folder_path_name: str, file_name: str, graph: dict) -> None:
    """
    Writes the graph represented as a dictionary to a file in the specified folder with the given file name.

    Args:
        path_name (str): The name of the path where the file will be saved.
        file_name (str): The name of the file to write the graph to.
        graph (dict): The graph represented as a directed graph (DiGraph).

    Returns:
        None.
    """

    extension = ".apx"
    path = folder_path_name + "/" + file_name + extension
    
    if os.path.exists(path):
        print(f"You cannot write (export) into the file {file_name}{extension} because it already exists and contains a graph.")
        sys.exit(1)
        
    with open(path, 'w') as file:
        for arg in graph:
            # Write arguments.
            file.write("arg(" + str(arg) + ").\n")
            
        for key,value  in graph.items():
            if len(value)!=0 :
                for argAtt in value:
                    # Fill with attack relations.
                    file.write("att(" + str(argAtt) + "," + str(key) + ").\n")
                    
    