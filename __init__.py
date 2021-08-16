"""
__init__.py
Main Python 3 File
"""
from . import enums


class Square:
	def __init__(self, position: list or tuple) -> None:
		self.position = position
		if ((position[0] + position[1]) & 1) == 0:
			self.color = enums.Square.dark
		else:
			self.color = enums.Square.light


class Piece:
	def __init__(self, position: list or tuple, piece_type: enums.Piece, color: enums.Color):
		self.position, self.piece_type, self.color = position, piece_type, color


class Game:
	def __init__(self):
		self.turn = enums.Color.white
		self.squares = [
			[
				Square([0, 0]), Square([0, 1]), Square([0, 2]), Square([0, 3]), Square([0, 4]), Square([0, 5]), Square([0, 6]),
				Square([0, 7])
			],
			[
				Square([1, 0]), Square([1, 1]), Square([1, 2]), Square([1, 3]), Square([1, 4]), Square([1, 5]), Square([1, 6]),
				Square([0, 7])
			],
			[
				Square([2, 0]), Square([2, 1]), Square([2, 2]), Square([2, 3]), Square([2, 4]), Square([2, 5]), Square([2, 6]),
				Square([2, 7])
			],
			[
				Square([3, 0]), Square([3, 1]), Square([3, 2]), Square([3, 3]), Square([3, 4]), Square([3, 5]), Square([3, 6]),
				Square([3, 7])
			],
			[
				Square([4, 0]), Square([4, 1]), Square([4, 2]), Square([4, 3]), Square([4, 4]), Square([4, 5]), Square([4, 6]),
				Square([4, 7])
			],
			[
				Square([5, 0]), Square([5, 1]), Square([5, 2]), Square([5, 3]), Square([5, 4]), Square([5, 5]), Square([5, 6]),
				Square([5, 7])
			],
			[
				Square([6, 0]), Square([6, 1]), Square([6, 2]), Square([6, 3]), Square([6, 4]), Square([6, 5]), Square([6, 6]),
				Square([6, 7])
			],
			[
				Square([7, 0]), Square([7, 1]), Square([7, 2]), Square([7, 3]), Square([7, 4]), Square([7, 5]), Square([7, 6]),
				Square([7, 7])
			],
		]
		self.pieces = [
			[
				Piece([0, 0], enums.Piece.rook, enums.Color.black), Piece([0, 1], enums.Piece.knight, enums.Color.black),
				Piece([0, 2], enums.Piece.bishop, enums.Color.black), Piece([0, 3], enums.Piece.queen, enums.Color.black),
				Piece([0, 4], enums.Piece.king, enums.Color.black), Piece([0, 5], enums.Piece.bishop, enums.Color.black),
				Piece([0, 6], enums.Piece.knight, enums.Color.black), Piece([0, 7], enums.Piece.rook, enums.Color.black)
			],
			[
				Piece([1, 0], enums.Piece.pawn, enums.Color.black), Piece([1, 1], enums.Piece.pawn, enums.Color.black),
				Piece([1, 2], enums.Piece.pawn, enums.Color.black), Piece([1, 3], enums.Piece.pawn, enums.Color.black),
				Piece([1, 4], enums.Piece.pawn, enums.Color.black), Piece([1, 5], enums.Piece.pawn, enums.Color.black),
				Piece([1, 6], enums.Piece.pawn, enums.Color.black), Piece([1, 7], enums.Piece.pawn, enums.Color.black)
			],
			[
				Piece([6, 0], enums.Piece.pawn, enums.Color.white), Piece([6, 1], enums.Piece.pawn, enums.Color.white),
				Piece([6, 2], enums.Piece.pawn, enums.Color.white), Piece([6, 3], enums.Piece.pawn, enums.Color.white),
				Piece([6, 4], enums.Piece.pawn, enums.Color.white), Piece([6, 5], enums.Piece.pawn, enums.Color.white),
				Piece([6, 6], enums.Piece.pawn, enums.Color.white), Piece([6, 7], enums.Piece.pawn, enums.Color.white)
			],
			[
				Piece([7, 0], enums.Piece.rook, enums.Color.white), Piece([7, 1], enums.Piece.knight, enums.Color.white),
				Piece([7, 2], enums.Piece.bishop, enums.Color.white), Piece([7, 3], enums.Piece.queen, enums.Color.white),
				Piece([7, 4], enums.Piece.king, enums.Color.white), Piece([7, 5], enums.Piece.bishop, enums.Color.white),
				Piece([7, 6], enums.Piece.knight, enums.Color.white), Piece([7, 7], enums.Piece.rook, enums.Color.white)
			]
		]
