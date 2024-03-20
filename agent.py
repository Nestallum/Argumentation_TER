from util import *

UG={"i":["a","b","c"],"b":["e"],"a":["d"],"c":[],"e":[],"d":[]}
OG=Create_OG(["i","a","b","c"],UG)
PG={'i': ['a', 'b'], 'a': [], 'b': []}

class agent :

   def __init__(self,OG,UG,cl=0.1):
       
       self.OG = OG
       self.Vk = Hbs(OG,"i")
       self.cl = cl
       self.lat = Att_Arg(OG,UG)
          
   def get_Vk(self):
       
       return self.Vk
   
   def next_move_possibility(self,PG):
       
       possibility_of_play = []
       
       for keys in PG :
           for keys2,value2 in self.lat.items():
               if(keys in value2) :
                   if(keys2 not in PG.keys()):
                        possibility_of_play.append(keys2)
                   
       print(possibility_of_play)
       
       return possibility_of_play
   
   def best_next_move(self,PG,UG):
       low_borne=self.Vk-self.cl
       high_borne=self.Vk+self.cl
       actual_value=Hbs(PG,"i")
       
       if(actual_value >= low_borne and actual_value <= low_borne):
           
           print("deja dans la zone de confort")
           return PG
       
       possibility_of_play=self.next_move_possibility(PG)
       best_arg = []
       best_value = min(abs(actual_value-low_borne),abs(actual_value-high_borne))
       print(best_value)
       
       if(len(possibility_of_play)==0):
           
           print("aucun coup n'est jouable")
           return PG
       
       for i in possibility_of_play :
           print(i)
           arguments = [keys for keys in PG]
           arguments.append(i)
           PG1 = Create_OG(arguments,UG)
           value = Hbs(PG1,"i")
           value = min(abs(low_borne-value),abs(high_borne-value))
           if(value <= best_value):
               best_arg.append(i)
               best_value=value
               
       if(len(best_arg) == 0):
           
           print(" aucun arguments est assez bon ")
           return PG
       
       arguments=[keys for keys in PG]
       
       arguments.append(best_arg[0])
       print(arguments)
       print(f"on rajoute l'argument {best_arg[0]}")
       
       return Create_OG(arguments,UG)
   

   
print(agent(OG,UG).best_next_move(PG,UG))