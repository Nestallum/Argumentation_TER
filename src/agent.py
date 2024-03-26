# agent.py

"""
This Python script contains a class representing an agent in an argumentation context, along with utility methods for processing and analyzing debate data.

Authors: Mohamed AZZAOUI, Nassim LATTAB
Creation Date: 20/03/2024
"""

from src.util import *

# Represents the agent class.
class agent :
   
    def __init__(self, i, OG, UG, cl=0.05):
        """
        Initializes the agent with its properties.

        Args:
            i (int): The identifier of the agent.
            OG (dict): The opinion graph representing the agent's knowledge.
            UG (dict): The universe graph representing the entire argumentation framework.
            cl (float): The comfort level of the agent (default is 0.05).
        """
       
        self.name=f"agent {i}"
        self.OG = OG
        self.Vk = Hbs(OG, "0") # Value of the agent’s opinion (value of the issue in the agent’s sub-graph).
        self.cl = cl
        self.attackers_adjacency_list = build_attackers_adjacency_list(OG, UG) # List of attackers.
        
    def get_Vk(self) -> float:
        """
            Returns the Belief Strength (Hbs) of the agent's knowledge.

            Returns:
                float: The Belief Strength (Hbs) of the agent.
            """
            
        return self.Vk
    
    def in_comfort_zone(self, PG) -> bool:
        """ Checks if the agent is in its comfort zone.

        Args:
            PG (dict): The public graph representing the current state of the debate.
            UG (dict): The universe graph representing the entire argumentation framework.

        Returns:
            bool: True if the agent is in its comfort zone, False otherwise.
        """

        # Boundaries around ideal value Vk.
        low_borne = self.Vk - self.cl
        high_borne = self.Vk + self.cl

        # Vp the actual value of the issue of the public debate graph.
        Vp = Hbs(PG, "0")
       
        if(Vp >= low_borne and Vp <= high_borne):
            return True
        
        return False
   
    def get_possible_next_moves(self, PG) -> list:
        """
        Returns all the possible moves that can be played by the agent.

        Args:
            PG (dict): The public graph representing the current state of the debate.

        Returns:
            list: A list of arguments that can be added to the public graph.
        """
        
        possible_moves = []
       
        for pg_arg in PG:
            for og_attacker, og_attacked in self.attackers_adjacency_list.items():
                # If an argument in the public graph (PG) is attacked and the attacker is not in PG, then we can add it.
                if(pg_arg in og_attacked and og_attacker not in PG.keys()):
                    possible_moves.append(og_attacker)        
        
        return possible_moves
   
    def best_next_move(self, PG, UG) -> dict:
        """
        Determines the best move for the agent to make towards its comfort zone.

        Args:
            PG (dict): The public graph representing the current state of the debate.
            UG (dict): The universe graph representing the entire argumentation framework.

        Returns:
            dict: The updated public graph after making the best move.
        """

        print(f"\nCurrent value of OG: {self.get_Vk()}")

        Vp = Hbs(PG, "0")
        print(f"Current value of PG: {Vp}")
        
        # Already in comfort zone, plays nothing.
        if(self.in_comfort_zone(PG)):
            print(f"{self.name} is in its comfort zone. No need to play an argument.")
            return PG
        
        # Else, find the best argument to play.
        print(f"{self.name} is not in its comfort zone.")

        possible_moves = self.get_possible_next_moves(PG)

        # If there is no argument to play.
        if(len(possible_moves) == 0):
            print("No playable moves, no addition.")
            return PG
        
        # Else, find the best argument to play.
        arg_to_play = None
        gap_to_minimize = abs(Vp - self.get_Vk())
        for move in possible_moves :
            arguments = [keys for keys in PG]
            # Generate temporal PG to test its new value adding a new move.
            arguments.append(move)
            temp_PG = generate_subgraph(UG, arguments)
            temp_Vp = Hbs(temp_PG, "0")
            temp_gap = abs(temp_Vp - self.get_Vk())

            # Updating the best value
            if(temp_gap < gap_to_minimize):
                arg_to_play = move
                gap_to_minimize = temp_gap
        
        # If no argument brings him closer to his comfort zone.
        if(arg_to_play == None):
            print("No good arguments, no addition.")
            return PG
        
        # Else, plays one of the goods arguments.
        arguments = [keys for keys in PG]
        arguments.append(arg_to_play)
        
        # Final prints
        print(f"{self.name} adds argument {arg_to_play} to the public graph.")
        new_PG = generate_subgraph(UG, arguments)
        new_Vp = Hbs(new_PG, "0")
        print(f"Vp of public graph now: {new_Vp}")
        
        # Generate new PG
        return new_PG