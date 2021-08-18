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
	
	def __str__(self) -> str:
		return self.color.title() + " square from game " + self.board
	
	def __repr__(self) -> str:
		return self.color.title() + " square from game " + self.board
	
	def __lt__(self, other) -> bool:
		raise ArithmeticError("Cannot compare squares")
	
	def __add__(self, _):
		raise ArithmeticError("Cannot add pieces")
	
	def __sub__(self, _):
		raise ArithmeticError("Cannot subtract pieces")
	
	def __mul__(self, _):
		raise ArithmeticError("Cannot multiply pieces")
	
	def __mod__(self, _):
		raise ArithmeticError("Cannot modulo pieces")
	
	def __floordiv__(self, _):
		raise ArithmeticError("Cannot divide pieces")
	
	def __divmod__(self, _):
		raise ArithmeticError("Cannot divide pieces")
	
	def __truediv__(self, _):
		raise ArithmeticError("Cannot divide pieces")
	
	def __floor__(self):
		raise ArithmeticError("Cannot floor")
	
	def __eq__(self, other):
		raise ArithmeticError("Cannot compare squares")


class Piece:
	def __init__(self, position: list or tuple, piece_type: enums.Piece, color: enums.Color, board):
		self.position, self.piece_type, self.color, self.board = position, piece_type, color, board
	
	def __str__(self) -> str:
		return self.color.title() + self.piece_type[0] + " from game " + {self.board}
	
	def __repr__(self) -> str:
		return self.color.title() + self.piece_type[0] + " from game " + {self.board}
	
	def __lt__(self, other) -> bool:
		return self.piece_type[1] < other.piece_type[1]
	
	def __add__(self, _):
		raise ArithmeticError("Cannot add pieces")
	
	def __sub__(self, _):
		raise ArithmeticError("Cannot subtract pieces")
	
	def __mul__(self, _):
		raise ArithmeticError("Cannot multiply pieces")
	
	def __mod__(self, _):
		raise ArithmeticError("Cannot modulo pieces")
	
	def __floordiv__(self, _):
		raise ArithmeticError("Cannot divide pieces")
	
	def __divmod__(self, _):
		raise ArithmeticError("Cannot divide pieces")
	
	def __truediv__(self, _):
		raise ArithmeticError("Cannot divide pieces")
	
	def __floor__(self):
		raise ArithmeticError("Cannot floor")
	
	def __eq__(self, other):
		return self.piece_type[1] == other.piece_type[1]


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
				Piece([0, 0], enums.Piece.rook, enums.Color.black, self),
				Piece([0, 1], enums.Piece.knight, enums.Color.black, self),
				Piece([0, 2], enums.Piece.bishop, enums.Color.black, self),
				Piece([0, 3], enums.Piece.queen, enums.Color.black, self),
				Piece([0, 4], enums.Piece.king, enums.Color.black, self),
				Piece([0, 5], enums.Piece.bishop, enums.Color.black, self),
				Piece([0, 6], enums.Piece.knight, enums.Color.black, self),
				Piece([0, 7], enums.Piece.rook, enums.Color.black, self)
			],
			[
				Piece([1, 0], enums.Piece.pawn, enums.Color.black, self),
				Piece([1, 1], enums.Piece.pawn, enums.Color.black, self),
				Piece([1, 2], enums.Piece.pawn, enums.Color.black, self),
				Piece([1, 3], enums.Piece.pawn, enums.Color.black, self),
				Piece([1, 4], enums.Piece.pawn, enums.Color.black, self),
				Piece([1, 5], enums.Piece.pawn, enums.Color.black, self),
				Piece([1, 6], enums.Piece.pawn, enums.Color.black, self),
				Piece([1, 7], enums.Piece.pawn, enums.Color.black, self)
			],
			[
				Piece([6, 0], enums.Piece.pawn, enums.Color.white, self),
				Piece([6, 1], enums.Piece.pawn, enums.Color.white, self),
				Piece([6, 2], enums.Piece.pawn, enums.Color.white, self),
				Piece([6, 3], enums.Piece.pawn, enums.Color.white, self),
				Piece([6, 4], enums.Piece.pawn, enums.Color.white, self),
				Piece([6, 5], enums.Piece.pawn, enums.Color.white, self),
				Piece([6, 6], enums.Piece.pawn, enums.Color.white, self),
				Piece([6, 7], enums.Piece.pawn, enums.Color.white, self)
			],
			[
				Piece([7, 0], enums.Piece.rook, enums.Color.white, self),
				Piece([7, 1], enums.Piece.knight, enums.Color.white, self),
				Piece([7, 2], enums.Piece.bishop, enums.Color.white, self),
				Piece([7, 3], enums.Piece.queen, enums.Color.white, self),
				Piece([7, 4], enums.Piece.king, enums.Color.white, self),
				Piece([7, 5], enums.Piece.bishop, enums.Color.white, self),
				Piece([7, 6], enums.Piece.knight, enums.Color.white, self),
				Piece([7, 7], enums.Piece.rook, enums.Color.white, self)
			]
		]
	
	def getFEN(self) -> str:
		return "(FEN)"
	
	def __str__(self) -> str:
		return "Chess Game with FEN " + self.getFEN()
	
	def __repr__(self) -> str:
		return "Chess Game with FEN " + self.getFEN()
	
	def __lt__(self, other) -> bool:
		return len(self.pieces) < len(other.pieces)
	
	def __add__(self, _):
		raise ArithmeticError("Cannot add games")
	
	def __sub__(self, _):
		raise ArithmeticError("Cannot subtract games")
	
	def __mul__(self, _):
		raise ArithmeticError("Cannot multiply games")
	
	def __mod__(self, _):
		raise ArithmeticError("Cannot modulo games")
	
	def __floordiv__(self, _):
		raise ArithmeticError("Cannot divide games")
	
	def __divmod__(self, _):
		raise ArithmeticError("Cannot divide games")
	
	def __truediv__(self, _):
		raise ArithmeticError("Cannot divide games")
	
	def __floor__(self):
		raise ArithmeticError("Cannot floor")
	
	def __eq__(self, other):
		return self.getFEN() == other.getFEN()
	