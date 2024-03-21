from util import *

UG={"i":["a","b","c"],"b":["e"],"a":["d"],"c":[],"e":[],"d":[]}
OG=generate_OG(["i","a","b","c"],UG)
PG={'i': ['a', 'b'], 'a': [], 'b': []}

# represente la class agent 
class agent :
   # initialise l'agent
   def __init__(self,i,OG,UG,cl=0.05):
       
       self.name=f"agent {i}"
       self.OG = OG
       self.Vk = Hbs(OG,"i")
       self.cl = cl
       self.lat = build_attackers_adjacency_list(OG,UG)
       
   # renvoie le hbs de l'agent   
   def get_Vk(self):
       
       return self.Vk
   # dis si l'agent est dans sa zone de confort ou pas
   def in_confort_zone(self,PG,UG):
       
       low_borne=self.Vk-self.cl
       high_borne=self.Vk+self.cl
       actual_value=Hbs(PG,"i")
       
       if(actual_value >= low_borne and actual_value <= high_borne):
           
           print(f"{self.name} est dans ça zone de confort")
           return True
       
       print(f"{self.name} est pas dans ça zone de confort")
       return False
   
   # renvoie tout les coups qui attaque un argument du graphe public
   def next_move_possibility(self,PG):
       
       possibility_of_play = []
       
       for keys in PG :
           for keys2,value2 in self.lat.items():
               if(keys in value2) :
                   if(keys2 not in PG.keys()):
                        possibility_of_play.append(keys2)
                   
       print(possibility_of_play)
       
       return possibility_of_play
   
   # les coups qui rapprochent le plus possible l'agent de sa zone de confort 
   def best_next_move(self,PG,UG):
       
       low_borne=self.Vk-self.cl
       high_borne=self.Vk+self.cl
       actual_value=Hbs(PG,"i")
       
       #l'agent est deja dans al zone de confort donc il ne joue pas
       if(actual_value >= low_borne and actual_value <= high_borne):
           
           print("\n deja dans la zone de confort")
           return PG
       
       possibility_of_play=self.next_move_possibility(PG)
       best_arg = []
       best_value = min(abs(actual_value-low_borne),abs(actual_value-high_borne))
       print(best_value)
       #il n'a aucun coup disponible 
       if(len(possibility_of_play)==0):
           
           print("\n aucun coup n'est jouable donc aucun ajout")
           return PG
       
       for i in possibility_of_play :
           print(i)
           arguments = [keys for keys in PG]
           arguments.append(i)
           PG1 = generate_OG(arguments,UG)
           value = Hbs(PG1,"i")
           value = min(abs(low_borne-value),abs(high_borne-value))
           if(value <= best_value):
               best_arg.append(i)
               best_value=value
       
       # aucun arguments le rapproche de sa zone de confort
       if(len(best_arg) == 0):
           
           print("\naucun arguments est assez bon donc aucun ajout ")
           return PG
       
       
       arguments=[keys for keys in PG]
       print(arguments)
       #il joue un arguments qui le rapproche de sa zone de confort  
       arguments.append(best_arg[0])
       
       print(f"\n {self.name}  rajoute l'argument {best_arg[0]} au public graph ")
       
       return generate_OG(arguments,UG)
   

 
print(Hbs(PG,"i")) 
print(Hbs(OG,"i")) 
