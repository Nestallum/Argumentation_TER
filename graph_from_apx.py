# graph_from_apx.py

"""
This Python script reads a .apx file and creates the associated graph.

Authors: Nassim LATTAB
Creation Date: 19/03/2024
"""

import os, sys, argparse, re

def get_command_args() -> tuple:
    """ 
    Returns the .apx file provided.
    """
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
    Key : attacked argument, Value : list of attacking arguments.
    """
    if not os.path.exists(file_name):
        print(f"The file {file_name} does not exist.")
        sys.exit(1)

    graph = {}
    # Regular expression for arguments. 
    # Each argument is defined in a line of the form "arg(name_argument)." 
    # Each attack is defined in a line of the form "att(attacking_arg,attacked_arg)."
    regex_pattern = re.compile(r'^(arg\(\w+\)|att\(\w+,\w+\))\.$')

    with open(file_name, 'r') as file:
        for line in file:
            # Checks for valid syntax for the representation of the UG in the apx file. Raise a ValueError if at least one of them is not valid.
            if not regex_pattern.match(line):
                raise ValueError("Unaccepted argument or attack for the representation of the UG in the text file.\n"+ 
                                "Each argument must be defined in a line of the form 'arg(name_argument).'\n"+
                                "Each attack must be defined in a line of the form 'att(attacking_arg,attacked_arg).'.")
            content = line[line.find("(")+1 : line.find(")")]

            if line.startswith("arg"):
                argument = content
                graph[argument] = list()

            elif line.startswith("att"):
                attacker, attacked = content.split(',')[0], content.split(',')[1]
                if not attacked in graph.keys():
                    raise ValueError("One of the attacker is not part of the arguments. All arguments must be defined before attacks.")
                
                graph[attacked].add(attacker)
                
    return graph