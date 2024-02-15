import search_209512664_206703191
import random
import math
from typing import Dict, Any
import hashlib
import json
from itertools import product


ids = ["209512664", "206703191"]


class OnePieceProblem(search_209512664_206703191.Problem):
    """This class implements a medical problem according to problem description file"""

    def __init__(self, initial):
        """Don't forget to implement the goal test
        You should change the initial to your own representation.
        search.Problem.__init__(self, initial) creates the root node"""
        ##saving the class atributes for use
        self.map = initial["map"]
        self.pirate_ships = initial["pirate_ships"]
        self.treasures = initial["treasures"]
        #ask whats happen if there is no marine ships
        self.marine_paths = initial["marine_ships"]
        self.marine_direction = {}
        for key, value in self.marine_paths.items():
            self.marine_direction[key] = "forward"
        #take one random ship
        self.rand_ship = next(iter(self.pirate_ships))
        #take one random treasure
        self.rand_treasure = next(iter(self.treasures))
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                if self.map[i][j] == "B":
                    base_location = (i, j)
                    self.base = base_location
        start_state = {}

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
            treasures_on_ship[key] = (None , None)

        start_state["treasures_on_ship"] = treasures_on_ship

        start_state["marine_direction"] = {}
        for key, value in self.marine_paths.items():
            start_state["marine_direction"][key] = "forward"

        start_state_set = self.dict_to_frozenset(start_state)

        # Defined the inital state , now will send to initial in parent class
        initial = start_state_set
        # Our goal is that treasures in base will be with all treasures
        goal_dict =  self.treasures
        self.goal = self.dict_to_frozenset(goal_dict)



        search_209512664_206703191.Problem.__init__(self, initial, self.goal)

    def actions(self, state):
        """Returns all the actions that can be executed in the given
        state. The result should be a tuple (or other iterable) of actions
        as defined in the problem description file"""
        state_dict = self.frozenset_to_dict(state)
        # Define borders
        map = self.map
        right_border, left_border = len(map[0]) - 1, 0
        down_border, up_border = len(map) - 1, 0
        # Initial new list that will hold all actions for all the ships
        all_actions_all_ships = []
        # Iterate the pirate ships and creates all the possible actions for each ship
        state_dict["pirate_ships"].items()
        for ship_name, value in state_dict["pirate_ships"].items():
            optional_actions_per_ship = []
            x, y = value[0], value[1]
            # Sail
            # Sail down
            if x < down_border and map[x + 1][y] != "I":
                sail_down = ("sail", ship_name, (x + 1, y))
                optional_actions_per_ship.append(sail_down)
            # Sail up
            if x > up_border and map[x - 1][y] != "I":
                sail_up = ("sail", ship_name, (x - 1, y))
                optional_actions_per_ship.append(sail_up)

            # Sail left
            if y > left_border and map[x][y - 1] != "I":
                sail_left = ("sail", ship_name, (x, y - 1))
                optional_actions_per_ship.append(sail_left)

            # Sail right
            if y < right_border and map[x][y + 1] != "I":
                sail_right = ("sail", ship_name, (x, y + 1))
                optional_actions_per_ship.append(sail_right)

            # Collect Treasures
            # treasure down
            if x < down_border and map[x + 1][y] == "I" and (x + 1, y) in state_dict["treasures"].values() and self.check_capcity(state_dict , ship_name) < 2:
                keys_number, keys = self.get_all_keys((x + 1, y), state_dict["treasures"])
                for item in keys:
                    #if the it is rand_trasure and no rand_ship so dont append but continue
                    if item == self.rand_treasure and ship_name != self.rand_ship:
                        continue
                    action = ("collect_treasure", ship_name, item)
                    optional_actions_per_ship.append(action)

            # treasure up
            if x > up_border and map[x - 1][y] == "I" and (x - 1, y) in state_dict["treasures"].values() and self.check_capcity(state_dict , ship_name) < 2:
                keys_number, keys = self.get_all_keys((x - 1, y), state_dict["treasures"])
                for item in keys:
                    if item == self.rand_treasure and ship_name != self.rand_ship:
                        continue
                    action = ("collect_treasure", ship_name, item)
                    optional_actions_per_ship.append(action)

            # treasure left
            if y > left_border and map[x][y - 1] == "I" and (x, y - 1) in state_dict["treasures"].values() and self.check_capcity(state_dict , ship_name) < 2:
                keys_number, keys = self.get_all_keys((x, y - 1), state_dict["treasures"])
                for item in keys:
                    if item == self.rand_treasure and ship_name != self.rand_ship:
                        continue
                    action = ("collect_treasure", ship_name, item)
                    optional_actions_per_ship.append(action)

            # treasure right
            if y < right_border and map[x][y + 1] == "I" and (x, y + 1) in state_dict["treasures"].values() and self.check_capcity(state_dict , ship_name) < 2:
                keys_number, keys = self.get_all_keys((x, y + 1), state_dict["treasures"])
                for item in keys:
                    if item == self.rand_treasure and ship_name != self.rand_ship:
                        continue
                    action = ("collect_treasure", ship_name, item)
                    optional_actions_per_ship.append(action)

            # Deposit Treasure
            if map[x][y] == "B" and self.check_capcity(state_dict , ship_name) != 0:
                deposit = ("deposit_treasure", ship_name)
                optional_actions_per_ship.append(deposit)

            # Wait
            wait = ("wait", ship_name)
            optional_actions_per_ship.append(wait)

            all_actions_all_ships.append(optional_actions_per_ship)
        cartesian_Product = list(product(*all_actions_all_ships, repeat=1))
        return cartesian_Product

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        # move pirate ship's to the next step , go over every ship
        result = self.frozenset_to_dict(state)
        for key, value in result["marine_locations"].items():
            #if there is no marine ships than break
            if result["marine_locations"] is None:
                break
            # if the ship is static and array len is one so go on
            if len(self.marine_paths[key]) == 1:
                continue

            if result["marine_direction"][key] == "forward":
                # if i reached the end so go back on track
                if self.marine_paths[key].index(value) == len(self.marine_paths[key]) - 1:
                    result["marine_direction"][key] = "back"
                    result["marine_locations"][key] = self.marine_paths[key][-2]
                # if i'm in the middle
                else:
                    result["marine_locations"][key] = self.marine_paths[key][self.marine_paths[key].index(value) + 1]
                continue

            if result["marine_direction"][key] == "back":
                # if i reached the start so go back forward
                if self.marine_paths[key].index(value) == 0:
                    result["marine_direction"][key] = "forward"
                    result["marine_locations"][key] = self.marine_paths[key][1]
                # if i'm in the middle
                else:
                    result["marine_locations"][key] = self.marine_paths[key][self.marine_paths[key].index(value) - 1]
        # lets iterate over the actions
        for one_action in action:
            # dont need to do anything
            if one_action[0] == "wait":
                continue
            # continue to the next sail point
            if one_action[0] == "sail":
                result["pirate_ships"][one_action[1]] = one_action[2]
                continue
            # deposit all treasures on ship to base
            #(“deposit_treasure”, “pirate_1”)
            if one_action[0] == "deposit_treasure":
                hash_list = []
                for key, value in result["treasures_in_base"].items():
                    hash_list.append((key,value))
                for treasure in result["treasures_on_ship"][one_action[1]]:
                    if treasure not in hash_list and treasure is not None:
                        result["treasures_in_base"][treasure] = self.treasures[treasure]
                result["treasures_on_ship"][one_action[1]] = (None,None)
                continue

            if one_action[0] == "collect_treasure":
                # take the treasure to the ship
                # check treasures when it is tuple or name
                #check if tuple on place 1 exists
                if result["treasures_on_ship"][one_action[1]][0] is None:
                    new_tuple = (one_action[2] , None)
                    result["treasures_on_ship"][one_action[1]] = new_tuple
                else:
                    new_tuple = (result["treasures_on_ship"][one_action[1]][0] ,one_action[2] )
                    result["treasures_on_ship"][one_action[1]] = new_tuple
        for key, value in result["pirate_ships"].items():
            #if there is no marine ships so pass
            if  result["marine_locations"] == {}:
                break
            if value in result["marine_locations"].values():
                result["treasures_on_ship"][key] = (None,None)
        result_set = self.dict_to_frozenset(result)
        return result_set

    def goal_test(self, state):
        """ Given a state, checks if this is the goal state.
         Returns True if it is, False otherwise."""
        state_dict = self.frozenset_to_dict(state)
        goal_part  = self.dict_to_frozenset(state_dict["treasures_in_base"])
        return self.goal == goal_part

    # def h(self , node):
    #     state = node.getstate()
    #     state_dict = self.frozenset_to_dict(state)
    #     sum_distances = 0
    #     # Board borders
    #     map = self.map
    #     right_border, left_border = len(map[0]) - 1, 0
    #     bottom_border, top_border = len(map) - 1, 0
    #     for t_name, t_location in state_dict["treasures"].items():
    #         # If treasure already deposit, the distance is zero
    #         if t_name in list(state_dict["treasures_in_base"].keys()):
    #             sum_distances += 0
    #             continue
    #         # If everywhere is islands, return infinty
    #         x_t, y_t = t_location[0], t_location[1]
    #         # False == sea,  True == Island or unreachable
    #         up, down, left, right = True, True, True, True
    #         # down
    #         if x_t < bottom_border and map[x_t + 1][y_t] != "I":
    #             down = False
    #         # up
    #         if x_t > top_border and map[x_t - 1][y_t] != "I":
    #             up = False
    #         # left
    #         if y_t > left_border and map[x_t][y_t - 1] != "I":
    #             left = False
    #         # right
    #         if y_t < right_border and map[x_t][y_t + 1] != "I":
    #             right = False
    #         # if no access at all, return infinity
    #         if up and down and left and right:
    #             sum_distances += float('inf')
    #             break
    #         # if treasure on ships and not deposit
    #         # for each ship, if the treasure on ship, find the distance from the ship to the base
    #         minimum_distance_ship = float('inf')
    #         x_base, y_base = self.base[0], self.base[1]
    #         for ship, treasures_tuple in state_dict["treasures_on_ship"].items():
    #             treasure_list = [treasures_tuple[0], treasures_tuple[1]]
    #             if t_name in treasure_list:
    #                 ship_location = state_dict["pirate_ships"][ship]
    #                 x_ship, y_ship = ship_location[0], ship_location[1]
    #                 ship_distance = abs(x_base - x_ship) + abs(y_base - y_ship)
    #                 if ship_distance < minimum_distance_ship:
    #                     minimum_distance_ship = ship_distance
    #         # take the minimum distance
    #         minimum_distance_island = float('inf')
    #
    #         if not up:
    #             adjacent_distance = abs(x_t - 1 - x_base) + abs(y_t - y_base)
    #             if adjacent_distance < minimum_distance_island:
    #                 minimum_distance_island = adjacent_distance
    #         if not down:
    #             adjacent_distance = abs(x_t + 1 - x_base) + abs(y_t - y_base)
    #             if adjacent_distance < minimum_distance_island:
    #                 minimum_distance_island = adjacent_distance
    #         if not left:
    #             adjacent_distance = abs(x_t - x_base) + abs(y_t - 1 - y_base)
    #             if adjacent_distance < minimum_distance_island:
    #                 minimum_distance_island = adjacent_distance
    #         if not right:
    #             adjacent_distance = abs(x_t - x_base) + abs(y_t + 1 - y_base)
    #             if adjacent_distance < minimum_distance_island:
    #                 minimum_distance_island = adjacent_distance
    #
    #         if minimum_distance_island < float('inf') and minimum_distance_ship < float('inf'):
    #             print(minimum_distance_island)
    #         sum_distances += min(minimum_distance_island , 0.5 * minimum_distance_ship)
    #     return sum_distances / len(self.pirate_ships)
    def h_sum_to(self, node):
        state = node.getstate()
        state_dict = self.frozenset_to_dict(state)
        sum_distances = 0
        # Board borders
        map = self.map
        right_border, left_border = len(map[0]) - 1, 0
        bottom_border, top_border = len(map) - 1, 0
        for t_name, t_location in state_dict["treasures"].items():
            # If treasure already deposit, the distance is zero
            if t_name in list(state_dict["treasures_in_base"].keys()):
                sum_distances += 0
                continue
            # If everywhere is islands, return infinty
            x_t, y_t = t_location[0], t_location[1]
            # False == sea,  True == Island or unreachable
            up, down, left, right = True, True, True, True
            # down
            if x_t < bottom_border and map[x_t + 1][y_t] != "I":
                down = False
            # up
            if x_t > top_border and map[x_t - 1][y_t] != "I":
                up = False
            # left
            if y_t > left_border and map[x_t][y_t - 1] != "I":
                left = False
            # right
            if y_t < right_border and map[x_t][y_t + 1] != "I":
                right = False
            # if no access at all, return infinity
            if up and down and left and right:
                sum_distances += float('inf')
                break
            # if treasure on ships and not deposit
            # for each ship, if the treasure on ship, find the distance from the ship to the base
            minimum_distance = float('inf')
            x_base, y_base = self.base[0], self.base[1]
            for ship, treasures_tuple in state_dict["treasures_on_ship"].items():
                treasure_list = [treasures_tuple[0], treasures_tuple[1]]
                if t_name in treasure_list:
                    ship_location = state_dict["pirate_ships"][ship]
                    x_ship, y_ship = ship_location[0], ship_location[1]
                    ship_distance = self.euclidian_distance(x_ship,y_ship ,x_base , y_base) + self.find_distance_closest_treasure(None,x_ship,y_ship)
                    if ship_distance < minimum_distance:
                        minimum_distance = ship_distance
            # take the minimum distance
            if minimum_distance < float('inf'):
                sum_distances += minimum_distance
                continue
            minimum_distance = float('inf')

            if not up:
                adjacent_distance =self.euclidian_distance(x_t - 1 ,y_t ,x_base , y_base)
                if adjacent_distance < minimum_distance:
                    minimum_distance = adjacent_distance + self.find_distance_closest_treasure(t_name,x_t - 1 ,y_t )
            if not down:
                adjacent_distance = self.euclidian_distance(x_t + 1 ,y_t ,x_base , y_base)
                if adjacent_distance < minimum_distance:
                    minimum_distance = adjacent_distance + self.find_distance_closest_treasure(t_name,x_t + 1 ,y_t )
            if not left:
                adjacent_distance = self.euclidian_distance(x_t ,y_t - 1 ,x_base , y_base)
                if adjacent_distance < minimum_distance:
                    minimum_distance = adjacent_distance + self.find_distance_closest_treasure(t_name,x_t ,y_t - 1 )
            if not right:
                adjacent_distance = self.euclidian_distance(x_t  ,y_t + 1 ,x_base , y_base)
                if adjacent_distance < minimum_distance:
                    minimum_distance = adjacent_distance + self.find_distance_closest_treasure(t_name,x_t  ,y_t + 1 )
            if minimum_distance < float('inf'):
                sum_distances += minimum_distance
                continue
        return sum_distances / len(self.pirate_ships)



    def find_distance_closest_treasure(self ,is_treasure,x_t , y_t):
        distance = float('inf')
        if len(self.treasures.values()) == 1 :
            return 0
        for key,value in self.treasures.items():
            if is_treasure is not None :
                if key == is_treasure:
                    continue
            dist = self.euclidian_distance(x_t , y_t , value[0] , value [1])
            if distance > dist:
                distance = dist

        return distance



    def h_max(self,node):

        state = node.getstate()
        state_dict = self.frozenset_to_dict(state)
        distances = {}
        # Board borders
        map = self.map
        right_border, left_border = len(map[0]) - 1, 0
        bottom_border, top_border = len(map) - 1, 0
        for t_name, t_location in state_dict["treasures"].items():
            # If treasure already deposit, the distance is zero
            if t_name in list(state_dict["treasures_in_base"].keys()):
                distances[t_name] = 0
                continue
            # If everywhere is islands, return infinty
            x_t, y_t = t_location[0], t_location[1]
            # False == sea,  True == Island or unreachable
            up, down, left, right = True, True, True, True
            # down
            if x_t < bottom_border and map[x_t + 1][y_t] != "I":
                down = False
            # up
            if x_t > top_border and map[x_t - 1][y_t] != "I":
                up = False
            # left
            if y_t > left_border and map[x_t][y_t - 1] != "I":
                left = False
            # right
            if y_t < right_border and map[x_t][y_t + 1] != "I":
                right = False
            # if no access at all, return infinity
            if up and down and left and right:
                distances[t_name] = float('inf')
                break
            # if treasure on ships and not deposit
            # for each ship, if the treasure on ship, find the distance from the ship to the base
            minimum_distance = float('inf')
            x_base, y_base = self.base[0], self.base[1]
            for ship, treasures_tuple in state_dict["treasures_on_ship"].items():
                treasure_list = [treasures_tuple[0], treasures_tuple[1]]
                if t_name in treasure_list:
                    ship_location = state_dict["pirate_ships"][ship]
                    x_ship, y_ship = ship_location[0], ship_location[1]
                    ship_distance = self.euclidian_distance(x_ship,y_ship ,x_base , y_base)
                    if ship_distance < minimum_distance:
                        minimum_distance = ship_distance
            # take the minimum distance
            if minimum_distance < float('inf'):
                distances[t_name] = minimum_distance
                continue

            minimum_distance = float('inf')

            if not up:
                adjacent_distance =self.euclidian_distance(x_t - 1 ,y_t ,x_base , y_base)
                if adjacent_distance < minimum_distance:
                    minimum_distance = adjacent_distance
            if not down:
                adjacent_distance = self.euclidian_distance(x_t + 1 ,y_t ,x_base , y_base)
                if adjacent_distance < minimum_distance:
                    minimum_distance = adjacent_distance
            if not left:
                adjacent_distance = self.euclidian_distance(x_t ,y_t - 1 ,x_base , y_base)
                if adjacent_distance < minimum_distance:
                    minimum_distance = adjacent_distance
            if not right:
                adjacent_distance = self.euclidian_distance(x_t  ,y_t + 1 ,x_base , y_base)
                if adjacent_distance < minimum_distance:
                    minimum_distance = adjacent_distance
            if minimum_distance < float('inf'):
                distances[t_name] = minimum_distance
                continue
        return max(distances.values())

    def h(self, node):
        """ This is the heuristic. It gets a node (not a state,
        state can be accessed via node.state)
        and returns a goal distance estimate"""

        state = node.getstate()
        state_dict = self.frozenset_to_dict(state)
        sum_distances = 0
        # Board borders
        map = self.map
        right_border, left_border = len(map[0]) - 1, 0
        bottom_border, top_border = len(map) - 1, 0
        for t_name, t_location in state_dict["treasures"].items():
            # If treasure already deposit, the distance is zero
            if t_name in list(state_dict["treasures_in_base"].keys()):
                sum_distances += 0
                continue
            # If everywhere is islands, return infinty
            x_t, y_t = t_location[0], t_location[1]
            # False == sea,  True == Island or unreachable
            up, down, left, right = True, True, True, True
            # down
            if x_t < bottom_border and map[x_t + 1][y_t] != "I":
                down = False
            # up
            if x_t > top_border and map[x_t - 1][y_t] != "I":
                up = False
            # left
            if y_t > left_border and map[x_t][y_t - 1] != "I":
                left = False
            # right
            if y_t < right_border and map[x_t][y_t + 1] != "I":
                right = False
            # if no access at all, return infinity
            if up and down and left and right:
                sum_distances += float('inf')
                break
            # if treasure on ships and not deposit
            # for each ship, if the treasure on ship, find the distance from the ship to the base
            minimum_distance = float('inf')
            x_base, y_base = self.base[0], self.base[1]
            for ship, treasures_tuple in state_dict["treasures_on_ship"].items():
                treasure_list = [treasures_tuple[0], treasures_tuple[1]]
                if t_name in treasure_list:
                    ship_location = state_dict["pirate_ships"][ship]
                    x_ship, y_ship = ship_location[0], ship_location[1]
                    ship_distance = self.euclidian_distance(x_ship,y_ship ,x_base , y_base)
                    if ship_distance < minimum_distance:
                        minimum_distance = ship_distance
            # take the minimum distance
            if minimum_distance < float('inf'):
                sum_distances += minimum_distance
                continue
            minimum_distance = float('inf')

            if not up:
                adjacent_distance =self.euclidian_distance(x_t - 1 ,y_t ,x_base , y_base)
                if adjacent_distance < minimum_distance:
                    minimum_distance = adjacent_distance
            if not down:
                adjacent_distance = self.euclidian_distance(x_t + 1 ,y_t ,x_base , y_base)
                if adjacent_distance < minimum_distance:
                    minimum_distance = adjacent_distance
            if not left:
                adjacent_distance = self.euclidian_distance(x_t ,y_t - 1 ,x_base , y_base)
                if adjacent_distance < minimum_distance:
                    minimum_distance = adjacent_distance
            if not right:
                adjacent_distance = self.euclidian_distance(x_t  ,y_t + 1 ,x_base , y_base)
                if adjacent_distance < minimum_distance:
                    minimum_distance = adjacent_distance
            if minimum_distance < float('inf'):
                sum_distances += minimum_distance
                continue
        return sum_distances / len(self.pirate_ships)

    """Feel free to add your own functions
    (-2, -2, None) means there was a timeout"""

    def euclidian_distance(self , x_1, y_1 , x_2 , y_2):
        return pow(pow((x_1 - x_2),2) + pow((y_1 - y_2),2),0.5)

    def h_1(self,node):
        state = node.getstate()
        state_dict = self.frozenset_to_dict(state)
        #lets figure which treasures in base :
        base_treasures = list(state_dict["treasures_in_base"].keys())
        #[treasure_1 , treasure_2]
        #Lets figure which treasures are in
        parsed_list = list(state_dict["treasures_on_ship"].values())
        for i in parsed_list:
            #if there is no treasure on ship the tuple will be (,)
            if i[0] is None :
                continue
            elif i[0] not in base_treasures:
                base_treasures.append(i[0])
            if i[1] is None:
                continue
            elif i[1] not in base_treasures:
                base_treasures.append(i[1])
            #check if base hasn't this treasure
        return (len(self.treasures) - len(base_treasures))/ len(self.pirate_ships)

    def h_2(self,node):
        state = node.getstate()
        state_dict = self.frozenset_to_dict(state)
        sum_distances = 0
        # Board borders
        map = self.map
        right_border, left_border = len(map[0]) - 1, 0
        bottom_border, top_border = len(map) - 1, 0
        for t_name, t_location in state_dict["treasures"].items():
            # If treasure already deposit, the distance is zero
            if t_name in list(state_dict["treasures_in_base"].keys()):
                sum_distances += 0
                continue
            # If everywhere is islands, return infinty
            x_t, y_t = t_location[0], t_location[1]
            # False == sea,  True == Island or unreachable
            up, down, left, right = True, True, True, True
            #down
            if x_t < bottom_border and map[x_t + 1][y_t] != "I":
                down = False
            #up
            if x_t > top_border and map[x_t - 1][y_t] != "I":
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
            x_base, y_base = self.base[0], self.base[1]
            for ship, treasures_tuple in state_dict["treasures_on_ship"].items():
                treasure_list = [treasures_tuple[0] , treasures_tuple[1]]
                if t_name in treasure_list:
                    ship_location = state_dict["pirate_ships"][ship]
                    x_ship , y_ship = ship_location[0], ship_location[1]
                    ship_distance = abs(x_base - x_ship) + abs(y_base - y_ship)
                    if ship_distance < minimum_distance:
                        minimum_distance = ship_distance
            # take the minimum distance
            if minimum_distance < float('inf'):
                sum_distances += minimum_distance
                continue
            minimum_distance = float('inf')

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

    def h_try_out(self , node):
        state = node.getstate()
        state_dict = self.frozenset_to_dict(state)
        sum_distances = 0
        pirats_num = len(self.pirate_ships)
        # Board borders
        map = self.map
        right_border, left_border = len(map[0]) - 1, 0
        bottom_border, top_border = len(map) - 1, 0
        for t_name, t_location in state_dict["treasures"].items():
            # If treasure already deposit, the distance is zero
            if t_name in list(state_dict["treasures_in_base"].keys()):
                sum_distances += 0
                continue
            # If everywhere is islands, return infinty
            x_t, y_t = t_location[0], t_location[1]
            # False == sea,  True == Island or unreachable
            up, down, left, right = True, True, True, True
            # down
            if x_t < bottom_border and map[x_t + 1][y_t] != "I":
                down = False
            # up
            if x_t > top_border and map[x_t - 1][y_t] != "I":
                up = False
            # left
            if y_t > left_border and map[x_t][y_t - 1] != "I":
                left = False
            # right
            if y_t < right_border and map[x_t][y_t + 1] != "I":
                right = False
            # if no access at all, return infinity
            if up and down and left and right:
                sum_distances += float('inf')
                break
            # if treasure on ships and not deposit
            # for each ship, if the treasure on ship, find the distance from the ship to the base
            minimum_distance = float('inf')
            x_base, y_base = self.base[0], self.base[1]
            for ship, treasures_tuple in state_dict["treasures_on_ship"].items():
                treasure_list = [treasures_tuple[0], treasures_tuple[1]]
                if t_name in treasure_list:
                    ship_location = state_dict["pirate_ships"][ship]
                    x_ship, y_ship = ship_location[0], ship_location[1]
                    ship_distance = abs(x_base - x_ship) + abs(y_base - y_ship)
                    if ship_distance < minimum_distance:
                        minimum_distance = ship_distance
            # take the minimum distance
            if minimum_distance < float('inf'):
                sum_distances += minimum_distance
                continue
            minimum_distance = float('inf')

            if not up:
                adjacent_distance = abs(x_t - 1 - x_base) + abs(y_t - y_base)
                if adjacent_distance < minimum_distance:
                    minimum_distance =  adjacent_distance
            if not down:
                adjacent_distance = abs(x_t + 1 - x_base) + abs(y_t - y_base)
                if adjacent_distance < minimum_distance:
                    minimum_distance =  adjacent_distance
            if not left:
                adjacent_distance = abs(x_t - x_base) + abs(y_t - 1 - y_base)
                if adjacent_distance <  minimum_distance:
                    minimum_distance =  adjacent_distance
            if not right:
                adjacent_distance = abs(x_t - x_base) + abs(y_t + 1 - y_base)
                if adjacent_distance < minimum_distance:
                    minimum_distance =  adjacent_distance
            if minimum_distance < float('inf'):
                sum_distances += minimum_distance
                continue
        return  sum_distances

    def get_key(self ,val , my_dict):
        for key, value in my_dict.items():
            if val == value:
                return key

        return "key doesn't exist"

    def get_all_keys(self, val, my_dict):
        keys_list = []
        for key, value in my_dict.items():
            if val == value:
                keys_list.append(key)

        if keys_list:
            return len(keys_list) , keys_list
        else:
            return "No keys found for the given value"


    # def find_all_treasures_in_island(self, state_dict, keys, key):
    #     #treasures_in_location = self.get_all_keys((x, y), state_dict["treasures"])
    #     for treasure_name in keys:
    #         collect_treasures = ("collect_treasure", key, treasure_name)
    #         return collect_treasures


    def dict_to_frozenset(self, dict_of_dicts):
        dict_of_frozensets = {}
        for internal_dict_name, internal_dict in dict_of_dicts.items():
            if isinstance(internal_dict, dict):
                frozen_internal_dict = frozenset(internal_dict.items())
                dict_of_frozensets[internal_dict_name] = frozen_internal_dict
            else:
                dict_of_frozensets[internal_dict_name] = internal_dict

        frozenset_of_frozensets = frozenset(dict_of_frozensets.items())
        return frozenset_of_frozensets
    def check_capcity(self ,state ,key):
        if state["treasures_on_ship"][key][0] is None:
            return 0
        if state["treasures_on_ship"][key][1] is None:
            return 1
        else:return 2
    def frozenset_to_dict(self, frozenset_of_sets):
        dict_of_dicts = {}
        for frozen_set in frozenset_of_sets:
            #dict_from_tuple = {}
            frozen_to_tuple = tuple(frozen_set)
            outer_dict_name = frozen_to_tuple[0]
            dict_values = frozen_to_tuple[1]
            inner_dict = {}

            for value in dict_values:
                if isinstance(value, tuple):
                    inner_dict_name = value[0]
                    inner_dict_values = value[1]
                    inner_dict[inner_dict_name] = inner_dict_values
                else:
                    dict_of_dicts[outer_dict_name] = dict_values
            dict_of_dicts[outer_dict_name] = inner_dict
        return dict_of_dicts


def create_onepiece_problem(game):
    return OnePieceProblem(game)
