import search
import random
import math
from typing import Dict, Any
import hashlib
import json




ids = ["209512664", "206703191"]


class OnePieceProblem(search.Problem):
    """This class implements a medical problem according to problem description file"""
    # {
    #     "map": [
    #         ['S', 'S', 'I', 'S'],
    #         ['S', 'S', 'S', 'S'],
    #         ['B', 'S', 'S', 'S'],
    #         ['S', 'S', 'S', 'S']
    #     ],
    #     "pirate_ships": {"pirate_ship_1": (2, 0)},
    #     "treasures": {'treasure_1': (0, 2)},
    #     "marine_ships": {'marine_1': [(1, 1), (1, 2), (2, 2), (2, 1)]}
    # }
    def __init__(self, initial):
        """Don't forget to implement the goal test
        You should change the initial to your own representation.
        search.Problem.__init__(self, initial) creates the root node"""
        ##saving the class atributes for use
        self.map = initial["map"]
        self.pirat_ships = initial["pirate_ships"]
        self.treasures = initial["treasures"]
        self.marine_paths = initial["marine_ships"]

        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                if self.map[i][j] == "B":
                    base_location = (i,j)
        self.base = base_location
        start_state[base] = self.base

        #start build the initial state , we want ships location
        start_state = {self.pirat_ships}

        marine_locations = {}
        for key,value in self.marine_paths:
            marine_name = key
            marine_start = value[0]
            marine_locations[marine_name] = marine_start
        start_state[marine_positions] = marine_locations
        #we want to save treasures , if tresaure stilll not taken he will be part of treasures in  state
        start_state[treasures] = self.treasures
        #treasures_in_base- holding the tresaures , this will help us to define the goal
        start_state[treasures_in_base] = {}
        #we want to model the loading of treasure
        treasures_ships = {}
        for key, value in self.pirat_ships:
            treasures_ships[key] = []
        start_state[treasures_on_ship] = treasures_ship




        search.Problem.__init__(self, initial)
        
    def actions(self, state):
        """Returns all the actions that can be executed in the given
        state. The result should be a tuple (or other iterable) of actions
        as defined in the problem description file"""

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""

    def goal_test(self, state):
        """ Given a state, checks if this is the goal state.
         Returns True if it is, False otherwise."""

    def h(self, node):
        """ This is the heuristic. It gets a node (not a state,
        state can be accessed via node.state)
        and returns a goal distance estimate"""
        return 0

    """Feel free to add your own functions
    (-2, -2, None) means there was a timeout"""

    def dict_hash(dictionary: Dict[str, Any]) -> str:
        """MD5 hash of a dictionary."""
        dhash = hashlib.md5()
        # We need to sort arguments so {'a': 1, 'b': 2} is
        # the same as {'b': 2, 'a': 1}
        encoded = json.dumps(dictionary, sort_keys=True).encode()
        dhash.update(encoded)
        return dhash.hexdigest()


def create_onepiece_problem(game):
    return OnePieceProblem(game)


