import search
import random
import math
from typing import Dict, Any
import hashlib
import json
from itertools import product




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
        self.pirate_ships = initial["pirate_ships"]
        self.treasures = initial["treasures"]
        self.marine_paths = initial["marine_ships"]
        self.marine_direction = {}
        for key, value in self.marine_paths.items():
            self.marine_direction[key] = "forward"

        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                if self.map[i][j] == "B":
                    base_location = (i, j)
                    self.base = base_location
        start_state = {}
        start_state["base"] = self.base

        # Start build the initial state , we want ships location
        start_state["pirate_ships"] = self.pirate_ships

        marine_locations = {}
        for key, value in self.marine_paths.items():
            marine_name = key
            marine_start = value[0]
            marine_locations[marine_name] = marine_start
        start_state["marine_locations"] = marine_locations
        # We want to save treasures , if tresaure stilll not taken he will be part of treasures in  state
        start_state["treasures"] = self.treasures
        # Treasures_in_base- holding the tresaures , this will help us to define the goal
        start_state["treasures_in_base"] = {}
        # We want to model the loading of treasure
        treasures_on_ship = {}
        for key, value in self.pirate_ships.items():
            treasures_on_ship[key] = []
        start_state["treasures_on_ship"] = treasures_on_ship


        # Defined the inital state , now will send to initial in parent class
        initial = start_state
        # Our goal is that treasures in base will be with all treasures
        self.goal = {"treasures_in_base": self.treasures}

        search.Problem.__init__(self, initial,self.goal)

    def actions(self, state):
        """Returns all the actions that can be executed in the given
        state. The result should be a tuple (or other iterable) of actions
        as defined in the problem description file"""
        # Define borders
        map = self.map
        right_border, left_border = len(map[0]) - 1, 0
        down_border, up_border = len(map) - 1, 0
        all_actions_all_ships = []
        for key, value in state["pirate_ships"].items():
            optional_actions_per_ship = []
            x, y = value[0], value[1]
            # Sail
            # Sail down
            if x < down_border and map[x + 1][y] != "I":
                sail_down = ("sail", key, (x + 1, y))
                optional_actions_per_ship.append(sail_down)
            # Sail up
            if x > up_border and map[x - 1][y] != "I":
                sail_up = ("sail", key, (x - 1, y))
                optional_actions_per_ship.append(sail_up)

            # Sail left
            if y > left_border and map[x][y - 1] != "I":
                sail_left = ("sail", key, (x, y - 1))
                optional_actions_per_ship.append(sail_left)

            # Sail right
            if y < right_border and map[x][y + 1] != "I":
                sail_right = ("sail", key, (x, y + 1))
                optional_actions_per_ship.append(sail_right)

            # Collect Treasures
            # treasure down
            if x < down_border and map[x + 1][y] == "I" and (x + 1, y) in state["treasures"].values() and len(state["treasures_on_ship"][key]) < 2:
                treasure_name = self.get_key((x + 1, y),state["treasures"])
                collect_treasure_down = ("collect_treasure", key, treasure_name)
                optional_actions_per_ship.append(collect_treasure_down)

            # treasure up
            if x > up_border and map[x - 1][y] == "I" and (x - 1, y) in state["treasures"].values() and len(state["treasures_on_ship"][key]) < 2:
                treasure_name = self.get_key((x - 1, y),state["treasures"])
                collect_treasure_up = ("collect_treasure", key, treasure_name)
                optional_actions_per_ship.append(collect_treasure_up)

            # treasure left
            if y > left_border and map[x][y - 1] == "I" and (x, y - 1) in state["treasures"].values() and len(state["treasures_on_ship"][key]) < 2:
                treasure_name = self.get_key((x, y - 1),state["treasures"])
                collect_treasure_left = ("collect_treasure", key, treasure_name)
                optional_actions_per_ship.append(collect_treasure_left)

            # treasure right
            if y < right_border and map[x][y + 1] == "I" and (x, y + 1) in state["treasures"].values() and len(state["treasures_on_ship"][key]) < 2:
                treasure_name = self.get_key((x, y + 1),state["treasures"])
                collect_treasure_right = ("collect_treasure", key, treasure_name)
                optional_actions_per_ship.append(collect_treasure_right)

            # Deposit Treasure
            if map[x][y] == "B" and len(state["treasures_on_ship"][key]) != 0:
                deposit = ("deposit_treasure", key)
                optional_actions_per_ship.append(deposit)

            # Wait
            wait = ("wait", key)
            optional_actions_per_ship.append(wait)

            all_actions_all_ships.append(optional_actions_per_ship)
        cartesian_Product = list(product(*all_actions_all_ships, repeat=1))
        return cartesian_Product

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        # move pirate ship's to the next step , go over every ship
        for key, value in state["marine_locations"].items():
            # if the ship is static and array len is one so go on
            if len(self.marine_paths[key]) == 1:
                continue

            if self.marine_direction[key] == "forward":
                # if i reached the end so go back on track
                if self.marine_paths[key].index(value) == len(self.marine_paths[key]) - 1:
                    self.marine_direction[key] = "back"
                    state["marine_locations"][key] = self.marine_paths[key][-2]
                # if i'm in the middle
                else:
                    state["marine_locations"][key] = self.marine_paths[key][self.marine_paths[key].index(value) + 1]
                continue

            if self.marine_direction[key] == "back":
                # if i reached the start so go back forward
                if self.marine_paths[key].index(value) == 0:
                    self.marine_direction[key] = "forward"
                    state["marine_locations"][key] = self.marine_paths[key][1]
                # if i'm in the middle
                else:
                    state["marine_locations"][key] = self.marine_paths[key][self.marine_paths[key].index(value) - 1]
        # lets iterate over the actions
        for one_action in action:
            # dont need to do anything
            if one_action[0] == "wait":
                continue
            # continue to the next sail point
            if one_action[0] == "sail":
                state["pirate_ships"][one_action[1]] = one_action[2]
                continue
            # deposit all treasures on ship to base
            #(“deposit_treasure”, “pirate_1”)
            if one_action[0] == "deposit_treasure":
                hash_list = []
                for key, value in state["treasures_in_base"].items():
                    hash_list.append((key,value))
                for treasure in state["treasures_on_ship"][one_action[1]]:
                    if treasure not in hash_list:
                        state["treasures_in_base"][treasure[0]] = treasure[1]
                state["treasures_on_ship"][one_action[1]].clear()
                continue

            if one_action[0] == "collect_treasure":
                # take the treasure to the ship
                # check treasures when it is tuple or name
                state["treasures_on_ship"][one_action[1]].append((one_action[2],self.treasures[one_action[2]]))

        for key, value in state["pirate_ships"].items():
            if value in state["marine_locations"].values():
                if len(state["treasures_on_ship"][key]) == 0:
                    continue
                else:state["treasures_on_ship"][key].clear()
        result = state
        print(result)
        return result

    def goal_test(self, state):
        """ Given a state, checks if this is the goal state.
         Returns True if it is, False otherwise."""
        first_hash_value = self.dict_hash(state["treasures_in_base"])
        second_hash_value = self.dict_hash(self.goal["treasures_in_base"])
        return first_hash_value == second_hash_value

    def h(self, node):
        """ This is the heuristic. It gets a node (not a state,
        state can be accessed via node.state)
        and returns a goal distance estimate"""
        return self.h_1(node)

    """Feel free to add your own functions
    (-2, -2, None) means there was a timeout"""


    def h_1(self,node):
        state = node.getstate()
        #lets figure which treasures in base :
        base_treasures = list(state["treasures_in_base"].keys())
        #[treasure_1 , treasure_2]
        #Lets figure which treasures are in
        parsed_list = list(state["treasures_on_ship"].values())
        for i in parsed_list:
            #if there is no treasure on ship the list will be []
            if len(i) == 0 :
                continue
            #check if base hasn't this treasure
            for j in i:
                if j[0] not in base_treasures:
                    base_treasures.append(j[0])
        return (len(self.treasures) - len(base_treasures))/ len(self.pirate_ships)

    def h_2(self,Node):
        state = Node.getstate()
        sum_distances = 0
        # Board borders
        map = self.map
        right_border, left_border = len(map[0]) - 1, 0
        down_border, up_border = len(map) - 1, 0
        for t_num, t_location in state["treasures"].items():
            # If treasure already deposit, the distance is zero
            if t_num in list(state["treasures_in_base"].keys()):
                sum_distances += 0
                continue
            # If everywhere is islands, return infinty
            x_t, y_t = t_location[0], t_location[1]
            # False == sea,  True == Island or unreachable
            up, down, left, right = True, True, True, True
            #down
            if x_t < down_border and map[x_t + 1][y_t] != "I":
                down = False
            #up
            if x_t > up_border and map[x_t - 1][y_t] != "I":
                up = False
            # left
            if y_t > left_border and map[x_t][y_t - 1] != "I":
                left = False
            #right
            if y_t < right_border and map[x_t][y_t + 1] != "I":
                right = False
            # if no access at all, return infinity
            if up and down and left and right:
                sum_distances += float('inf')
                break
            # if treasure on ships and not deposit
            # for each ship, if the treasure on ship, find the distance from the ship to the base
            minimum_distance = float('inf')
            for ship, treasures_list in state["treasures_on_ship"].items():
                if (t_num , t_location) in treasures_list:
                    ship_location = state["pirate_ships"][ship]
                    x_ship , y_ship = ship_location[0], ship_location[1]
                    ship_distance = abs(x_t - x_ship) + abs(y_t - y_ship)
                    if ship_distance < minimum_distance:
                        minimum_distance = ship_distance
            # take the minimum distance
            if minimum_distance < float('inf'):
                sum_distances += minimum_distance
                continue
            minimum_distance = float('inf')
            x_base , y_base = self.base[0], self.base[1]
            if not up:
                adjacent_distance = abs(x_t - 1 - x_base) + abs(y_t - y_base)
                if adjacent_distance < minimum_distance:
                    minimum_distance = adjacent_distance
            if not down:
                adjacent_distance = abs(x_t + 1 - x_base) + abs(y_t - y_base)
                if adjacent_distance < minimum_distance:
                    minimum_distance = adjacent_distance
            if not left:
                adjacent_distance = abs(x_t - x_base) + abs(y_t - 1 - y_base)
                if adjacent_distance < minimum_distance:
                    minimum_distance = adjacent_distance
            if not right:
                adjacent_distance = abs(x_t - x_base) + abs(y_t + 1 - y_base)
                if adjacent_distance < minimum_distance:
                    minimum_distance = adjacent_distance
            if minimum_distance < float('inf'):
                sum_distances += minimum_distance
                continue
        return sum_distances / len(self.pirate_ships)



    def dict_hash(self,dictionary: Dict[str, Any]) -> str:
        """MD5 hash of a dictionary."""
        dhash = hashlib.md5()
        # We need to sort arguments so {'a': 1, 'b': 2} is
        # the same as {'b': 2, 'a': 1}
        encoded = json.dumps(dictionary, sort_keys=True).encode()
        dhash.update(encoded)
        return dhash.hexdigest()

    def get_key(self ,val , my_dict):
        for key, value in my_dict.items():
            if val == value:
                return key

        return "key doesn't exist"

def create_onepiece_problem(game):
    return OnePieceProblem(game)


