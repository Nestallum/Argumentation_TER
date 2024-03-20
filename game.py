
from agent import *


def auto_generated_game(UG,number_of_agent):
    
    agents=[]
    PG={"i":[]}
    before_PG = {}
    
    for i in range(number_of_agent):
        agents.append(agent(i,Create_UG_subgraph(UG),UG))
        
    nb_turn=0 
    while(PG != before_PG):
        nb_turn = +1
        before_PG = PG
        print(f"\n tour numero {nb_turn}")
        for i in range(number_of_agent):
            print(f"\n tour de l'agent {agents[i].name}")
            PG=agents[i].best_next_move(PG,UG)



def self_generated_game(UG,agents):
    
    nb_turn=0 
    while(PG != before_PG):
        nb_turn = +1
        before_PG = PG
        print(f"\n tour numero {nb_turn}")
        for i in range(len(agents)):
            print(f"\n tour de l'agent {agents[i].name}")
            PG=agents[i].best_next_move(PG,UG)