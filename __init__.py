"""
__init__.py
Main Python 3 File
"""

from . import enums
from . import errors


class Square:
	def __init__(self, position, board):
		self.position = position
		self.board = board
		if ((position[0] + position[1]) & 1) == 0:
			self.color = enums.Square.dark
		else:
			self.color = enums.Square.light
	
	def __str__(self):
		return self.color.title() + " square from " + str(self.board)
	
	def __repr__(self):
		return self.color.title() + " square from " + str(self.board)
	
	def __lt__(self, other):
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
	def __init__(self, position, piece_type, color, board):
		self.position, self.piece_type, self.color, self.board = position, piece_type, color, board
	
	def moves(self):
		return []

	def __str__(self):
		return self.color.title() + " " + self.piece_type[0] + " from " + str(self.board)
	
	def __repr__(self):
		return self.color.title() + " " + self.piece_type[0] + " from " + str(self.board)
	
	def __lt__(self, other):
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
	def __init__(self, raise_errors = True):
		self.turn = enums.Color.white
		self.squares, self.pieces = [], []
		for x in range(8):
			row = []
			for y in range(8):
				row.append(Square([x, y], self))
				if x in [0, 7]:
					if y in [0, 7]:
						self.pieces.append(Piece([x, y], enums.Piece.pawn, enums.Color.black if x == 0 else enums.Color.white, self))
					elif y in [1, 6]:
						self.pieces.append(Piece([x, y], enums.Piece.knight, enums.Color.black if x == 0 else enums.Color.white, self))
					elif y in [1, 6]:
						self.pieces.append(Piece([x, y], enums.Piece.bishop, enums.Color.black if x == 0 else enums.Color.white, self))
					elif y == 3:
						self.pieces.append(Piece([x, y], enums.Piece.queen, enums.Color.black if x == 0 else enums.Color.white, self))
					elif y == 3:
						self.pieces.append(Piece([x, y], enums.Piece.king, enums.Color.black if x == 0 else enums.Color.white, self))
				elif x in [1, 6]:
					self.pieces.append(Piece([x, y], enums.Piece.pawn, enums.Color.black if x == 1 else enums.Color.white, self))
			self.squares.append(row)
		self.raise_errors = raise_errors
	
	def FEN(self):
		return "(FEN TEXT)"
	
	def move(self, move):
		if move not in self.moves():
			if self.raise_errors:
				raise errors.MoveNotPossible(str(move))
			return False
	
	def moves(self):
		return [i.moves() for i in self.pieces]
	
	def __str__(self):
		return "Chess Game with FEN " + self.FEN()
	
	def __repr__(self):
		return "Chess Game with FEN " + self.FEN()
	
	def __lt__(self, other):
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
		return self.FEN() == other.FEN()
	