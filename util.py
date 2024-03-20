# util.py

"""
This Python script contains utility methods for processing and analyzing debate data.

Authors: Mohamed AZZAOUI, Nassim LATTAB
Creation Date: 19/03/2024
"""

universe_graph={"i":["a","b","c"],"b":["e"],"a":["d"],"c":[],"e":[],"d":[]}
    
def Hbs(graph: dict, argument: str) -> float:
    """ 
    Calculates and returns the Belief Strength (Hbs) of an argument.

    The Belief Strength (Hbs) of an argument is calculated as follows:
    - If no other arguments attack the given argument, its Belief Strength (Hbs) is 1.
    - Otherwise, the Belief Strength (Hbs) is calculated as 1 divided by the sum of the Belief Strengths (Hbs)
      of all attacking arguments, plus 1.
    """
    
    # If nobody attacks the argument, the value is of his Hbs 1.
    if len(graph[argument]) == 0: 
        return 1
    
    else:
        # Sum the Belief Strengths (Hbs) of all attacking arguments.
        total_hbs = 0                  
        for i in range(len(graph[argument])):
            total_hbs += Hbs(graph, graph[argument][i])
            
        # Calculate and return the Belief Strength (Hbs) of the argument.
        return 1 / (1 + total_hbs)
    
# print(Hbs(universe_graph,"i"))