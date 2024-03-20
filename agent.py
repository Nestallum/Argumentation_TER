from Argumentation_TER.util import *


class agent :

   def __init__(self,OG,Vk,lat,UG,cl=0.1):
       self.OG = OG
       self.Vk = Hbs(OG,"i")
       self.cl = cl
       self.lat = Att_ARG(OG,UG)
   def get_hbs(self):
       return self.hbs
   
   def next_move_possibility(self,PG):
       possibility_of_play = []
       
       for keys in PG :
           for keys2,items2 in self.lat.items():
               if(keys in items2) :
                   possibility_of_play.append(keys2)
                   
       print(possibility_of_play)
       return possibility_of_play
   
   def best_next_move(self,PG,UG):
       possibility_of_play=self.next_move_possibility(self,PG)
       for i in range(len(possibility_of_play)):
           