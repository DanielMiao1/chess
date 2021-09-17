"""
enums.py
Type Enumerations
"""


class Color:
	white, black = "white", "black"


class Piece:
	pawn, knight, bishop, rook = "pawn", "knight", "bishop", "rook"
	queen, king = "queen", "king"


class Move:
	def __init__(self, name, old_position, new_position, piece, is_capture=False):
		self.piece = piece
		self.name = name
		self.old_position, self.new_position = old_position, new_position
		self.is_capture = is_capture
