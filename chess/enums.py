# -*- coding: utf-8 -*-


"""
enums.py
Type Enumerations
"""

from . import functions


class Color:
	white, black = "white", "black"
	current, any = "current", "any"

	@staticmethod
	def all():
		return [Color.white, Color.black]

	@staticmethod
	def invert(color):
		if not Color.valid(color):
			raise errors.UndefinedColor(color)
		elif Color.isWhite(color):
			return "black"
		else:
			return "white"

	@staticmethod
	def valid(color):
		return color in Color.all()

	@staticmethod
	def isWhite(color):
		return color in [Color.white, "w"]

	@staticmethod
	def isBlack(color):
		return color in [Color.black, "b"]


class Piece:
	pawn, knight, bishop, rook = "pawn", "knight", "bishop", "rook"
	queen, king = "queen", "king"
	unicode_dictionary = {"whiteking": "♔", "blackking": "♚", "whitequeen": "♕", "blackqueen": "♛", "whiterook": "♖", "blackrook": "♜", "whitebishop": "♗", "blackbishop": "♝", "whiteknight": "♘", "blackknight": "♞", "whitepawn": "♙", "blackpawn": "♟"}
	piece_values = {"pawn": 1, "knight": 3, "bishop": 3, "rook": 5, "queen": 9, "king": float("inf")}
	piece_square_tables = {
		"middlegame": {
			"pawn": [[0, 0, 0, 0, 0, 0, 0, 0], [50, 50, 50, 50, 50, 50, 50, 50], [35, 35, 35, 35, 35, 35, 35, 35], [5, 5, 15, 14, 14, 15, 5, 5], [5, 5, 7, 12, 12, 7, 5, 5], [-4, -4, -4, -2, -2, -4, -4, -4], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
			"knight": [[-100, -70, -50, -50, -50, -50, -70, -100], [-70, -30, 0, 0, 0, 0, -30, -70], [-50, 10, 15, 16, 16, 15, 10, -50], [-30, 5, 8, 30, 30, 8, 5, -30], [-30, 4, 12, 15, 15, 12, 4, -30], [-50, 5, 15, 5, 5, 15, 5, -50], [-70, -50, -5, -2, -7, -5, -50, -70], [-100, -20, -50, -10, -10, -20, -20, -100]],
			"bishop": [[-20, 0, -2, -2, -2, -2, 0, -20], [-10, 0, 0, 0, 0, 0, 0, -10], [-6, 10, 8, 5, 5, 8, 10, -6], [-4, 15, 10, 9, 9, 10, 15, -4], [-2, 0, 20, 12, 12, 20, 0, -2], [-5, -5, 2, 15, 15, 2, -5, -5], [0, 30, -5, 5, 5, -5, 30, 0], [-50, -20, -10, -40, -40, -10, -20, -50]],
			"rook": [[10, 10, 10, 10, 10, 10, 10, 10], [25, 25, 25, 25, 25, 25, 25, 25], [5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5], [-5, -5, -5, -5, -5, -5, -5, -5], [-15, -15, -5, -15, -15, -15, -15, -15], [0, -5, 0, 10, 15, 10, -5, 0]],
			"queen": [[0, 30, 30, 40, 40, 30, 30, 0], [5, 20, 20, 25, 25, 20, 20, 5], [0, 20, 20, 25, 25, 20, 20, 0], [0, 20, 20, 20, 20, 20, 20, 6], [-2, 5, 5, 5, 5, 5, 5, -2], [-5, 0, 0, -5, -5, 6, 0, -5], [-10, -2, 0, 2, 2, 2, -2, -10], [-20, -19, -5, 5, 0, -5, -19, -20]],
			"king": [[-50, -50, -50, -50, -50, -50, -50, -50], [-50, -50, -50, -50, -50, -50, -50, -50], [-50, -50, -50, -50, -50, -50, -50, -50], [-50, -50, -50, -50, -50, -50, -50, -50], [-50, -50, -50, -50, -50, -50, -50, -50], [-50, -50, -50, -50, -50, -50, -50, -50], [-50, -50, -50, -45, -45, -50, -50, -50], [5, 7, 5, -10, 0, 0, 5, 7]]
		},
		"endgame": {
			"pawn": [[0, 0, 0, 0, 0, 0, 0, 0], [200, 200, 200, 200, 200, 200, 200, 200], [80, 80, 80, 80, 80, 80, 80, 80], [40, 30, 20, 10, 10, 20, 30, 40], [20, 10, 0, -2, -2, 0, 10, 20], [10, 10, 5, 0, 0, 5, 10, 10], [5, 5, 5, 5, 5, 5, 5, 5], [0, 0, 0, 0, 0, 0, 0, 0]],
			"knight": [[-100, -70, -50, -50, -50, -50, -70, -100], [-70, -30, 0, 0, 0, 0, -30, -70], [-50, 10, 15, 16, 16, 15, 10, -50], [-30, 5, 8, 30, 30, 8, 5, -30], [-30, 4, 12, 15, 15, 12, 4, -30], [-50, 5, 15, 5, 5, 15, 5, -50], [-70, -50, -5, -2, -7, -5, -50, -70], [-100, -150, -50, -10, -10, -20, -150, -100]],
			"bishop": [[-20, -10, -2, -2, -2, -2, -10, -20], [-10, 0, 0, 0, 0, 0, 0, -10], [-6, 10, 8, 5, 5, 8, 10, -6], [-4, 15, 10, 9, 9, 10, 15, -4], [-2, 0, 20, 12, 12, 20, 0, -2], [-5, -5, 2, 15, 15, 2, -5, -5], [0, 30, -5, 5, 5, -5, 30, 0], [-50, -20, -150, -40, -40, -150, -20, -50]],
			"rook": [[10, 10, 10, 10, 10, 10, 10, 10], [30, 30, 30, 30, 30, 25, 25, 25], [5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5], [-5, -5, -5, -5, -5, -5, -5, -5], [-15, -15, -5, -15, -15, -15, -15, -15], [0, -5, 0, 10, 15, 10, -5, 0]],
			"queen": [[20, 30, 30, 40, 40, 30, 30, 20], [5, 20, 20, 25, 25, 20, 20, 5], [0, 20, 20, 25, 25, 20, 20, 0], [0, 20, 20, 20, 20, 20, 20, 0], [5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, -150, 5, 5, 5, 5]],
			"king": [[-500, -250, -200, -200, -200, -200, -250, -500], [-250, 10, 10, 10, 10, 10, 10, -250], [-200, 10, 10, 10, 10, 10, 10, -200], [-200, 10, 10, 10, 10, 10, 10, -200], [-200, 10, 10, 10, 10, 10, 10, -200], [-200, 10, 10, 10, 10, 10, 10, -200], [-250, 0, 0, 0, 0, 0, 0, -250], [-500, -400, -350, -200, -200, -200, -400, -500]]
		}
	}

	@staticmethod
	def all():
		return [Piece.pawn, Piece.knight, Piece.bishop, Piece.rook, Piece.queen, Piece.king]

	@staticmethod
	def unicode(piece, color="white"):
		if not Piece.valid(piece):
			raise errors.UndefinedPiece(piece)
			return False
		if not Color.valid(color):
			raise errors.UndefinedColor(color)
			return False
		return Piece.unicode_dictionary[color + piece]

	@staticmethod
	def value(piece):
		try:
			piece = piece.piece_type
		except AttributeError:
			pass
		if Piece.valid(piece):
			return Piece.piece_values[piece]
		raise errors.UndefinedPiece(piece)

	@staticmethod
	def evaluate_piece_position(piece, position, color, game_phase):
		if not Phase.valid(game_phase):
			raise errors.UndefinedGamePhase(game_phase)
		if not Piece.valid(piece):
			raise errors.UndefinedPiece(piece)
		if not Color.valid(color):
			raise errors.UndefinedColor(color)
		if color == Color.white:
			return Piece.piece_square_tables["middlegame" if game_phase in [Phase.opening, Phase.middlegame] else "endgame"][piece][functions.coordinateToIndex(position)[0]][functions.coordinateToIndex(position)[1]]
		return list(reversed([list(reversed(i)) for i in Piece.piece_square_tables["middlegame" if game_phase in [Phase.opening, Phase.middlegame] else "endgame"][piece]]))[functions.coordinateToIndex(position)[0]][functions.coordinateToIndex(position)[1]]

	@staticmethod
	def valid(piece):
		return piece in Piece.all()


class Phase:
	opening, middlegame, endgame = "opening", "middlegame", "endgame"

	@staticmethod
	def all():
		return [Phase.opening, Phase.middlegame, Phase.endgame]

	@staticmethod
	def valid(phase):
		return phase in Phase.all()


class Castle:
	kingside, queenside = "kingside", "queenside"

	@staticmethod
	def all():
		return [Castle.kingside, Castle.queenside]

	@staticmethod
	def valid(castle):
		return castle in Castle.all()


class Stop:
	never, capture_piece, no_capture, piece = "never", "capture_piece", "no_capture", "piece"

	@staticmethod
	def all():
		return [Stop.never, Stop.capture_piece, Stop.no_capture, Stop.piece]

	@staticmethod
	def valid(stop):
		return stop in Stop.all()


class Move:
	def __init__(self, name, old_position, new_position, piece, is_capture=False, check=False, castle=None, castle_rook=None, double_pawn_move=False, en_passant=False, en_passant_position=None):
		self.piece = piece
		self.name = name
		self.old_position, self.new_position = old_position, new_position
		self.is_capture = is_capture
		self.check = check
		self.castle = castle
		self.castle_rook = castle_rook
		self.double_pawn_move = double_pawn_move
		self.en_passant = en_passant
		self.en_passant_position = en_passant_position
		if is_capture and piece is not None:
			self.captured_piece = self.piece.board.pieceAt(new_position)
		else:
			self.captured_piece = None

	def visualized(self, print_result=False, empty_squares=" ", separators=True, old_position_symbol="□", new_position_symbol="■", capture_symbol="X"):
		if empty_squares == "":
			empty_squares = " "
		empty_squares = empty_squares[0]
		squares = []
		for x in range(8):
			row = []
			for y in range(8):
				row.append(old_position_symbol if functions.coordinateToIndex(self.old_position) == [x, y] else capture_symbol if functions.coordinateToIndex(self.new_position) == [x, y] and self.is_capture else new_position_symbol if functions.coordinateToIndex(self.new_position) == [x, y] else empty_squares)
			squares.append(row)
		if print_result:
			print(("---------------------------------\n" if separators else "") + ("\n---------------------------------\n" if separators else "\n").join([("| " if separators else "") + (" | " if separators else " ").join(i) + (" |" if separators else "") for i in squares]) + ("\n---------------------------------" if separators else ""))
			return
		return ("---------------------------------\n" if separators else "") + ("\n---------------------------------\n" if separators else "\n").join([("| " if separators else "") + (" | " if separators else " ").join(i) + (" |" if separators else "") for i in squares]) + ("\n---------------------------------" if separators else "")

	__str__ = __repr__ = lambda self: str(self.name)


class MoveSet:
	def __init__(self, *moves):
		if len(moves) == 1 and isinstance(moves[0], (list, set, tuple)):
			self.moves = [i for i in list(moves[0]) if isinstance(i, Move)]
		else:
			self.moves = [i for i in moves if isinstance(i, Move)]

	def visualized(self, print_result=False, empty_squares=" ", separators=True, old_position_symbol="□", new_position_symbol="■", capture_symbol="X"):
		if empty_squares == "":
			empty_squares = " "
		empty_squares = empty_squares[0]
		squares = []
		for x in range(8):
			row = []
			for y in range(8):
				row.append(old_position_symbol if [x, y] in map(functions.coordinateToIndex, self.old_positions()) else capture_symbol if [x, y] in [i.new_position for i in self.moves if i.is_capture] else new_position_symbol if [x, y] in map(functions.coordinateToIndex, self.new_positions()) else empty_squares)
			squares.append(row)
		if print_result:
			print(("---------------------------------\n" if separators else "") + ("\n---------------------------------\n" if separators else "\n").join([("| " if separators else "") + (" | " if separators else " ").join(i) + (" |" if separators else "") for i in squares]) + ("\n---------------------------------" if separators else ""))
			return
		return ("---------------------------------\n" if separators else "") + ("\n---------------------------------\n" if separators else "\n").join([("| " if separators else "") + (" | " if separators else " ").join(i) + (" |" if separators else "") for i in squares]) + ("\n---------------------------------" if separators else "")

	def old_positions(self):
		return [i.old_position for i in self.moves]

	def new_positions(self):
		return [i.new_position for i in self.moves]

	def __contains__(self, obj):
		if isinstance(obj, Move):
			return obj in self.moves
		return False

	def __add__(self, other):
		if isinstance(other, MoveSet):
			return MoveSet(self.moves + other.moves)
		if isinstance(other, Move):
			return MoveSet(self.moves + [other])
		if isinstance(other, (list, set, tuple)):
			new_set = MoveSet(self.moves)
			for i in other:
				new_set += i
			return new_set
		return self

	def __radd__(self, other):
		return self.__add__(other)

	def __iadd__(self, other):
		return self.__add__(other)

	def __sub__(self, other):
		if isinstance(other, MoveSet):
			new_set = MoveSet(self.moves)
			for i in other.moves:
				if i in self.moves:
					new_set.moves.remove(i)
			return new_set
		if isinstance(other, Move):
			return MoveSet([i for i in self.moves if i != other])
		if isinstance(other, (list, set, tuple)):
			new_set = MoveSet(self.moves)
			for i in other:
				new_set -= i
			return new_set
		return self

	def __rsub__(self, other):
		return self.__sub__(other)

	def __isub__(self, other):
		return self.__sub__(other)

	def __neg__(self):
		new_set = MoveSet(self.moves)
		for i in new_set:
			i.new_position, i.old_position = i.old_position, i.new_position
		return new_set

	def __pos__(self):
		return MoveSet(self.moves)

	def __len__(self):
		return len(self.moves)

	def __iter__(self):
		self.iter_position = 0
		return self

	def __next__(self):
		if self.iter_position < len(self.moves):
			self.iter_position += 1
			return self.moves[self.iter_position - 1]
		else:
			raise StopIteration

	def next(self):
		if self.iter_position < len(self.moves):
			self.iter_position += 1
			return self.moves[self.iter_position - 1]
		else:
			raise StopIteration

	__str__ = __repr__ = lambda self: ", ".join(map(str, self.moves))
