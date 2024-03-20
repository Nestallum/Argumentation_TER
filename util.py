univers_graph={"i":["a","b","c"],"b":["e"],"a":["d"],"c":[],"e":[],"d":[]}
opinion_graph={"i":[],"d":[]}

def Att_Arg(OG,UG):
    
    liste_adjacence_att={}
    print(UG)
    for key in OG.keys():
        liste_adjacence_att[key]=[]
        for key2,value2 in UG.items() :
            if(key in value2):
                liste_adjacence_att[key].append(key2)
                
    return liste_adjacence_att

def Hbs(graph,root,dict={}):
    
    if(root in dict.keys()): #dictionary who permit to not calculate again the same Hbs
        return dict[root]
    
    if((len(graph[root])) == 0): #if anybody attack the arguments the value is 1
        dict[root] = 1
        return 1
    
    else :
        sum = 0                  #take all the arguments who attack root and do the sum of their hbs for calculate the hbs of root
        for i in range(len(graph[root])):
            sum += Hbs(graph,(graph[root])[i],dict)
            
        dict[root] = 1/(1+sum)
        return 1/(1+sum)
    
print(Hbs(univers_graph,"i"))

print(Att_Arg(opinion_graph,univers_graph))