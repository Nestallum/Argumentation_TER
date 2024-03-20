# util.py
"""
This Python script contains utility methods for processing and analyzing debate data.

Authors: Mohamed AZZAOUI, Nassim LATTAB
Creation Date: 19/03/2024
"""


univers_graph={"i":["a","b","c"],"b":["e"],"a":["d"],"c":[],"e":[],"d":[]}

opinion_graph={"i":[],"d":[]}

arguments=["a","i","b","d"]

def Att_Arg(OG,UG):
    
    liste_adjacence_att={}
    for key in OG.keys():
        liste_adjacence_att[key]=[]
        for key2,value2 in UG.items() :
            if(key in value2):
                liste_adjacence_att[key].append(key2)
                
    return liste_adjacence_att

def Create_OG(arguments,UG):
    
    OG = {}
    
    for i in arguments :
        arg = []
        for l in UG[i]:
            if(l in arguments):
                arg.append(l)
        OG[i] = arg
        
    return OG

def Hbs(graph : dict ,root:str ,dict={})-> float:


    """ 
    Calculates and returns the Belief Strength (Hbs) of an argument.

    The Belief Strength (Hbs) of an argument is calculated as follows:
    - If no other arguments attack the given argument, its Belief Strength (Hbs) is 1.
    - Otherwise, the Belief Strength (Hbs) is calculated as 1 divided by the total_Hbs of the Belief Strengths (Hbs)
      of all attacking arguments, plus 1.
    """
     
    if(root in dict.keys()):
        return dict[root]
    
    # If nobody attacks the argument, the value is of his Hbs 1.
    if((len(graph[root])) == 0): 
        return 1
    
    else :
        # Sums the Belief Strengths (Hbs) of all attacking arguments.
        total_Hbs = 0                 
        for i in range(len(graph[root])):
            total_Hbs += Hbs(graph,(graph[root])[i],dict)
            
        dict[root] = 1/(1+total_Hbs)
        # Calculate and return the Belief Strength (Hbs) of the argument.
        return 1/(1+total_Hbs)
    



    
# print(Hbs(universe_graph,"i"))

