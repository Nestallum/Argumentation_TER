# graph_from_apx.py

"""
This Python script reads a .apx file and creates the associated graph.

Authors: Nassim LATTAB
Creation Date: 19/03/2024
"""

import os, sys, argparse, re

def get_command_args() -> str:
    """ 
    Returns the .apx file provided.
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

def read_UG_from_file(file_name: str) -> dict:
    """
    Returns the Universe Graph (UG) read from the specified file as a dictionary.
    Key : attacked argument, Value : list of attacking arguments (may be empty).
    """
    if not os.path.exists(file_name):
        print(f"The file {file_name} does not exist.")
        sys.exit(1)

    graph = {}

    with open(file_name, 'r') as file:
        for line in file:

            # Get the line content
            content = line[line.find("(")+1 : line.find(")")]

            # Add arguments to the dict as attacked args
            if line.startswith("arg"):
                argument = content
                graph[argument] = list()

            # For each attacker, add it to the list of attacking args
            elif line.startswith("att"):
                attacker, attacked = content.split(',')[0], content.split(',')[1]                
                graph[attacked].append(attacker)
                
    return graph