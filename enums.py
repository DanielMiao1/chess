"""
enums.py
Type Enumerations
"""


class Color:
	white, black = "white", "black"


class Piece:
	pawn, knight, bishop, rook = ["pawn", 1], ["knight", 3], ["bishop", 3], ["rook", 5]
	queen, king = ["queen", 9], ["king", float("inf")]


class Move:
	def __init__(self, name, old_position, new_position, is_capture=False):
		self.name = name
		self.old_position, self.new_position = old_position, new_position
		self.is_capture = is_capture
