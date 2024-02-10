from typing import Dict, Any
import hashlib
import json

# def dict_hash(dictionary: Dict[str, Any]) -> str:
#     """MD5 hash of a dictionary."""
#     dhash = hashlib.md5()
#     # We need to sort arguments so {'a': 1, 'b': 2} is
#     # the same as {'b': 2, 'a': 1}
#     encoded = json.dumps(dictionary, sort_keys=True).encode()
#     dhash.update(encoded)
#     return dhash.hexdigest()
#
# dict_1 = {'a': 1, 'b': 2}
# dict_2 = {'b': 2, 'a': 1}
#
# print(dict_hash(dict_2))
# print(dict_hash(dict_1))
# #
# class MarineShip:
#
#     def __init__(self, path):
#         self.path = self.create_path(path)
#         self.turns_counter = 0
#         self.current_location = self.path[0]
#
#
#     def create_path(self, path):
#         reversed_path = self.path[::-1]
#         reversed_path = reversed_path[1:]
#         reversed_path = reversed_path[:-1]
#         real_path = self.path + reversed_path
#         return real_path
#
#     def move(self):
#         self.turns_counter += 1
#         self.current_location = self.path[self.turns_counter % len(self.path)]
#         return self.current_location
#
#
#
#
#
# class Board:
#
#     def __init__(self, map, treasures):
#         self.map = map
#         self.right_border = len(self.map[0]) - 1
#         self.left_border = 0
#         self.down_border = len(map) - 1
#         self.up_border = 0
#         self.squares = []
#
#         for i in range(0,len(map)):
#             row = []
#             for j in range(0,len(map[0])):
#                 #sea / tresure / island / base
#                 if map[i][j] == "I":
#                     location = (i,j)
#                     if location in treasures.values():
#                         new_square = Square(i,j,"T")
#                         row.append(new_square)
#                         continue
#                     else:
#                         new_square = Square(i,j,"I")
#                         row.append(new_square)
#                         continue
#                 if map[i][j] == "B":
#                     new_square = Square(i, j, "B")
#                     row.append(new_square)
#                     continue
#                 if map[i][j] == "S":
#                     new_square = Square(i,j,"S")
#                     row.append(new_square)
#                     continue
#             self.squares.append(row)
#
#
#
#
# class Base:
#     pass
#
# class Sea:
#     pass
# class Treasure:
#
#     def __init__(self):
#         self.is_picked = False
#
#     def is_collected(self):
#         if not self.is_picked:
#             self.is_picked = True
#             return "picked"
#         return "no treasure"
#
#
#  class square:
#
#      def __int__(self, i, j, kind):
#          self.location = (i, j)
#          if kind == "T":
#            self.kind = Treasure()
#            self.is_passable = False
#          if kind == "I":
#            self.kind = Island()
#            self.is_passable = False
#          if kind == "B":
#            self.kind == Base()
#            self.is_passable = True
#          if kind == "S":
#             self.kind = Sea()
#             self.is_passable = True

# class Pirate_Ship:
#
#     def __init__(self , location):
#         self.location = location
#         self.tresaures = []
#
#     def sail(self, direction ):
#         if direction == "right":
#             self.location = (self.location[0] , self.location[1] + 1)
#         if direction == "left":
#             self.location = (self.location[0], self.location[1] - 1)
#         if direction == "up":
#             self.location = (self.location[0] - 1, self.location[1])
#         if direction == "down":
#             self.location = (self.location[0] + 1, self.location[1])
#         return
#
#     def collect_tresaure(self , square):
#
