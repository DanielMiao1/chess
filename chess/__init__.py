# -*- coding: utf-8 -*-

import chess.errors
import chess.openings
import chess.functions

try:
	unicode
except NameError:
	unicode = str


class Color:
	white, black = "white", "black"
	current, any = "current", "any"

	@staticmethod
	def all():
		"""
		:return: Iterable[str]
		"""
		return Color.white, Color.black

	@staticmethod
	def invert(color):
		"""
		:type color: Any
		:return: str
		"""
		if not Color.valid(color):
			raise errors.UndefinedColor(color)
		elif Color.isWhite(color):
			return "black"
		else:
			return "white"

	@staticmethod
	def valid(color):
		"""
		:type color: Any
		:return: bool
		"""
		return color in Color.all()

	@staticmethod
	def isWhite(color):
		"""
		:type color: Any
		:return: bool
		"""
		return color in [Color.white, "w"]

	@staticmethod
	def isBlack(color):
		"""
		:type color: Any
		:return: bool
		"""
		return color in [Color.black, "b"]


class PieceEnum:
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
		"""
		:return: Iterable[str]
		"""
		return PieceEnum.pawn, PieceEnum.knight, PieceEnum.bishop, PieceEnum.rook, PieceEnum.queen, PieceEnum.king

	@staticmethod
	def unicode(piece, color="white"):
		"""
		:type piece: str
		:type color: str
		:return: str
		"""
		if not PieceEnum.valid(piece):
			raise errors.UndefinedPiece(piece)
		if not Color.valid(color):
			raise errors.UndefinedColor(color)
		return PieceEnum.unicode_dictionary[color + piece]

	@staticmethod
	def value(piece):
		"""
		:type piece: Piece | str
		:return: int | float
		"""
		try:
			piece = piece.piece_type
		except AttributeError:
			pass
		if PieceEnum.valid(piece):
			return PieceEnum.piece_values[piece]
		raise errors.UndefinedPiece(piece)

	@staticmethod
	def evaluate_piece_position(piece, position, color, game_phase):
		"""
		:type piece: str
		:type position: str
		:type color: str
		:type game_phase: str
		:return: int
		"""
		if not Phase.valid(game_phase):
			raise errors.UndefinedGamePhase(game_phase)
		if not PieceEnum.valid(piece):
			raise errors.UndefinedPiece(piece)
		if not Color.valid(color):
			raise errors.UndefinedColor(color)
		if color == Color.white:
			if game_phase in [Phase.opening, Phase.middlegame]:
				return PieceEnum.piece_square_tables["middlegame"][piece][functions.coordinateToIndex(position)[0]][functions.coordinateToIndex(position)[1]]
			return PieceEnum.piece_square_tables["endgame"][piece][functions.coordinateToIndex(position)[0]][functions.coordinateToIndex(position)[1]]
		if game_phase in [Phase.opening, Phase.middlegame]:
			return list(reversed([list(reversed(i)) for i in PieceEnum.piece_square_tables["middlegame"][piece]]))[functions.coordinateToIndex(position)[0]][functions.coordinateToIndex(position)[1]]
		return list(reversed([list(reversed(i)) for i in PieceEnum.piece_square_tables["endgame"][piece]]))[functions.coordinateToIndex(position)[0]][functions.coordinateToIndex(position)[1]]

	@staticmethod
	def valid(piece):
		"""
		:type piece: Any
		:return: bool
		"""
		return piece in PieceEnum.all()


class Phase:
	opening, middlegame, endgame = "opening", "middlegame", "endgame"

	@staticmethod
	def all():
		"""
		:return: Iterable[str]
		"""
		return Phase.opening, Phase.middlegame, Phase.endgame

	@staticmethod
	def valid(phase):
		"""
		:type phase: Any
		:return: bool
		"""
		return phase in Phase.all()


class Castle:
	kingside, queenside = "kingside", "queenside"

	@staticmethod
	def all():
		"""
		:return: Iterable[str]
		"""
		return Castle.kingside, Castle.queenside

	@staticmethod
	def valid(castle):
		"""
		:type castle: Any
		:return: bool
		"""
		return castle in Castle.all()


class Stop:
	never, capture_piece, no_capture, piece = "never", "capture_piece", "no_capture", "piece"

	@staticmethod
	def all():
		"""
		:return: Iterable[str]
		"""
		return Stop.never, Stop.capture_piece, Stop.no_capture, Stop.piece

	@staticmethod
	def valid(stop):
		"""
		:type stop: Any
		:return: bool
		"""
		return stop in Stop.all()


class Move:
	def __init__(self, name, old_position, new_position, piece, is_capture=False, check=False, castle=None, castle_rook=None, double_pawn_move=False, en_passant=False, en_passant_position=None, promotion=False):
		"""
		:type name: str
		:type old_position: str
		:type new_position: str
		:type piece: Piece | None
		:type is_capture: bool
		:type check: bool
		:type castle: str | None
		:type castle_rook: Piece | None
		:type double_pawn_move: bool
		:type en_passant: bool
		:type en_passant_position: str | None
		:type promotion: bool | str
		:return: None
		"""
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
		self.promotion = promotion
		if is_capture and piece is not None:
			self.captured_piece = self.piece.board.pieceAt(new_position)
		else:
			self.captured_piece = None

	def visualized(self, print_result=False, empty_squares=" ", separators=True, old_position_symbol="□", new_position_symbol="■", capture_symbol="X"):
		"""
		Returns or prints a string representation of the move
		:type print_result: bool
		:type empty_squares: str
		:type separators: bool
		:type old_position_symbol: str
		:type new_position_symbol: str
		:type capture_symbol: str
		:return: str | None
		"""
		if empty_squares == "":
			empty_squares = " "
		empty_squares = empty_squares[0]
		string = ""
		for x in range(8):
			string += "\n"
			if separators:
				string += "---------------------------------\n"
			for y in range(8):
				if functions.coordinateToIndex(self.old_position) == [x, y]:
					if separators:
						string += "| " + old_position_symbol + " "
					else:
						string += old_position_symbol + " "
				elif functions.coordinateToIndex(self.new_position) == [x, y] and self.is_capture:
					if separators:
						string += "| " + capture_symbol + " "
					else:
						string += capture_symbol + " "
				elif functions.coordinateToIndex(self.new_position) == [x, y]:
					if separators:
						string += "| " + new_position_symbol + " "
					else:
						string += new_position_symbol + " "
				else:
					if separators:
						string += "| " + empty_squares + " "
					else:
						string += empty_squares + " "
			if separators:
				string += "|"
		if separators:
			string += "\n---------------------------------"
		if print_result:
			print(string)
		else:
			return string

	def __str__(self, *args, **kwargs):
		"""
		:type args: Any
		:type kwargs: Any
		:return: str
		"""
		return str(self.name)

	def __repr__(self, *args, **kwargs):
		"""
		:type args: Any
		:type kwargs: Any
		:return: str
		"""
		return str(self.name)


class MoveSet:
	def __init__(self, *moves):
		"""
		:type moves: *Iterable[Move]
		:return: None
		"""
		if len(moves) == 1 and isinstance(moves[0], (list, set, tuple)):
			self.moves = []
			for i in list(moves[0]):
				if isinstance(i, Move):
					self.moves.append(i)
		else:
			self.moves = []
			for i in moves:
				if isinstance(i, Move):
					self.moves.append(i)

	def visualized(self, print_result=False, empty_squares=" ", separators=True, old_position_symbol="□", new_position_symbol="■", capture_symbol="X"):
		"""
		Returns or prints a string representation of the moves
		:type print_result: bool
		:type empty_squares: str
		:type separators: bool
		:type old_position_symbol: str
		:type new_position_symbol: str
		:type capture_symbol: str
		:return: str | None
		"""
		if empty_squares == "":
			empty_squares = " "
		empty_squares = empty_squares[0]
		string = ""
		for x in range(8):
			string += "\n"
			if separators:
				string += "---------------------------------\n"
			for y in range(8):
				if separators:
					character = "| " + empty_squares + " "
				else:
					character = empty_squares + " "
				for z in self.moves:
					if functions.coordinateToIndex(z.old_position) == [x, y]:
						if separators:
							character = "| " + old_position_symbol + " "
						else:
							character = old_position_symbol + " "
					elif functions.coordinateToIndex(z.new_position) == [x, y] and z.is_capture:
						if separators:
							character = "| " + capture_symbol + " "
						else:
							character = capture_symbol + " "
					elif functions.coordinateToIndex(z.new_position) == [x, y]:
						if separators:
							character = "| " + new_position_symbol + " "
						else:
							character = new_position_symbol + " "
				string += character
			if separators:
				string += "|"
		if separators:
			string += "\n---------------------------------"
		if print_result:
			print(string)
		else:
			return string

	def old_positions(self):
		"""
		:return: List[str]
		"""
		positions = []
		for i in self.moves:
			positions.append(i.old_position)
		return positions

	def new_positions(self):
		"""
		:return: List[str]
		"""
		positions = []
		for i in self.moves:
			positions.append(i.new_position)
		return positions

	def __contains__(self, obj):
		"""
		:type obj: Any
		:return: bool
		"""
		if isinstance(obj, Move):
			return obj in self.moves
		return False

	def __add__(self, other):
		"""
		:type other: Any
		:return: MoveSet
		"""
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
		"""
		:type other: Any
		:return: MoveSet
		"""
		return self.__add__(other)

	def __iadd__(self, other):
		"""
		:type other: Any
		:return: MoveSet
		"""
		return self.__add__(other)

	def __sub__(self, other):
		"""
		:type other: Any
		:return: MoveSet
		"""
		if isinstance(other, MoveSet):
			new_set = MoveSet(self.moves)
			for i in other.moves:
				if i in self.moves:
					new_set.moves.remove(i)
			return new_set
		if isinstance(other, Move):
			moves = []
			for i in self.moves:
				if i != other:
					moves.append(i)
			return MoveSet(moves)
		if isinstance(other, (list, set, tuple)):
			new_set = MoveSet(self.moves)
			for i in other:
				new_set -= i
			return new_set
		return self

	def __rsub__(self, other):
		"""
		:type other: Any
		:return: MoveSet
		"""
		return self.__sub__(other)

	def __isub__(self, other):
		"""
		:type other: Any
		:return: MoveSet
		"""
		return self.__sub__(other)

	def __neg__(self):
		"""
		:return: MoveSet
		"""
		new_set = MoveSet(self.moves)
		for i in new_set:
			i.new_position, i.old_position = i.old_position, i.new_position
		return new_set

	def __pos__(self):
		"""
		:return: MoveSet
		"""
		return MoveSet(self.moves)

	def __len__(self):
		"""
		:return: int
		"""
		return len(self.moves)

	def __iter__(self):
		"""
		:return: Move
		"""
		self.iter_position = 0
		return self

	def __next__(self):
		"""
		:return: Move
		"""
		if self.iter_position < len(self.moves):
			self.iter_position += 1
			return self.moves[self.iter_position - 1]
		else:
			raise StopIteration

	def next(self):
		"""
		:return: Move
		"""
		if self.iter_position < len(self.moves):
			self.iter_position += 1
			return self.moves[self.iter_position - 1]
		else:
			raise StopIteration

	__str__ = __repr__ = lambda self: ", ".join(map(str, self.moves))


class Line:
	def __init__(self, start, end, jump=False):
		"""
		Initialize the line
		:type start: str
		:type end: str
		:type jump: bool
		:return: None
		"""
		self.start_position = start
		self.end_position = end
		if not jump:
			if start[0] == end[0]:
				self.positions = []
				for i in range(int(start[1]) + 1, int(end[1])):
					self.positions.append(start[0] + str(i))
			elif start[1] == end[1]:
				self.positions = []
				for i in range({"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}[start[0]] + 1, {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}[end[0]]):
					self.positions.append(("a", "b", "c", "d", "e", "f", "g", "h")[i] + start[1])
			elif int(functions.coordinateToIndex(start)[1]) < int(functions.coordinateToIndex(end)[1]) and int(functions.coordinateToIndex(start)[0]) < int(functions.coordinateToIndex(end)[0]):
				pos1, pos2 = functions.coordinateToIndex(end)
				pos1, pos2 = pos1 - 1, pos2 - 1
				self.positions = []
				while [pos1, pos2] != functions.coordinateToIndex(start):
					if pos1 < 0 or 0 > pos2:
						raise errors.InvalidLineCoordinates(start, end)
					self.positions.append(functions.indexToCoordinate([pos1, pos2]))
					pos1, pos2 = pos1 - 1, pos2 - 1
			elif int(functions.coordinateToIndex(start)[1]) > int(functions.coordinateToIndex(end)[1]) and int(functions.coordinateToIndex(start)[0]) > int(functions.coordinateToIndex(end)[0]):
				pos1, pos2 = functions.coordinateToIndex(end)
				pos1, pos2 = pos1 + 1, pos2 + 1
				self.positions = []
				while [pos1, pos2] != functions.coordinateToIndex(start):
					if pos1 >= 8 or 8 <= pos2:
						raise errors.InvalidLineCoordinates(start, end)
					self.positions.append(functions.indexToCoordinate([pos1, pos2]))
					pos1, pos2 = pos1 + 1, pos2 + 1
			elif int(functions.coordinateToIndex(start)[1]) < int(functions.coordinateToIndex(end)[1]) and int(functions.coordinateToIndex(start)[0]) > int(functions.coordinateToIndex(end)[0]):
				pos1, pos2 = functions.coordinateToIndex(end)
				pos1, pos2 = pos1 + 1, pos2 - 1
				self.positions = []
				while [pos1, pos2] != functions.coordinateToIndex(start):
					if pos1 >= 8 or 0 > pos2:
						raise errors.InvalidLineCoordinates(start, end)
					self.positions.append(functions.indexToCoordinate([pos1, pos2]))
					pos1, pos2 = pos1 + 1, pos2 - 1
			elif int(functions.coordinateToIndex(start)[1]) > int(functions.coordinateToIndex(end)[1]) and int(functions.coordinateToIndex(start)[0]) < int(functions.coordinateToIndex(end)[0]):
				pos1, pos2 = functions.coordinateToIndex(end)
				pos1, pos2 = pos1 - 1, pos2 + 1
				self.positions = []
				while [pos1, pos2] != functions.coordinateToIndex(start):
					if pos1 < 0 or 8 <= pos2:
						raise errors.InvalidLineCoordinates(start, end)
					self.positions.append(functions.indexToCoordinate([pos1, pos2]))
					pos1, pos2 = pos1 - 1, pos2 + 1
			else:
				raise errors.InvalidLineCoordinates(start, end)
		else:
			self.positions = []

	def visualized(self, print_result=False, separators=True, empty_squares=" ", line_symbol="●", start_position_symbol="○", end_position_symbol="◎"):
		"""
		Returns or prints a string representation of the line
		:type print_result: bool
		:type separators: bool
		:type empty_squares: str
		:type line_symbol: str
		:type start_position_symbol: str
		:type end_position_symbol: str
		:return: str | None
		"""
		if empty_squares == "":
			empty_squares = " "
		empty_squares = empty_squares[0]
		string = ""
		for x in range(8):
			string += "\n"
			if separators:
				string += "---------------------------------\n"
			for y in range(8):
				if functions.coordinateToIndex(self.start_position) == [x, y]:
					if separators:
						string += "| " + start_position_symbol + " "
					else:
						string += start_position_symbol + " "
				elif functions.coordinateToIndex(self.end_position) == [x, y]:
					if separators:
						string += "| " + end_position_symbol + " "
					else:
						string += end_position_symbol + " "
				elif functions.indexToCoordinate([x, y]) in self.positions:
					if separators:
						string += "| " + line_symbol + " "
					else:
						string += line_symbol + " "
				else:
					if separators:
						string += "| " + empty_squares + " "
					else:
						string += empty_squares + " "
			if separators:
				string += "|"
		if separators:
			string += "\n---------------------------------"
		if print_result:
			print(string)
		else:
			return string

	def __str__(self):
		"""
		:return: str
		"""
		return self.visualized()

	def __repr__(self):
		"""
		:return: str
		"""
		return str(self.positions)

	def __unicode__(self):
		"""
		:return: str
		"""
		return self.visualized()

	def __contains__(self, item):
		"""
		:type item: Any
		:return: bool
		"""
		return item in self.positions


class Square:
	def __init__(self, position, board):
		"""
		Initialize the square
		:type position: List[int]
		:type board: Game
		:return: None
		"""
		self.position = functions.indexToCoordinate(position)
		self.board = board
		if ((position[0] + position[1]) & 1) == 0:
			self.color = Color.white
		else:
			self.color = Color.black

	def __str__(self):
		"""
		:return: str
		"""
		return self.color.title() + " square from " + str(self.board)

	def __eq__(self, other):
		"""
		:type other: Any
		:return: bool
		"""
		return self.position == other.position and isinstance(other, Square)

	def __unicode__(self):
		"""
		:return: str
		"""
		return self.color.title() + " square"

	__lt__ = __le__ = lambda self, *args: self.error(Exception("Cannot compare squares"))

	__add__ = __radd__ = __sub__ = __rsub__ = __mul__ = __rmul__ = __div__ = __rdiv__ = __truediv__ = __rtruediv__ = __floordiv__ = __rfloordiv__ = __mod__ = __rmod__ = __divmod__ = __rdivmod__ = __pow__ = __rpow__ = __lshift__ = __rlshift__ = __rshift__ = __rrshift__ = __and__ = __rand__ = __or__ = __ror__ = __xor__ = __rxor__ = __iadd__ = __isub__ = __imul__ = __idiv__ = __itruediv__ = __ifloordiv__ = __imod__ = __ipow__ = __iand__ = __ior__ = __ixor__ = __ilshift__ = __irshift__ = __neg__ = __pos__ = __abs__ = __invert__ = __int__ = __long__ = __float__ = __complex__ = __oct__ = __hex__ = __coerce__ = lambda self, *args: self.error(ArithmeticError("Cannot perform arithmetic operations on Square object"))

	__getitem__ = __setitem__ = __delitem__ = __getslice__ = __setslice__ = __delslice__ = __contains__ = lambda self, *args: self.board.error(IndexError("Cannot perform operation on Square"))


class Piece:
	def __init__(self, position, piece_type, color, board):
		"""
		Initialize the piece
		:type position: str
		:type piece_type: str
		:type color: str
		:type board: Game
		:return: None
		"""
		if isinstance(position, str):
			self.position = position
		else:
			self.position = functions.indexToCoordinate(position)
		self.piece_type, self.color, self.board = piece_type, color, board
		self.moved = False
		self.en_passant = False

	def moveTo(self, position, override_pieces=True, evaluate_opening=True, evaluate_checks=True):
		"""
		Move the piece to a position
		:type position: str
		:type override_pieces: bool
		:type evaluate_opening: bool
		:type evaluate_checks: bool
		:return: None
		"""
		if self.board.pieceAt(position) and override_pieces:
			self.board.pieces.remove(self.board.pieceAt(position))
			self.board.squares_hashtable[position] = False
		elif not override_pieces and self.board.pieceAt(position):
			self.board.pieceAt(position).position = self.position
		self.board.squares_hashtable[self.position], self.board.squares_hashtable[position] = self.board.squares_hashtable[position], self.board.squares_hashtable[self.position]
		self.position = position
		if evaluate_checks:
			for i in self.moves(show_data=True, evaluate_checks=False):
				if i.new_position == self.board.getKing(Color.invert(self.color)).position:
					self.board.in_check = Color.invert(self.color)
					break
		if evaluate_opening:
			self.board.updateOpening()

	def moves(self, show_data=False, evaluate_checks=True):
		"""
		Legal moves of the piece
		:type show_data: bool
		:type evaluate_checks: bool
		:return: List[Move] | List[str]
		"""
		if self.board.game_over:
			return []
		moves = []
		if self.piece_type == PieceEnum.pawn:  # Pawn moves
			moves.extend(self.board.generatePawnCaptures(self.position, self.color, piece=self))
			moves.extend(self.board.generatePawnMoves(self.position, self.color, piece=self))
		elif self.piece_type == PieceEnum.knight:  # Knight moves
			moves.extend(self.board.generateKnightMoves(self.position, self.color, piece=self))
		elif self.piece_type == PieceEnum.bishop:  # Bishop moves
			moves.extend(self.board.generateBishopMoves(self.position, self.color, piece=self))
		if self.piece_type == PieceEnum.rook:  # Rook moves
			moves.extend(self.board.generateRookMoves(self.position, self.color, piece=self))
		elif self.piece_type == PieceEnum.queen:  # Queen moves
			moves.extend(self.board.generateQueenMoves(self.position, self.color, piece=self))
		elif self.piece_type == PieceEnum.king:
			moves.extend(self.board.generateKingMoves(self.position, self.color, piece=self))
			moves.extend(self.board.generateKingCastles(self.position, piece=self))
		check_line = self.board.checkLine()
		new_moves = []
		for x in moves:
			if self.board.in_check and self.piece_type != PieceEnum.king and x.new_position not in check_line.positions + [check_line.start_position]:
				continue
			if evaluate_checks:
				if self.piece_type == PieceEnum.pawn:
					moves_ = []
					for z in self.board.generatePawnCaptures(x.new_position, self.color):
						moves_.append(z.new_position)
					if self.board.getKing(Color.invert(self.color)).position in moves_:
						x.name += "+"
						x.check = True
				elif self.piece_type == PieceEnum.knight:
					moves_ = []
					for z in self.board.generateKnightMoves(x.new_position, self.color):
						moves_.append(z.new_position)
					if self.board.getKing(Color.invert(self.color)).position in moves_:
						x.name += "+"
						x.check = True
				elif self.piece_type == PieceEnum.bishop:
					moves_ = []
					for z in self.board.generateBishopMoves(x.new_position, self.color):
						moves_.append(z.new_position)
					if self.board.getKing(Color.invert(self.color)).position in moves_:
						x.name += "+"
						x.check = True
				elif self.piece_type == PieceEnum.rook:
					moves_ = []
					for z in self.board.generateRookMoves(x.new_position, self.color):
						moves_.append(z.new_position)
					if self.board.getKing(Color.invert(self.color)).position in moves_:
						x.name += "+"
						x.check = True
				elif self.piece_type == PieceEnum.queen:
					moves_ = []
					for z in self.board.generateQueenMoves(x.new_position, self.color):
						moves_.append(z.new_position)
					if self.board.getKing(Color.invert(self.color)).position in moves_:
						x.name += "+"
						x.check = True
			if show_data:
				new_moves.append(x)
			else:
				new_moves.append(x.name)
		return new_moves

	def __str__(self):
		"""
		:return: str
		"""
		return self.color.title() + " " + self.piece_type + " at " + self.position

	def __lt__(self, other):
		"""
		:type other: Any
		:return: bool
		"""
		return PieceEnum.value(self.piece_type) < PieceEnum.value(other)

	def __le__(self, other):
		"""
		:type other: Any
		:return: bool
		"""
		return PieceEnum.value(self.piece_type) <= PieceEnum.value(other)

	def __eq__(self, other):
		"""
		:type other: Any
		:return: bool
		"""
		if isinstance(other, Piece):
			other_vars = {}
			for x, y in vars(other).items():
				if x != "board":
					other_vars[x] = y
			this_vars = {}
			for x, y in vars(self).items():
				if x != "board":
					this_vars[x] = y
			return other_vars == this_vars
		return False

	def __unicode__(self):
		"""
		:return: str
		"""
		return self.color.title() + " " + self.piece_type

	__add__ = __radd__ = __sub__ = __rsub__ = __mul__ = __rmul__ = __div__ = __rdiv__ = __truediv__ = __rtruediv__ = __floordiv__ = __rfloordiv__ = __mod__ = __rmod__ = __divmod__ = __rdivmod__ = __pow__ = __rpow__ = __lshift__ = __rlshift__ = __rshift__ = __rrshift__ = __and__ = __rand__ = __or__ = __ror__ = __xor__ = __rxor__ = __iadd__ = __isub__ = __imul__ = __idiv__ = __itruediv__ = __ifloordiv__ = __imod__ = __ipow__ = __iand__ = __ior__ = __ixor__ = __ilshift__ = __irshift__ = __neg__ = __pos__ = __abs__ = __invert__ = __int__ = __long__ = __float__ = __complex__ = __oct__ = __hex__ = __coerce__ = lambda self, *args: self.error(ArithmeticError("Cannot perform arithmetic operations on Piece object"))

	__getitem__ = __setitem__ = __delitem__ = __getslice__ = __setslice__ = __delslice__ = __contains__ = lambda self, *args: self.board.error(IndexError("Cannot perform operation on Piece"))


class Game:
	def __init__(self, fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", raise_errors=True, evaluate_openings=False, pieces=Piece):
		"""
		Initialize the game
		:type fen: str
		:type raise_errors: bool
		:type evaluate_openings: bool
		:type pieces: Any
		:return: None
		"""
		if not functions.FENvalid(fen):
			fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
		self.tags = {"Result": "*"}
		self.properties = {
			"promotions": {"N": PieceEnum.knight, "B": PieceEnum.bishop, "R": PieceEnum.rook, "Q": PieceEnum.queen}
		}
		self.pieces_class = pieces
		self.opening = ""  # Opening
		self.evaluate_openings = evaluate_openings
		self.squares, self.pieces = [], []  # Pieces and squares
		self.in_check = False  # False if neither side is in check, Color.white if white is in check, otherwise Color.black if black is in check
		self.game_over = False
		self.is_checkmate = False
		self.is_stalemate = False
		self.drawn = False
		self.checking_piece = None  # The piece checking a king, or None
		self.white_king = self.black_king = None
		# Append squares
		for x in range(8):
			row = []
			for y in range(8):
				row.append(Square([x, y], self))
			self.squares.append(row)
		self.raise_errors = raise_errors  # Raise errors
		# Load FEN-specific values
		self.loadFEN(fen, evaluate_opening=fen != "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

	def loadFEN(self, fen, evaluate_opening=True, evaluate_checks=True):
		"""
		Load/Reload with the specified FEN. Returns whether the FEN loaded successfully
		:type fen: str
		:type evaluate_opening: bool
		:type evaluate_checks: bool
		:return: bool
		"""
		self.move_list, self.raw_move_list = "", []  # Move lists
		if not functions.FENvalid(fen):
			self.error(errors.InvalidFEN(fen))
			return False
		self.positions = [fen]  # Set positions variable
		self.starting_fen = fen  # Set the starting FEN
		# Reset self.pieces
		if self.pieces:
			self.pieces = []
		# If a piece has been captured
		captured_piece = 0
		for x in fen.split()[0].split("/"):
			for y in x:
				captured_piece += int(not unicode(y).isnumeric())
		self.captured_piece = captured_piece < 32
		# The side to move
		if fen.split()[-5].lower() == "w":
			self.turn = Color.white
		else:
			self.turn = Color.black
		self.half_moves = int(fen.split()[-2])  # Halfmove clock
		self.full_moves = int(fen.split()[-1])  # Fullmove clock
		# Castling rights
		if fen.split()[2] != "-":
			self.castling_rights = fen.split()[2]
		else:
			self.castling_rights = None
		# En passant pawns
		if fen.split()[3] != "-":
			self.en_passant_positions = fen.split()[3]
		else:
			self.en_passant_positions = None
		# Clear squares_hashtable
		self.squares_hashtable = {}  # Squares hashtable
		for x in "abcdefgh":
			for y in range(1, 9):
				self.squares_hashtable[x + str(y)] = False
		# Add pieces
		for i, j in enumerate(functions.splitNumbers(fen.split()[0]).split("/")):
			for x, y in enumerate(j):
				if unicode(y).isnumeric():
					continue
				self.pieces.append(self.pieces_class(functions.indexToCoordinate([i, x]), PieceEnum.pawn if y.lower() == "p" else PieceEnum.knight if y.lower() == "n" else PieceEnum.bishop if y.lower() == "b" else PieceEnum.rook if y.lower() == "r" else PieceEnum.queen if y.lower() == "q" else PieceEnum.king, Color.white if y.isupper() else Color.black, self))
				self.squares_hashtable[functions.indexToCoordinate([i, x])] = self.pieces[-1]
				if self.pieces[-1].piece_type == PieceEnum.king:
					if self.pieces[-1].color == Color.white:
						self.white_king = self.pieces[-1]
					else:
						self.black_king = self.pieces[-1]
		# Load opening
		if evaluate_opening:
			self.updateOpening()
		if evaluate_checks:
			in_check = [self.pieceAt(i.new_position) for i in self.legal_moves(show_data=True, color=self.turn, evaluate_checks=False, evaluate_checkmate=False) if i.new_position == self.pieceType(PieceEnum.king, color=Color.invert(self.turn))[0].position]
			if in_check:
				self.in_check = in_check[0]
			else:
				self.in_check = False
		return True

	def loadPGN(self, pgn=None, file=None, quotes="\""):
		"""
		Loads the specified pgn. If the file argument is specified (is not None), loads the text of the file instead.
		:type pgn: str | None
		:type file: str | None
		:type quotes: str
		:return: bool | None
		"""
		if file is pgn is None:
			return

		if file is not None:
			pgn = open(file).read()
		self.__init__()
		for x, y in enumerate(pgn.splitlines()):
			if y.strip() == "":
				continue
			if y.strip().startswith("[") and y.strip().endswith("]"):
				self.tags[y[1:y.index(quotes) - 1]] = y[y.index(quotes) + 1:-2]
				continue
			if y.startswith("1."):
				moves = functions.getMovesFromString(y)
				for i, j in enumerate(moves):
					try:
						if i == len(moves) - 1:
							self.move(j)
						else:
							self.move(j, evaluate_checks=False, evaluate_opening=False)
					except errors.Error:
						self.error(errors.InvalidPGNMove(j, i))
						return False
			else:
				self.error(errors.InvalidPGNLine(y, x + 1))
				return False
		return True

	def loadOpening(self, opening_name):
		"""
		Load the specified opening
		:type opening_name: str
		:return: bool
		"""
		for i in openings.openings:
			if opening_name.lower().replace("king's pawn game", "open game").replace("queen's pawn game", "closed game").replace("russian game", "petrov's defense") in [i["name"].lower(), i["eco"].lower() + " " + i["name"].lower(), i["eco"].lower() + i["name"].lower(), i["eco"].lower().replace("'", ""), i["eco"].lower() + " " + i["name"].lower().replace("'", ""), i["eco"].lower() + i["name"].lower().replace("'", "")]:
				self.loadFEN(i["fen"] + " - 0 1")
				return True
		return False

	def reset(self):
		"""
		Reset game
		:return: None
		"""
		self.loadFEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

	def FEN(self):
		"""
		Returns the FEN of the game
		:return: str
		"""
		fen = ""  # Set fen variable
		# Get squares
		for x in self.squares:
			for y in x:
				if self.pieceAt(y.position):
					fen += (self.pieceAt(y.position).piece_type[0] if self.pieceAt(y.position).piece_type != PieceEnum.knight else "n").upper() if self.pieceAt(y.position).color == Color.white else (self.pieceAt(y.position).piece_type[0] if self.pieceAt(y.position).piece_type != PieceEnum.knight else "n")
				else:
					fen += "1"
			fen += "/"
		fen = functions.combineNumbers(fen[:-1])
		fen += " " + self.turn[0]  # Add the side to move
		fen += " " + (self.castling_rights if self.castling_rights is not None else "-")  # Castling rights
		fen += " " + (self.en_passant_positions if self.en_passant_positions is not None else "-")  # En Passant captures
		fen += " " + str(self.half_moves) + " " + str(self.full_moves)  # Add halfmove and fullmove clock
		return fen

	def PGN(self, **kwargs):
		"""
		Returns the PGN of the game.
		:type kwargs: **str
		:return: str
		"""
		pgn = ""
		for i in kwargs:
			pgn += "[" + i + " \"" + str(kwargs[i]) + "\"]\n"
		pgn += ("\n" if kwargs else "") + self.move_list + str(self.tags["Result"])
		return pgn

	def error(self, error):
		"""
		Raises an error if allowed
		:type error: Any
		:return: None
		"""
		if self.raise_errors:
			raise error

	def placePiece(self, coordinate, color, piece_type):
		"""
		Places a piece with the specified properties at position `coordinate`, overriding any existing pieces on the coordinate.
		:type coordinate: str
		:type color: str
		:type piece_type: str
		:return: Piece
		"""
		if self.pieceAt(coordinate):
			self.pieces.remove(self.pieceAt(coordinate))
		self.pieces.append(self.pieces_class(coordinate, piece_type, color, self))
		self.squares_hashtable[coordinate] = self.pieces[-1]
		return self.pieces[-1]

	def removePiece(self, coordinate):
		"""
		Removes the piece at the specified coordinate
		:type coordinate: str
		:return: Piece | None
		"""
		piece = self.pieceAt(coordinate)
		if piece is not None:
			self.pieces.remove(piece)
			self.squares_hashtable[coordinate] = False
			return piece

	def getKing(self, color):
		"""
		Returns the king of color `color`
		:type color: str
		:return: Piece
		"""
		if not Color.valid(color):
			self.error(errors.UndefinedColor(color))

		if color == Color.white:
			return self.white_king
		return self.black_king

	def checkLine(self):
		"""
		If a side is in check, returns the line in which the check is delivered
		:return: Line | None
		"""
		if not self.in_check:
			return False
		return Line(self.checking_piece.position, self.getKing(self.in_check).position, jump=self.checking_piece.piece_type == PieceEnum.knight)

	def move(self, move, evaluate_checks=True, evaluate_opening=True, evaluate_move_checks=True, evaluate_move_checkmate=True):
		"""
		Makes the specified move if it is legal
		:type move: str | Move
		:type evaluate_checks: bool
		:type evaluate_opening: bool
		:type evaluate_move_checks: bool
		:type evaluate_move_checkmate: bool
		:return: Move
		"""
		move_data = None
		if isinstance(move, str):
			if " " in move:
				for i in move.split()[:-1]:
					self.move(i, evaluate_checks=False, evaluate_move_checks=False, evaluate_opening=False)
				move = move.split()[-1]
			# Iterate through the legal moves
			for i in self.legal_moves(show_data=True, evaluate_checks=evaluate_move_checks, evaluate_checkmate=evaluate_move_checkmate):
				if i.name == move:  # If the name of the current move is the move specified
					move_data = i  # Set move_data equal to the current move
					break  # Break from the loop
			if move_data is None:
				self.error(errors.MoveNotPossible(move))
			move = functions.toSAN(move, self)  # Convert to SAN
		elif isinstance(move, Move):
			move_data = move
			move = move.name
		else:  # If move is not a valid type, raise an error and return False
			self.error(errors.InvalidMove(move))
			return False

		if move_data.is_capture:  # If the move is a capture
			# Remove the captured piece
			self.pieces.remove(self.squares_hashtable[move_data.new_position])
			self.squares_hashtable[move_data.new_position] = False
			self.captured_piece = True

		self.squares_hashtable[move_data.piece.position], self.squares_hashtable[move_data.new_position] = self.squares_hashtable[move_data.new_position], self.squares_hashtable[move_data.piece.position]
		move_data.piece.position = move_data.new_position
		move_data.piece.moved = True
		if move_data.castle_rook:  # If the move is a castle
			move_data.castle_rook.moved = True
			if move_data.castle == Castle.kingside:  # Kingside castling
				# Move the rook's position to the f-file
				self.squares_hashtable[move_data.castle_rook.position], self.squares_hashtable["f" + move_data.castle_rook.position[1]] = self.squares_hashtable["f" + move_data.castle_rook.position[1]], self.squares_hashtable[move_data.castle_rook.position]
				move_data.castle_rook.position = "f" + move_data.castle_rook.position[1]
			else:  # Queenside castling
				# Move the rook's position to the d-file
				self.squares_hashtable[move_data.castle_rook.position], self.squares_hashtable["d" + move_data.castle_rook.position[1]] = self.squares_hashtable["d" + move_data.castle_rook.position[1]], self.squares_hashtable[move_data.castle_rook.position]
				move_data.castle_rook.position = "d" + move_data.castle_rook.position[1]

		# Clear en passant positions
		self.en_passant_positions = None
		for x in self.pieces:
			x.en_passant = False

		# If the move was a double pawn push
		if move_data.double_pawn_move:
			move_data.piece.en_passant = True  # Set en_passant variable of moved piece to true
			self.en_passant_positions = move_data.new_position[0] + str(int(move_data.new_position[1]) - (1 if move_data.piece.color == Color.white else -1))  # Append en passant position to en_passant_positions variable

		# If the move was an en passant capture
		if move_data.en_passant:
			# Remove the captured piece
			self.pieces.remove(self.squares_hashtable[move_data.en_passant_position])
			self.squares_hashtable[move_data.en_passant_position] = False
			self.captured_piece = True

		if self.castling_rights is not None and move_data.piece.piece_type == PieceEnum.king:  # If the piece moved was a king
			if move_data.piece.color == Color.white:  # If moved side is white
				self.castling_rights = self.castling_rights.replace("K", "").replace("Q", "")  # Disable white castling
			else:  # Otherwise (if moved side is black)
				self.castling_rights = self.castling_rights.replace("k", "").replace("q", "")  # Disable black castling
			if self.castling_rights == "":  # If the castling_rights variable is now an empty string
				self.castling_rights = None  # Set the castling_rights variable to None

		if self.castling_rights is not None and move_data.piece.piece_type == PieceEnum.rook:  # If the piece moved was a rook
			if move_data.old_position == "a1":  # If the rook was on a1
				self.castling_rights = self.castling_rights.replace("Q", "")  # Disable white queenside castling
			elif move_data.old_position == "a8":  # If the rook was on a8
				self.castling_rights = self.castling_rights.replace("q", "")  # Disable black queenside castling
			elif move_data.old_position == "h1":  # If the rook was on h1
				self.castling_rights = self.castling_rights.replace("K", "")  # Disable white kingside castling
			elif move_data.old_position == "h8":  # If the rook was on h8
				self.castling_rights = self.castling_rights.replace("k", "")  # Disable black kingside castling

		if move_data.promotion:
			move_data.piece.piece_type = self.properties["promotions"][move_data.promotion]

		self.raw_move_list.append(move_data)  # Append the move to the raw_move_list list

		if move_data is None:  # If move_data is None (no move was found), raise an error and return False
			self.error(errors.MoveNotPossible(move))
			return False
		if self.in_check:  # If a king was in check before this move
			# This move must have gotten out of check
			self.in_check = False
			self.checking_piece = None
		else:  # Otherwise
			if evaluate_checks:  # If the evaluate_checks parameter is True
				if any([True for i in self.legal_moves(show_data=True, color=self.turn, evaluate_checks=evaluate_move_checks, evaluate_checkmate=evaluate_move_checkmate) if i.new_position == self.pieceType(PieceEnum.king, color=Color.invert(self.turn))[0].position]):  # If the king can be captured
					self.in_check = Color.invert(self.turn)  # Set in_check variable
					self.checking_piece = move_data.piece
				else:  # Otherwise
					self.in_check = False  # Set in_check to False
					self.checking_piece = None  # Reset piece giving check

		# Add move to move list and increase fullmove counter if necessary
		if self.turn == Color.white:  # If white moved
			# Add move to move list
			if self.move_list == "":  # If there has not been any moves
				self.move_list += "1. " + move  # Add a "1. " before the move string to the moves list
			else:  # Otherwise
				self.move_list += " " + str(int(self.move_list.split()[-3][0]) + 1) + ". " + move  # Add a space character, the move number, followed by a period before the move string to the moves list
		else:  # If black moved
			if self.move_list == "":  # If there has not been any moves (a custom FEN)
				self.move_list += "1. ... " + move  # Add a "1. ..." string before the move name to the moves list
			else:  # Otherwise
				self.move_list += " " + move  # Add move name (preceded by a space) to move list

			self.full_moves += 1  # Increase the fullmove counter

		# Calculate halfmove counter
		if move_data.is_capture or move_data.piece.piece_type == PieceEnum.pawn:  # Reset halfmove counter if the move is a pawn move or a capture
			self.half_moves = 0
		else:  # Otherwise, increase the halfmove counter by 1
			self.half_moves += 1

		self.turn = Color.invert(self.turn)  # Invert turn

		if evaluate_opening:  # If the evaluate_opening parameter is True
			self.updateOpening()  # Update the opening using the updateOpening function

		if not self.legal_moves(evaluate_checks=False, evaluate_checkmate=False):
			self.game_over = True
			if self.in_check:
				self.is_checkmate = True
				self.tags["Result"] = "1-0" if self.turn == Color.black else "0-1"
			else:
				self.drawn = True
				self.is_stalemate = True
				self.tags["Result"] = "1/2-1/2"

		self.positions.append(self.FEN())  # Append the current FEN to the positions list

		return move_data  # Return the move data (Move object)

	def legal_moves(self, show_data=False, color=Color.current, evaluate_checks=True, evaluate_checkmate=True, piece_type=PieceEnum.all()):
		"""
		Returns all legal moves by pieces of type(s) piece_type
		:type show_data: bool
		:type color: str
		:type evaluate_checks: bool
		:type evaluate_checkmate: bool
		:type piece_type: str | List[str]
		:return: List[str] | List[Move]
		"""
		if self.game_over:
			return []

		moves = []  # Define empty moves list

		if color == Color.current:
			color = self.turn

		if isinstance(piece_type, (list, set, tuple)):  # If the piece_type parameter is an iterable
			for i in self.pieces:  # Iterate through pieces
				if (color == Color.any or i.color == color) and i.piece_type in piece_type:
					moves.extend(i.moves(show_data=show_data, evaluate_checks=evaluate_checks))  # Append the piece moves
		elif piece_type in PieceEnum.all():  # If the piece type is a single type
			for i in self.pieceType(piece_type):  # Iterate through the pieces of the specified type
				if color == Color.any or i.color == color:  # If the specified color(s) includes the piece color
					moves.extend(i.moves(show_data=show_data, evaluate_checks=evaluate_checks))  # Append the piece moves

		return moves  # Return result

	def pieceType(self, piece, color=Color.any):
		"""
		Returns all pieces with type `piece` and color `color`
		:type piece: str
		:type color: str
		:return: List[Piece]
		"""
		if color == Color.any:
			color = [Color.white, Color.black]
		elif color == Color.current:
			color = [self.turn]
		else:
			color = [color]

		return [i for i in self.pieces if i.color in color and i.piece_type == piece]

	def gamePhase(self):
		"""
		Returns the current game phase
		:return: str
		"""
		# The game is in the opening phase if there are less than 7 full moves or a piece has not been captured
		if len(self.raw_move_list) // 2 <= 6 or not self.captured_piece:
			return Phase.opening

		# If the game is not in the opening phase, it is in the endgame phase if both sides do not have a queen, or if the king moved more than three times
		if not self.pieceType(PieceEnum.queen) or [i.piece.piece_type for i in self.raw_move_list].count(PieceEnum.king) > 3:
			return Phase.endgame

		return Phase.middlegame  # Otherwise, the game must be in the middlegame phase

	def totalMaterial(self):
		"""
		The total amount of material
		:return: int
		"""
		material = 0
		for i in self.pieces:
			if i.piece_type != PieceEnum.king:
				material += PieceEnum.value(i.piece_type)
		return material

	def materialDifference(self):
		"""
		Returns the material difference. Positive values indicate white has more material, while negative values indicate black has more.
		:return: int
		"""
		difference = 0
		for i in self.pieces:
			if i.piece_type == PieceEnum.king:
				continue
			if i.color == Color.white:
				difference += PieceEnum.value(i.piece_type)
			else:
				difference -= PieceEnum.value(i.piece_type)

		return difference

	def evaluate(self):
		"""
		Evaluates the current position
		:return: float
		"""
		evaluation_centipawns = (self.materialDifference() * 100) + (0.1 * (len(self.legal_moves(color=Color.white)) - len(self.legal_moves(color=Color.black))))  # Material difference + piece mobility

		for i in self.pieces:
			evaluation_centipawns += PieceEnum.evaluate_piece_position(i.piece_type, i.position, i.color, self.gamePhase()) / 10

		return round(evaluation_centipawns / 100, 5)

	def pieceAt(self, coordinate):
		"""
		Returns the piece at coordinate if one exists, otherwise return None
		:type coordinate: str
		:return: None | Piece
		"""
		if not functions.coordinateValid(coordinate):  # If the coordinate is not valid, raise an error and return None
			self.error(errors.InvalidCoordinate(coordinate))
			return None
		if self.squares_hashtable[coordinate]:
			return self.squares_hashtable[coordinate]
		return None

	def takeback(self, evaluate_openings=True, evaluate_checks=True):
		"""
		Take backs one move. To take back multiple moves, call the function multiple times.
		:type evaluate_openings: bool
		:type evaluate_checks: bool
		:return: None
		"""
		if not self.raw_move_list:  # If there has not been any moves, return
			return

		# Reset the moved piece's position
		self.squares_hashtable[self.raw_move_list[-1].new_position], self.squares_hashtable[self.raw_move_list[-1].old_position] = self.squares_hashtable[self.raw_move_list[-1].old_position], self.squares_hashtable[self.raw_move_list[-1].new_position]
		self.raw_move_list[-1].piece.position = self.raw_move_list[-1].old_position

		if self.raw_move_list[-1].is_capture:  # If the last move was a capture
			# Bring back the captured piece
			self.pieces.append(self.pieces_class(self.raw_move_list[-1].new_position, self.raw_move_list[-1].captured_piece.piece_type, self.raw_move_list[-1].captured_piece.color, self))
			self.squares_hashtable[self.raw_move_list[-1].new_position] = self.pieces[-1]

		# Reset the castle rook's position if the last move was a castle
		if self.raw_move_list[-1].castle == Castle.kingside:  # If the last move was a kingside castle
			self.squares_hashtable[self.raw_move_list[-1].castle_rook.position], self.squares_hashtable["h" + self.raw_move_list[-1].castle_rook.position[1]] = self.squares_hashtable["h" + self.raw_move_list[-1].castle_rook.position[1]], self.squares_hashtable[self.raw_move_list[-1].castle_rook.position]
			self.raw_move_list[-1].castle_rook.position = "h" + self.raw_move_list[-1].castle_rook.position[1]
		elif self.raw_move_list[-1].castle == Castle.queenside:  # If the last move was a queenside castle
			self.squares_hashtable[self.raw_move_list[-1].castle_rook.position], self.squares_hashtable["f" + self.raw_move_list[-1].castle_rook.position[1]] = self.squares_hashtable["f" + self.raw_move_list[-1].castle_rook.position[1]], self.squares_hashtable[self.raw_move_list[-1].castle_rook.position]
			self.raw_move_list[-1].castle_rook.position = "f" + self.raw_move_list[-1].castle_rook.position[1]

		# If the last move was a promotion
		if self.raw_move_list[-1].promotion:
			self.raw_move_list[-1].piece.piece_type = PieceEnum.pawn  # Make the promoted piece a pawn
		
		self.half_moves = int(self.positions[-2].split()[-2])

		self.raw_move_list.pop()  # Remove the last move from the raw move list

		# Remove the last move from the move list
		if self.move_list.split()[-2][-1] == ".":
			self.move_list = " ".join(self.move_list.split()[:-2])
		else:
			self.move_list = " ".join(self.move_list.split()[:-1])
		
		self.turn = Color.invert(self.turn)  # Invert the turn
		# Update en_passant_positions
		if self.positions[-2].split()[-3] == "-":
			self.en_passant_positions = None
		else:
			self.en_passant_positions = self.positions[-2].split()[-3]
		# Set opening
		if self.move_list == "":
			self.opening = ""
		elif evaluate_openings:
			self.updateOpening()
		# Update self.positions list
		self.positions.pop()
		# Update in_check variable
		if evaluate_checks:
			in_check = False
			for x in self.pieces:
				if x.color == self.turn or x.piece_type == PieceEnum.king:
					continue
				if x.piece_type == PieceEnum.pawn:
					generate_function = self.generatePawnCaptures
				elif x.piece_type == PieceEnum.knight:
					generate_function = self.generateKnightMoves
				elif x.piece_type == PieceEnum.bishop:
					generate_function = self.generateBishopMoves
				elif x.piece_type == PieceEnum.rook:
					generate_function = self.generateRookMoves
				else:
					generate_function = self.generateQueenMoves
				for y in generate_function(x.position, x.color):
					if y.new_position == self.getKing(self.turn).position:
						self.in_check = self.turn
						in_check = True
						break
			if not in_check:
				self.in_check = False

	def updateOpening(self):
		"""
		Updates the opening if allowed
		:return: False | str
		"""
		if self.evaluate_openings:
			position = self.FEN().split()[0]
			for i in openings.openings:
				if i["position"] == position:
					self.opening = i["eco"] + " " + i["name"]
					return self.opening
		return False

	def attackers(self, coordinate, color):
		"""
		Returns the pieces that attack the coordinate
		:type coordinate: str
		:type color: str
		:return: List[Piece]
		"""
		if color == Color.current:
			color = self.turn
		if color not in [Color.white, Color.black]:
			self.error(errors.UndefinedColor(color))
			return []
		if self.pieceAt(coordinate) and self.pieceAt(coordinate).color == color:
			self.error(errors.InvalidColor("The color " + str(color) + " is invalid, as the piece at " + str(coordinate) + " has the same color. Perhaps you meant to use the protectors() function?"))
			return []
		attackers = []
		for i in self.pieces:
			if i.color != color:
				continue
			if i.piece_type == PieceEnum.pawn:  # Pawn capture squares
				if coordinate in [x.new_position for x in self.generatePawnCaptures(i.position, color, return_all=True)]:
					attackers.append(i)
			elif i.piece_type == PieceEnum.knight:  # Knight capture squares
				if coordinate in [x.new_position for x in self.generateKnightMoves(i.position, color)]:
					attackers.append(i)
			elif i.piece_type == PieceEnum.bishop:  # Bishop capture squares
				if coordinate in [x.new_position for x in self.generateBishopMoves(i.position, color)]:
					attackers.append(i)
			elif i.piece_type == PieceEnum.rook:  # Rook capture squares
				if coordinate in [x.new_position for x in self.generateRookMoves(i.position, color)]:
					attackers.append(i)
			elif i.piece_type == PieceEnum.queen:  # Queen capture squares
				if coordinate in [x.new_position for x in self.generateQueenMoves(i.position, color)]:
					attackers.append(i)
			elif i.piece_type == PieceEnum.king:  # King capture squares
				if functions.coordinateToIndex(coordinate) in [[functions.coordinateToIndex(i.position)[0] - 1, functions.coordinateToIndex(i.position)[1] - 1], [functions.coordinateToIndex(i.position)[0] - 1, functions.coordinateToIndex(i.position)[1]], [functions.coordinateToIndex(i.position)[0] - 1, functions.coordinateToIndex(i.position)[1] + 1], [functions.coordinateToIndex(i.position)[0], functions.coordinateToIndex(i.position)[1] - 1], [functions.coordinateToIndex(i.position)[0], functions.coordinateToIndex(i.position)[1] + 1], [functions.coordinateToIndex(i.position)[0] + 1, functions.coordinateToIndex(i.position)[1] - 1], [functions.coordinateToIndex(i.position)[0] + 1, functions.coordinateToIndex(i.position)[1]], [functions.coordinateToIndex(i.position)[0] + 1, functions.coordinateToIndex(i.position)[1] + 1]]:
					attackers.append(i)
		return attackers

	def protectors(self, piece):
		"""
		Returns the protectors of the piece
		:type piece: Piece
		:return: List[Piece]
		"""
		if not isinstance(piece, Piece):
			self.error(errors.InvalidPiece(piece))
		protectors = []
		for x in self.pieces:
			if x.color != piece.color:
				continue
			if x.piece_type == PieceEnum.pawn:
				if piece.position in [i.new_position for i in self.generatePawnCaptures(x.position, x.color, return_all=True)]:
					protectors.append(x)
			elif x.piece_type == PieceEnum.knight:
				if piece.position in [i.new_position for i in self.generateKnightMoves(x.position, x.color, return_all=True)]:
					protectors.append(x)
			elif x.piece_type == PieceEnum.bishop:
				if piece.position in [i.new_position for i in self.generateBishopMoves(x.position, x.color, stop=Stop.piece)]:
					protectors.append(x)
			elif x.piece_type == PieceEnum.rook:
				if piece.position in [i.new_position for i in self.generateRookMoves(x.position, x.color, stop=Stop.piece)]:
					protectors.append(x)
			elif x.piece_type == PieceEnum.queen:
				if piece.position in [i.new_position for i in self.generateQueenMoves(x.position, x.color, stop=Stop.piece)]:
					protectors.append(x)
		return protectors

	def visualized(self, print_result=False, use_unicode=True, empty_squares=" ", separators=True):
		"""
		Returns a string representation of the pieces
		:type print_result: bool
		:type use_unicode: bool
		:type empty_squares: str
		:type separators: bool
		:return: None | str
		"""
		if empty_squares == "":
			empty_squares = " "
		empty_squares = empty_squares[0]
		string = ""
		for x in range(8):
			string += "\n"
			if separators:
				if use_unicode:
					string += "---------------------------------\n"
				else:
					string += "-----------------------------------------\n"
			for y in range(8):
				if self.pieceAt(functions.indexToCoordinate([x, y])):
					if separators:
						if use_unicode:
							string += "| " + PieceEnum.unicode(self.pieceAt(functions.indexToCoordinate([x, y])).piece_type, self.pieceAt(functions.indexToCoordinate([x, y])).color) + " "
						else:
							string += "| " + str(self.pieceAt(functions.indexToCoordinate([x, y])).color[0]).upper() + {"pawn": "P", "knight": "N", "bishop": "B", "rook": "R", "queen": "Q", "king": "K"}[self.pieceAt(functions.indexToCoordinate([x, y])).piece_type] + " "
					else:
						if use_unicode:
							string += PieceEnum.unicode(self.pieceAt(functions.indexToCoordinate([x, y])).piece_type, self.pieceAt(functions.indexToCoordinate([x, y])).color) + " "
						else:
							string += str(self.pieceAt(functions.indexToCoordinate([x, y])).color[0]).upper() + {"pawn": "P", "knight": "N", "bishop": "B", "rook": "R", "queen": "Q", "king": "K"}[self.pieceAt(functions.indexToCoordinate([x, y])).piece_type] + " "
				else:
					if separators:
						if use_unicode:
							string += "| " + empty_squares + " "
						else:
							string += "|  " + empty_squares + " "
					else:
						if use_unicode:
							string += empty_squares + " "
						else:
							string += " " + empty_squares + " "
			if separators:
				string += "|"
		if separators:
			if use_unicode:
				string += "\n---------------------------------"
			else:
				string += "\n-----------------------------------------"
		if print_result:
			print(string)
		else:
			return string

	def generatePawnMoves(self, position, color, return_all=False, piece=None):
		"""
		:type position: str
		:type color: str
		:type return_all: bool
		:type piece: Piece | None
		:return: List[Move]
		"""
		moves = []
		if (color == Color.black and position[1] == "1") or (color == Color.white and position[1] == "8") or not functions.coordinateValid(position):
			return moves if (color == Color.black and position[1] == "1") or (color == Color.white and position[1] == "8") else [self.error(errors.InvalidCoordinate(position)), moves][1]

		if Color.isWhite(color):
			if return_all:
				moves = [Move(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1]]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1]]), piece), Move(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 2, functions.coordinateToIndex(position)[1]]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 2, functions.coordinateToIndex(position)[1]]), piece, double_pawn_move=True)]
			else:
				if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1]])):
					return moves
				if position[1] == "2" and not self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 2, functions.coordinateToIndex(position)[1]])):
					moves = [Move(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1]]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1]]), piece), Move(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 2, functions.coordinateToIndex(position)[1]]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 2, functions.coordinateToIndex(position)[1]]), piece, double_pawn_move=True)]
				else:
					moves = [Move(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1]]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1]]), piece)]
			if position[1] == "7" and not self.pieceAt(position[0] + "8"):
				return [Move(position[0] + "8=" + i, position, position[0] + "8", piece, promotion=i) for i in list(self.properties["promotions"])]
			return moves
		elif Color.isBlack(color):
			if return_all:
				moves = [Move(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1]]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1]]), piece), Move(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 2, functions.coordinateToIndex(position)[1]]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 2, functions.coordinateToIndex(position)[1]]), piece, double_pawn_move=True)]
			else:
				if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1]])):
					return moves
				if position[1] == "7" and not self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 2, functions.coordinateToIndex(position)[1]])):
					moves = [Move(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1]]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1]]), piece), Move(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 2, functions.coordinateToIndex(position)[1]]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 2, functions.coordinateToIndex(position)[1]]), piece, double_pawn_move=True)]
				else:
					moves = [Move(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1]]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1]]), piece)]
			if position[1] == "2" and not self.pieceAt(position[0] + "1"):
				return [Move(position[0] + "1=" + i, position, position[0] + "1", piece, promotion=i) for i in list(self.properties["promotions"])]
			return moves
		else:
			self.error(errors.UndefinedColor(color))
			return []

	def generatePawnCaptures(self, position, color, return_all=False, piece=None):
		"""
		:type position: str
		:type color: str
		:type return_all: bool
		:type piece: Piece | None
		:return: List[Move]
		"""
		if (color == Color.black and position[1] == "1") or (color == Color.white and position[1] == "8"):
			return []

		if not functions.coordinateValid(position):
			self.error(errors.InvalidCoordinate(position))
			return []

		if Color.isWhite(color):
			if position[0] not in "ah" and (return_all or (self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 1])) and self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 1])) and self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 1])).color != color and self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 1])).color != color)):
				if position[1] == "7":
					return [Move(position[0] + "x" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 1]) + "=" + i, position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 1]), piece, is_capture=True, promotion=i) for i in list(self.properties["promotions"])] + [Move(position[0] + "x" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 1]) + "=" + i, position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 1]), piece, is_capture=True, promotion=i) for i in list(self.properties["promotions"])]
				return [Move(position[0] + "x" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 1]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 1]), piece, is_capture=True), Move(position[0] + "x" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 1]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 1]), piece, is_capture=True)]

			if position[0] != "h" and self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 1])) and self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 1])).color != color:
				if position[1] == "7":
					return [Move(position[0] + "x" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 1]) + "=" + i, position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 1]), piece, is_capture=True, promotion=i) for i in list(self.properties["promotions"])]
				return [Move(position[0] + "x" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 1]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 1]), piece, is_capture=True)]

			if position[0] != "a" and self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 1])) and self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 1])).color != color:
				if position[1] == "7":
					return [Move(position[0] + "x" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 1]) + "=" + i, position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 1]), piece, is_capture=True, promotion=i) for i in list(self.properties["promotions"])]
				return [Move(position[0] + "x" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 1]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 1]), piece, is_capture=True)]
		elif Color.isBlack(color):
			if position[0] not in "ah" and (return_all or (self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 1])) and self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 1])) and self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 1])).color != color and self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 1])).color != color)):
				if position[1] == "2":
					return [Move(position[0] + "x" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 1]) + "=" + i, position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 1]), piece, is_capture=True, promotion=i) for i in list(self.properties["promotions"])] + [Move(position[0] + "x" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 1]) + "=" + i, position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 1]), piece, is_capture=True, promotion=i) for i in list(self.properties["promotions"])]
				return [Move(position[0] + "x" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 1]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 1]), piece, is_capture=True), Move(position[0] + "x" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 1]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 1]), piece, is_capture=True)]

			if position[0] != "h" and self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 1])) and self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 1])).color != color:
				if position[1] == "2":
					return [Move(position[0] + "x" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 1]) + "=" + i, position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 1]), piece, is_capture=True, promotion=i) for i in list(self.properties["promotions"])]
				return [Move(position[0] + "x" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 1]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 1]), piece, is_capture=True)]

			if position[0] != "a" and self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 1])) and self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 1])).color != color:
				if position[1] == "2":
					return [Move(position[0] + "x" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 1]) + "=" + i, position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 1]), piece, is_capture=True, promotion=i) for i in list(self.properties["promotions"])]
				return [Move(position[0] + "x" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 1]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 1]), piece, is_capture=True)]
		else:
			self.error(errors.UndefinedColor(color))

		return []

	def generateKnightMoves(self, position, color, return_all=False, piece=None):
		"""
		:type position: str
		:type color: str
		:type return_all: bool
		:type piece: Piece | None
		:return: List[Move]
		"""
		if not functions.coordinateValid(position):
			self.error(errors.InvalidCoordinate(position))
			return []
		if not Color.valid(color):
			self.error(errors.UndefinedColor(color))
			return []
		moves = []
		if position[0] != "h" and position[1] not in ["1", "2"]:
			if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 2, functions.coordinateToIndex(position)[1] + 1])) and not return_all:
				if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 2, functions.coordinateToIndex(position)[1] + 1])).color == Color.invert(color):
					moves.append(Move("Nx" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 2, functions.coordinateToIndex(position)[1] + 1]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 2, functions.coordinateToIndex(position)[1] + 1]), piece, is_capture=True))
			else:
				moves.append(Move("N" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 2, functions.coordinateToIndex(position)[1] + 1]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 2, functions.coordinateToIndex(position)[1] + 1]), piece))
		if position[0] not in ["g", "h"] and position[1] != "1":
			if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 2])) and not return_all:
				if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 2])).color == Color.invert(color):
					moves.append(Move("Nx" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 2]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 2]), piece, is_capture=True))
			else:
				moves.append(Move("N" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 2]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 2]), piece))
		if position[0] != "a" and position[1] not in ["7", "8"]:
			if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 2, functions.coordinateToIndex(position)[1] - 1])) and not return_all:
				if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 2, functions.coordinateToIndex(position)[1] - 1])).color == Color.invert(color):
					moves.append(Move("Nx" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 2, functions.coordinateToIndex(position)[1] - 1]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 2, functions.coordinateToIndex(position)[1] - 1]), piece, is_capture=True))
			else:
				moves.append(Move("N" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 2, functions.coordinateToIndex(position)[1] - 1]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 2, functions.coordinateToIndex(position)[1] - 1]), piece))
		if position[0] not in ["a", "b"] and position[1] != "8":
			if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 2])) and not return_all:
				if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 2])).color == Color.invert(color):
					moves.append(Move("Nx" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 2]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 2]), piece, is_capture=True))
			else:
				moves.append(Move("N" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 2]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 2]), piece))
		if position[0] != "a" and position[1] not in ["1", "2"]:
			if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 2, functions.coordinateToIndex(position)[1] - 1])) and not return_all:
				if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 2, functions.coordinateToIndex(position)[1] - 1])).color == Color.invert(color):
					moves.append(Move("Nx" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 2, functions.coordinateToIndex(position)[1] - 1]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 2, functions.coordinateToIndex(position)[1] - 1]), piece, is_capture=True))
			else:
				moves.append(Move("N" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 2, functions.coordinateToIndex(position)[1] - 1]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 2, functions.coordinateToIndex(position)[1] - 1]), piece))
		if position[0] not in ["a", "b"] and position[1] != "1":
			if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 2])) and not return_all:
				if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 2])).color == Color.invert(color):
					moves.append(Move("Nx" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 2]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 2]), piece, is_capture=True))
			else:
				moves.append(Move("N" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 2]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 2]), piece))
		if position[0] != "h" and position[1] not in ["7", "8"]:
			if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 2, functions.coordinateToIndex(position)[1] + 1])) and not return_all:
				if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 2, functions.coordinateToIndex(position)[1] + 1])).color == Color.invert(color):
					moves.append(Move("Nx" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 2, functions.coordinateToIndex(position)[1] + 1]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 2, functions.coordinateToIndex(position)[1] + 1]), piece, is_capture=True))
			else:
				moves.append(Move("N" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 2, functions.coordinateToIndex(position)[1] + 1]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 2, functions.coordinateToIndex(position)[1] + 1]), piece))
		if position[0] not in ["g", "h"] and position[1] != "8":
			if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 2])) and not return_all:
				if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 2])).color == Color.invert(color):
					moves.append(Move("Nx" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 2]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 2]), piece, is_capture=True))
			else:
				moves.append(Move("N" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 2]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 2]), piece))
		return moves

	def generateBishopMoves(self, position, color, stop=Stop.capture_piece, piece=None):
		"""
		:type position: str
		:type color: str
		:type stop: str
		:type piece: Piece | None
		:return: List[Move]
		"""
		moves = []
		capture, (pos1, pos2), piece_found = False, functions.coordinateToIndex(position), 0
		while pos1 != 0 and pos2 != 0:
			pos1, pos2 = pos1 - 1, pos2 - 1
			if stop == Stop.piece:
				moves.append(Move("B" + functions.indexToCoordinate([pos1, pos2]), position, functions.indexToCoordinate([pos1, pos2]), piece))
				if self.pieceAt(functions.indexToCoordinate([pos1, pos2])):
					break
			elif stop != Stop.never:
				for i in self.pieces:
					if functions.coordinateToIndex(i.position) == [pos1, pos2]:
						if stop == Stop.capture_piece:
							if i.color == color:
								break
							capture = True
						elif stop == Stop.no_capture:
							break
				else:
					moves.append(Move("B" + ("x" if capture else "") + functions.indexToCoordinate([pos1, pos2]), position, functions.indexToCoordinate([pos1, pos2]), piece, is_capture=capture))
					if capture:
						break
					continue
				break
			else:
				moves.append(Move("B" + functions.indexToCoordinate([pos1, pos2]), position, functions.indexToCoordinate([pos1, pos2]), piece))
		capture, (pos1, pos2) = False, functions.coordinateToIndex(position)
		while pos1 != 7 and pos2 != 7:
			pos1, pos2 = pos1 + 1, pos2 + 1
			if stop == Stop.piece:
				moves.append(Move("B" + functions.indexToCoordinate([pos1, pos2]), position, functions.indexToCoordinate([pos1, pos2]), piece))
				if self.pieceAt(functions.indexToCoordinate([pos1, pos2])):
					break
			elif stop != Stop.never:
				for i in self.pieces:
					if functions.coordinateToIndex(i.position) == [pos1, pos2]:
						if stop == Stop.capture_piece:
							if i.color == color:
								break
							capture = True
						elif stop == Stop.no_capture:
							break
				else:
					moves.append(Move("B" + ("x" if capture else "") + functions.indexToCoordinate([pos1, pos2]), position, functions.indexToCoordinate([pos1, pos2]), piece, is_capture=capture))
					if capture:
						break
					continue
				break
			else:
				moves.append(Move("B" + functions.indexToCoordinate([pos1, pos2]), position, functions.indexToCoordinate([pos1, pos2]), piece))
		capture, (pos1, pos2) = False, functions.coordinateToIndex(position)
		while pos1 != 0 and pos2 != 7:
			pos1, pos2 = pos1 - 1, pos2 + 1
			if stop == Stop.piece:
				moves.append(Move("B" + functions.indexToCoordinate([pos1, pos2]), position, functions.indexToCoordinate([pos1, pos2]), piece))
				if self.pieceAt(functions.indexToCoordinate([pos1, pos2])):
					break
			elif stop != Stop.never:
				for i in self.pieces:
					if functions.coordinateToIndex(i.position) == [pos1, pos2]:
						if stop == Stop.capture_piece:
							if i.color == color:
								break
							capture = True
						elif stop == Stop.no_capture:
							break
				else:
					moves.append(Move("B" + ("x" if capture else "") + functions.indexToCoordinate([pos1, pos2]), position, functions.indexToCoordinate([pos1, pos2]), piece, is_capture=capture))
					if capture:
						break
					continue
				break
			else:
				moves.append(Move("B" + functions.indexToCoordinate([pos1, pos2]), position, functions.indexToCoordinate([pos1, pos2]), piece))
		capture, (pos1, pos2) = False, functions.coordinateToIndex(position)
		while pos1 != 7 and pos2 != 0:
			pos1, pos2 = pos1 + 1, pos2 - 1
			if stop == Stop.piece:
				moves.append(Move("B" + functions.indexToCoordinate([pos1, pos2]), position, functions.indexToCoordinate([pos1, pos2]), piece))
				if self.pieceAt(functions.indexToCoordinate([pos1, pos2])):
					break
			elif stop != Stop.never:
				for i in self.pieces:
					if functions.coordinateToIndex(i.position) == [pos1, pos2]:
						if stop == Stop.capture_piece:
							if i.color == color:
								break
							capture = True
						elif stop == Stop.no_capture:
							break
				else:
					moves.append(Move("B" + ("x" if capture else "") + functions.indexToCoordinate([pos1, pos2]), position, functions.indexToCoordinate([pos1, pos2]), piece, is_capture=capture))
					if capture:
						break
					continue
				break
			else:
				moves.append(Move("B" + functions.indexToCoordinate([pos1, pos2]), position, functions.indexToCoordinate([pos1, pos2]), piece))
		return moves

	def generateRookMoves(self, position, color, stop=Stop.capture_piece, piece=None):
		"""
		:type position: str
		:type color: str
		:type stop: str
		:type piece: Piece | None
		:return: List[Move]
		"""
		moves = []
		capture = False
		for x in reversed(range(functions.coordinateToIndex(position)[0])):
			if stop == Stop.piece:
				moves.append(Move("R" + functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]]), position, functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]]), piece))
				if self.pieceAt(functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]])):
					break
			elif stop != Stop.never:
				for y in self.pieces:
					if functions.coordinateToIndex(y.position) == [x, functions.coordinateToIndex(position)[1]]:
						if y.color == color or stop == Stop.no_capture:
							break
						capture = True
				else:
					moves.append(Move("R" + ("x" if capture else "") + functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]]), position, functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]]), piece, is_capture=capture))
					if capture:
						break
					continue
				break
			else:
				moves.append(Move("R" + functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]]), position, functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]]), piece))
		capture = False
		for x in reversed(range(functions.coordinateToIndex(position)[1])):
			if stop == Stop.piece:
				moves.append(Move("R" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x]), piece))
				if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x])):
					break
			elif stop != Stop.never:
				for y in self.pieces:
					if functions.coordinateToIndex(y.position) == [functions.coordinateToIndex(position)[0], x]:
						if y.color == color or stop == Stop.no_capture:
							break
						capture = True
				else:
					moves.append(Move("R" + ("x" if capture else "") + functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x]), piece, is_capture=capture))
					if capture:
						break
					continue
				break
			else:
				moves.append(Move("R" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x]), piece))
		capture = False
		for x in range(functions.coordinateToIndex(position)[0] + 1, 8):
			if stop == Stop.piece:
				moves.append(Move("R" + functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]]), position, functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]]), piece))
				if self.pieceAt(functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]])):
					break
			elif stop != Stop.never:
				for y in self.pieces:
					if functions.coordinateToIndex(y.position) == [x, functions.coordinateToIndex(position)[1]]:
						if y.color == color or stop == Stop.no_capture:
							break
						capture = True
				else:
					moves.append(Move("R" + ("x" if capture else "") + functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]]), position, functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]]), piece, is_capture=capture))
					if capture:
						break
					continue
				break
			else:
				moves.append(Move("R" + functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]]), position, functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]]), piece))
		capture = False
		for x in range(functions.coordinateToIndex(position)[1] + 1, 8):
			if stop == Stop.piece:
				moves.append(Move("R" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x]), piece))
				if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x])):
					break
			elif stop != Stop.never:
				for y in self.pieces:
					if functions.coordinateToIndex(y.position) == [functions.coordinateToIndex(position)[0], x]:
						if y.color == color or stop == Stop.no_capture:
							break
						capture = True
				else:
					moves.append(Move("R" + ("x" if capture else "") + functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x]), piece, is_capture=capture))
					if capture:
						break
					continue
				break
			else:
				moves.append(Move("R" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x]), piece))
		return moves

	def generateQueenMoves(self, position, color, stop=Stop.capture_piece, piece=None):
		"""
		:type position: str
		:type color: str
		:type stop: str
		:type piece: Piece | None
		:return: List[Move]
		"""
		moves = []
		# Diagonal moves
		capture, (pos1, pos2), piece_found = False, functions.coordinateToIndex(position), 0
		while pos1 != 0 and pos2 != 0:
			pos1, pos2 = pos1 - 1, pos2 - 1
			if stop == Stop.piece:
				moves.append(Move("Q" + functions.indexToCoordinate([pos1, pos2]), position, functions.indexToCoordinate([pos1, pos2]), piece))
				if self.pieceAt(functions.indexToCoordinate([pos1, pos2])):
					break
			elif stop != Stop.never:
				for i in self.pieces:
					if functions.coordinateToIndex(i.position) == [pos1, pos2]:
						if stop == Stop.capture_piece:
							if i.color == color:
								break
							capture = True
						elif stop == Stop.no_capture:
							break
				else:
					moves.append(Move("Q" + ("x" if capture else "") + functions.indexToCoordinate([pos1, pos2]), position, functions.indexToCoordinate([pos1, pos2]), piece, is_capture=capture))
					if capture:
						break
					continue
				break
			else:
				moves.append(Move("Q" + functions.indexToCoordinate([pos1, pos2]), position, functions.indexToCoordinate([pos1, pos2]), piece))
		capture, (pos1, pos2) = False, functions.coordinateToIndex(position)
		while pos1 != 7 and pos2 != 7:
			pos1, pos2 = pos1 + 1, pos2 + 1
			if stop == Stop.piece:
				moves.append(Move("Q" + functions.indexToCoordinate([pos1, pos2]), position, functions.indexToCoordinate([pos1, pos2]), piece))
				if self.pieceAt(functions.indexToCoordinate([pos1, pos2])):
					break
			elif stop != Stop.never:
				for i in self.pieces:
					if functions.coordinateToIndex(i.position) == [pos1, pos2]:
						if stop == Stop.capture_piece:
							if i.color == color:
								break
							capture = True
						elif stop == Stop.no_capture:
							break
				else:
					moves.append(Move("Q" + ("x" if capture else "") + functions.indexToCoordinate([pos1, pos2]), position, functions.indexToCoordinate([pos1, pos2]), piece, is_capture=capture))
					if capture:
						break
					continue
				break
			else:
				moves.append(Move("Q" + functions.indexToCoordinate([pos1, pos2]), position, functions.indexToCoordinate([pos1, pos2]), piece))
		capture, (pos1, pos2) = False, functions.coordinateToIndex(position)
		while pos1 != 0 and pos2 != 7:
			pos1, pos2 = pos1 - 1, pos2 + 1
			if stop == Stop.piece:
				moves.append(Move("Q" + functions.indexToCoordinate([pos1, pos2]), position, functions.indexToCoordinate([pos1, pos2]), piece))
				if self.pieceAt(functions.indexToCoordinate([pos1, pos2])):
					break
			elif stop != Stop.never:
				for i in self.pieces:
					if functions.coordinateToIndex(i.position) == [pos1, pos2]:
						if stop == Stop.capture_piece:
							if i.color == color:
								break
							capture = True
						elif stop == Stop.no_capture:
							break
				else:
					moves.append(Move("Q" + ("x" if capture else "") + functions.indexToCoordinate([pos1, pos2]), position, functions.indexToCoordinate([pos1, pos2]), piece, is_capture=capture))
					if capture:
						break
					continue
				break
			else:
				moves.append(Move("Q" + functions.indexToCoordinate([pos1, pos2]), position, functions.indexToCoordinate([pos1, pos2]), piece))
		capture, (pos1, pos2) = False, functions.coordinateToIndex(position)
		while pos1 != 7 and pos2 != 0:
			pos1, pos2 = pos1 + 1, pos2 - 1
			if stop == Stop.piece:
				moves.append(Move("Q" + functions.indexToCoordinate([pos1, pos2]), position, functions.indexToCoordinate([pos1, pos2]), piece))
				if self.pieceAt(functions.indexToCoordinate([pos1, pos2])):
					break
			elif stop != Stop.never:
				for i in self.pieces:
					if functions.coordinateToIndex(i.position) == [pos1, pos2]:
						if stop == Stop.capture_piece:
							if i.color == color:
								break
							capture = True
						elif stop == Stop.no_capture:
							break
				else:
					moves.append(Move("Q" + ("x" if capture else "") + functions.indexToCoordinate([pos1, pos2]), position, functions.indexToCoordinate([pos1, pos2]), piece, is_capture=capture))
					if capture:
						break
					continue
				break
			else:
				moves.append(Move("Q" + functions.indexToCoordinate([pos1, pos2]), position, functions.indexToCoordinate([pos1, pos2]), piece))
		# Straight moves
		capture = False
		for x in reversed(range(functions.coordinateToIndex(position)[0])):
			if stop == Stop.piece:
				moves.append(Move("Q" + functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]]), position, functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]]), piece))
				if self.pieceAt(functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]])):
					break
			elif stop != Stop.never:
				for y in self.pieces:
					if functions.coordinateToIndex(y.position) == [x, functions.coordinateToIndex(position)[1]]:
						if y.color == color or stop == Stop.no_capture:
							break
						capture = True
				else:
					moves.append(Move("Q" + ("x" if capture else "") + functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]]), position, functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]]), piece, is_capture=capture))
					if capture:
						break
					continue
				break
			else:
				moves.append(Move("Q" + functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]]), position, functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]]), piece))
		capture = False
		for x in reversed(range(functions.coordinateToIndex(position)[1])):
			if stop == Stop.piece:
				moves.append(Move("Q" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x]), piece))
				if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x])):
					break
			elif stop != Stop.never:
				for y in self.pieces:
					if functions.coordinateToIndex(y.position) == [functions.coordinateToIndex(position)[0], x]:
						if y.color == color or stop == Stop.no_capture:
							break
						capture = True
				else:
					moves.append(Move("Q" + ("x" if capture else "") + functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x]), piece, is_capture=capture))
					if capture:
						break
					continue
				break
			else:
				moves.append(Move("Q" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x]), piece))
		capture = False
		for x in range(functions.coordinateToIndex(position)[0] + 1, 8):
			if stop == Stop.piece:
				moves.append(Move("Q" + functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]]), position, functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]]), piece))
				if self.pieceAt(functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]])):
					break
			elif stop != Stop.never:
				for y in self.pieces:
					if functions.coordinateToIndex(y.position) == [x, functions.coordinateToIndex(position)[1]]:
						if y.color == color or stop == Stop.no_capture:
							break
						capture = True
				else:
					moves.append(Move("Q" + ("x" if capture else "") + functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]]), position, functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]]), piece, is_capture=capture))
					if capture:
						break
					continue
				break
			else:
				moves.append(Move("Q" + functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]]), position, functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]]), piece))
		capture = False
		for x in range(functions.coordinateToIndex(position)[1] + 1, 8):
			if stop == Stop.piece:
				moves.append(Move("Q" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x]), piece))
				if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x])):
					break
			elif stop != Stop.never:
				for y in self.pieces:
					if functions.coordinateToIndex(y.position) == [functions.coordinateToIndex(position)[0], x]:
						if y.color == color or stop == Stop.no_capture:
							break
						capture = True
				else:
					moves.append(Move("Q" + ("x" if capture else "") + functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x]), piece, is_capture=capture))
					if capture:
						break
					continue
				break
			else:
				moves.append(Move("Q" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x]), piece))
		return moves

	def generateKingMoves(self, position, color, piece=None):
		"""
		:type position: str
		:type color: str
		:type piece: Piece | None
		:return: List[Move]
		"""
		if piece is None:
			piece = self.pieceAt(position)
		
		moves = []
		if position[0] != "h" and position[1] != "1":
			if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 1])):
				valid = not self.protectors(self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 1])))
			else:
				valid = not self.attackers(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 1]), Color.invert(color))
			if valid:
				if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 1])):
					if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 1])).color != color:
						moves.append(Move(name="Kx" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 1]), old_position=position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 1]), piece=piece, is_capture=True))
				else:
					moves.append(Move(name="K" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 1]), old_position=position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 1]), piece=piece))
		if position[0] != "a" and position[1] != "8":
			if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 1])):
				valid = not self.protectors(self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 1])))
			else:
				valid = not self.attackers(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 1]), Color.invert(color))
			if valid:
				if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 1])):
					if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 1])).color != color:
						moves.append(Move(name="Kx" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 1]), old_position=position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 1]), piece=piece, is_capture=True))
				else:
					moves.append(Move(name="K" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 1]), old_position=position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 1]), piece=piece))
		if position[0] != "a" and position[1] != "1":
			if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 1])):
				valid = not self.protectors(self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 1])))
			else:
				valid = not self.attackers(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 1]), Color.invert(color))
			if valid:
				if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 1])):
					if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 1])).color != color:
						moves.append(Move(name="Kx" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 1]), old_position=position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 1]), piece=piece, is_capture=True))
				else:
					moves.append(Move(name="K" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 1]), old_position=position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 1]), piece=piece))
		if position[0] != "h" and position[1] != "8":
			if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 1])):
				valid = not self.protectors(self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 1])))
			else:
				valid = not self.attackers(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 1]), Color.invert(color))
			if valid:
				if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 1])):
					if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 1])).color != color:
						moves.append(Move(name="Kx" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 1]), old_position=position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 1]), piece=piece, is_capture=True))
				else:
					moves.append(Move(name="K" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 1]), old_position=position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 1]), piece=piece))
		if position[0] != "a":
			if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0], functions.coordinateToIndex(position)[1] - 1])):
				valid = not self.protectors(self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0], functions.coordinateToIndex(position)[1] - 1])))
			else:
				valid = not self.attackers(functions.indexToCoordinate([functions.coordinateToIndex(position)[0], functions.coordinateToIndex(position)[1] - 1]), Color.invert(color))
			if valid:
				if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0], functions.coordinateToIndex(position)[1] - 1])):
					if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0], functions.coordinateToIndex(position)[1] - 1])).color != color:
						moves.append(Move(name="Kx" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0], functions.coordinateToIndex(position)[1] - 1]), old_position=position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(position)[0], functions.coordinateToIndex(position)[1] - 1]), piece=piece, is_capture=True))
				else:
					moves.append(Move(name="K" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0], functions.coordinateToIndex(position)[1] - 1]), old_position=position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(position)[0], functions.coordinateToIndex(position)[1] - 1]), piece=piece))
		if position[0] != "h":
			if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0], functions.coordinateToIndex(position)[1] + 1])):
				valid = not self.protectors(self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0], functions.coordinateToIndex(position)[1] + 1])))
			else:
				valid = not self.attackers(functions.indexToCoordinate([functions.coordinateToIndex(position)[0], functions.coordinateToIndex(position)[1] + 1]), Color.invert(color))
			if valid:
				if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0], functions.coordinateToIndex(position)[1] + 1])):
					if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0], functions.coordinateToIndex(position)[1] + 1])).color != color:
						moves.append(Move(name="Kx" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0], functions.coordinateToIndex(position)[1] + 1]), old_position=position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(position)[0], functions.coordinateToIndex(position)[1] + 1]), piece=piece, is_capture=True))
				else:
					moves.append(Move(name="K" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0], functions.coordinateToIndex(position)[1] + 1]), old_position=position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(position)[0], functions.coordinateToIndex(position)[1] + 1]), piece=piece))
		if position[1] != "1":
			if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1]])):
				valid = not self.protectors(self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1]])))
			else:
				valid = not self.attackers(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1]]), Color.invert(color))
			if valid:
				if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1]])):
					if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1]])).color != color:
						moves.append(Move(name="Kx" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1]]), old_position=position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1]]), piece=piece, is_capture=True))
				else:
					moves.append(Move(name="K" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1]]), old_position=position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1]]), piece=piece))
		if position[1] != "8":
			if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1]])):
				valid = not self.protectors(self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1]])))
			else:
				valid = not self.attackers(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1]]), Color.invert(color))
			if valid:
				if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1]])):
					if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1]])).color != color:
						moves.append(Move(name="Kx" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1]]), old_position=position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1]]), piece=piece, is_capture=True))
				else:
					moves.append(Move(name="K" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1]]), old_position=position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1]]), piece=piece))
		return moves

	def generateKingCastles(self, position, piece=None):
		"""
		:type position: str
		:type piece: Piece | None
		:return: List[Move]
		"""
		if piece is None:
			piece = self.pieceAt(position)

		moves = []
		if self.castling_rights is not None and not piece.moved and self.in_check != piece.color:
			valid = True
			for x in self.pieceType(PieceEnum.rook, piece.color):
				if x.position[1] == position[1] and not x.moved:
					if functions.coordinateToIndex(position)[1] < functions.coordinateToIndex(x.position)[1] and ((piece.color == "white" and "K" in self.castling_rights) or (piece.color == "black" and "k" in self.castling_rights)):
						for y in range(functions.coordinateToIndex(position)[1] + 1, functions.coordinateToIndex(x.position)[1]):
							if self.attackers(functions.indexToCoordinate([functions.coordinateToIndex(position)[0], y]), Color.invert(piece.color)) or self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0], y])):
								valid = False
								break
						if valid:
							moves.append(Move("O-O", position, "g" + position[1], piece=piece, castle=Castle.kingside, castle_rook=x))
						else:
							valid = True
							continue
					elif functions.coordinateToIndex(position)[1] > functions.coordinateToIndex(x.position)[1] and ((piece.color == "white" and "Q" in self.castling_rights) or (piece.color == "black" and "q" in self.castling_rights)):
						for y in range(functions.coordinateToIndex(x.position)[1] + 1, functions.coordinateToIndex(position)[1]):
							if self.attackers(functions.indexToCoordinate([functions.coordinateToIndex(position)[0], y]), Color.invert(piece.color)) or self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0], y])):
								valid = False
								break
						if valid:
							moves.append(Move("O-O-O", position, "c" + position[1], piece=piece, castle=Castle.queenside, castle_rook=x))
						else:
							valid = True
							continue

		return moves
	
	def minimax_evaluation(self, depth, alpha=float("-inf"), beta=float("inf"), maximizing=True, color=Color.current):
		"""
		:type depth: int
		:type alpha: float
		:type beta: float
		:type maximizing: bool
		:type color: str
		:return: dict
		"""
		if color == Color.current:
			color = self.turn
		move = None

		if depth == 0 or self.game_over:
			return {"move": move, "evaluation": self.evaluate() if color == Color.white else -self.evaluate()}

		base = float("-inf" if maximizing else "inf")
		for i in self.legal_moves():
			self.move(i)
			evaluation = self.minimax_evaluation(depth - 1, alpha=alpha, beta=beta, maximizing=not maximizing, color=color)["evaluation"]
			self.takeback()
			if (maximizing and base < evaluation) or (not maximizing and base > evaluation):
				base = evaluation
				move = i
			if (maximizing and beta <= max(alpha, evaluation)) or (not maximizing and alpha >= min(beta, evaluation)):
				break
		return {"move": move, "evaluation": base}

	def __str__(self):
		"""
		:return: str
		"""
		return "Chess Game with FEN " + self.FEN()

	def __lt__(self, other):
		"""
		:type other: Game
		:return: bool
		"""
		return self.totalMaterial() < other.totalMaterial()

	def __le__(self, other):
		"""
		:type other: Game
		:return: bool
		"""
		return self.totalMaterial() <= other.totalMaterial()

	def __contains__(self, obj):
		"""
		:type obj: Any
		:return: bool
		"""
		if isinstance(obj, Piece):
			return self.squares_hashtable[obj.position] == obj
		if isinstance(obj, Square):
			return vars(obj) in map(vars, self.squares)

		return False

	def __unicode__(self):
		"""
		:return: str
		"""
		return self.visualized()

	def __eq__(self, other):
		"""
		:type other: Game
		:return: bool
		"""
		return self.FEN() == other.FEN()

	__add__ = __radd__ = __sub__ = __rsub__ = __mul__ = __rmul__ = __div__ = __rdiv__ = __truediv__ = __rtruediv__ = __floordiv__ = __rfloordiv__ = __mod__ = __rmod__ = __divmod__ = __rdivmod__ = __pow__ = __rpow__ = __lshift__ = __rlshift__ = __rshift__ = __rrshift__ = __and__ = __rand__ = __or__ = __ror__ = __xor__ = __rxor__ = __iadd__ = __isub__ = __imul__ = __idiv__ = __itruediv__ = __ifloordiv__ = __imod__ = __ipow__ = __iand__ = __ior__ = __ixor__ = __ilshift__ = __irshift__ = __neg__ = __pos__ = __abs__ = __invert__ = __int__ = __long__ = __float__ = __complex__ = __oct__ = __hex__ = __coerce__ = lambda self, *args: self.error(ArithmeticError("Cannot perform arithmetic operations on Game object"))

	__getitem__ = __setitem__ = __delitem__ = __getslice__ = __setslice__ = __delslice__ = lambda self, *args: self.error(IndexError("Cannot perform operation on Game object"))


class Antichess(Game):
	class AntichessPiece(Piece):
		def __init__(self, position, piece_type, color, board):
			super(Antichess.AntichessPiece, self).__init__(position, piece_type, color, board)

		def moves(self, show_data=False, evaluate_checks=False):
			if self.board.game_over:
				return []
			for x in self.board.pieces:
				if x != self:
					for y in x.moves(show_data=False, evaluate_checks=False):
						if "x" in y:
							return []
			moves = []
			if self.piece_type == PieceEnum.pawn:  # Pawn moves
				moves.extend(self.board.generatePawnCaptures(self.position, self.color, piece=self))
				moves.extend(self.board.generatePawnMoves(self.position, self.color, piece=self))
			elif self.piece_type == PieceEnum.knight:  # Knight moves
				moves.extend(self.board.generateKnightMoves(self.position, self.color, piece=self))
			elif self.piece_type == PieceEnum.bishop:  # Bishop moves
				moves.extend(self.board.generateBishopMoves(self.position, self.color, piece=self))
			if self.piece_type == PieceEnum.rook:  # Rook moves
				moves.extend(self.board.generateRookMoves(self.position, self.color, piece=self))
			elif self.piece_type == PieceEnum.queen:  # Queen moves
				moves.extend(self.board.generateQueenMoves(self.position, self.color, piece=self))
			elif self.piece_type == PieceEnum.king:
				moves.extend(self.board.generateKingMoves(self.position, self.color, piece=self))
			captures, non_captures = [], []
			for i in moves:
				if i.is_capture:
					if show_data:
						captures.append(i)
					else:
						captures.append(i.name)
				else:
					if not captures:
						if show_data:
							non_captures.append(i)
						else:
							non_captures.append(i.name)
			if captures:
				return captures
			return non_captures

	def __init__(self, fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", raise_errors=True, evaluate_openings=False, pieces=Piece):
		super(Antichess, self).__init__(fen=fen, raise_errors=raise_errors, evaluate_openings=evaluate_openings, pieces=pieces)
		self.properties["promotions"]["K"] = PieceEnum.king

	def legal_moves(self, show_data=False, color=Color.current, evaluate_checks=True, evaluate_checkmate=True, piece_type=PieceEnum.all()):
		moves = super(Antichess, self).legal_moves(show_data=True, color=color, evaluate_checks=False, evaluate_checkmate=False, piece_type=piece_type)
		captures, non_captures = [], []
		for i in moves:
			if i.is_capture:
				if show_data:
					captures.append(i)
				else:
					captures.append(i.name)
			else:
				if not captures:
					if show_data:
						non_captures.append(i)
					else:
						non_captures.append(i.name)

		if captures:
			return captures
		return non_captures

	def move(self, move, evaluate_checks=True, evaluate_opening=True, evaluate_move_checks=True, evaluate_move_checkmate=True):
		move = super(Antichess, self).move(move, evaluate_checks=False, evaluate_opening=evaluate_opening, evaluate_move_checks=False, evaluate_move_checkmate=False)
		if self.in_check:
			self.in_check = False

		if not self.legal_moves():
			self.game_over = True
			self.tags["Result"] = "1-0" if self.turn == Color.white else "0-1"
			if self.drawn:
				self.drawn = False
				self.is_stalemate = False

		return move

	def generateKingMoves(self, position, color, piece=None):
		moves = []
		if position[0] != "h" and position[1] != "1":
			if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 1])):
				if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 1])).color != color:
					moves.append(Move(name="Kx" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 1]), old_position=position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 1]), piece=piece, is_capture=True))
			else:
				moves.append(Move(name="K" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 1]), old_position=position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 1]), piece=piece))
		if position[0] != "a" and position[1] != "8":
			if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 1])):
				if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 1])).color != color:
					moves.append(Move(name="Kx" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 1]), old_position=position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 1]), piece=piece, is_capture=True))
			else:
				moves.append(Move(name="K" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 1]), old_position=position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 1]), piece=piece))
		if position[0] != "a" and position[1] != "1":
			if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 1])):
				if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 1])).color != color:
					moves.append(Move(name="Kx" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 1]), old_position=position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 1]), piece=piece, is_capture=True))
			else:
				moves.append(Move(name="K" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 1]), old_position=position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 1]), piece=piece))
		if position[0] != "h" and position[1] != "8":
			if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 1])):
				if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 1])).color != color:
					moves.append(Move(name="Kx" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 1]), old_position=position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 1]), piece=piece, is_capture=True))
			else:
				moves.append(Move(name="K" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 1]), old_position=position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 1]), piece=piece))
		if position[0] != "a":
			if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0], functions.coordinateToIndex(position)[1] - 1])):
				if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0], functions.coordinateToIndex(position)[1] - 1])).color != color:
					moves.append(Move(name="Kx" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0], functions.coordinateToIndex(position)[1] - 1]), old_position=position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(position)[0], functions.coordinateToIndex(position)[1] - 1]), piece=piece, is_capture=True))
			else:
				moves.append(Move(name="K" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0], functions.coordinateToIndex(position)[1] - 1]), old_position=position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(position)[0], functions.coordinateToIndex(position)[1] - 1]), piece=piece))
		if position[0] != "h":
			if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0], functions.coordinateToIndex(position)[1] + 1])):
				if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0], functions.coordinateToIndex(position)[1] + 1])).color != color:
					moves.append(Move(name="Kx" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0], functions.coordinateToIndex(position)[1] + 1]), old_position=position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(position)[0], functions.coordinateToIndex(position)[1] + 1]), piece=piece, is_capture=True))
			else:
				moves.append(Move(name="K" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0], functions.coordinateToIndex(position)[1] + 1]), old_position=position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(position)[0], functions.coordinateToIndex(position)[1] + 1]), piece=piece))
		if position[1] != "1":
			if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1]])):
				if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1]])).color != color:
					moves.append(Move(name="Kx" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1]]), old_position=position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1]]), piece=piece, is_capture=True))
			else:
				moves.append(Move(name="K" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1]]), old_position=position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1]]), piece=piece))
		if position[1] != "8":
			if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1]])):
				if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1]])).color != color:
					moves.append(Move(name="Kx" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1]]), old_position=position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1]]), piece=piece, is_capture=True))
			else:
				moves.append(Move(name="K" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1]]), old_position=position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1]]), piece=piece))
		return moves

	def generateKingCastles(self, *args, **kwargs):
		return []


class ThreeCheck(Game):
	def __init__(self, fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", raise_errors=True, evaluate_openings=False, pieces=Piece):
		super(ThreeCheck, self).__init__(fen=fen, raise_errors=raise_errors, evaluate_openings=evaluate_openings, pieces=pieces)
		self.white_checks = self.black_checks = 0

	def move(self, move, evaluate_checks=True, evaluate_opening=True, evaluate_move_checks=True, evaluate_move_checkmate=True):
		move = super(ThreeCheck, self).move(move=move, evaluate_checks=evaluate_checks, evaluate_opening=evaluate_opening, evaluate_move_checks=evaluate_move_checks, evaluate_move_checkmate=evaluate_move_checkmate)
		if move.check:
			if self.turn == Color.white:
				self.black_checks += 1
			else:
				self.white_checks += 1

			if self.white_checks == 3:
				self.game_over = True
				self.tags["Result"] = "1-0"
			elif self.black_checks == 3:
				self.game_over = True
				self.tags["Result"] = "0-1"
		return move


class KingOfTheHill(Game):
	def __init__(self, fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", raise_errors=True, evaluate_openings=False, pieces=Piece):
		super(KingOfTheHill, self).__init__(fen=fen, raise_errors=raise_errors, evaluate_openings=evaluate_openings, pieces=pieces)

	def move(self, move, evaluate_checks=True, evaluate_opening=True, evaluate_move_checks=True, evaluate_move_checkmate=True):
		move = super(KingOfTheHill, self).move(move=move, evaluate_checks=evaluate_checks, evaluate_opening=evaluate_opening, evaluate_move_checks=evaluate_move_checks, evaluate_move_checkmate=evaluate_move_checkmate)
		if self.white_king.position in ["d4", "d5", "e4", "e5"]:
			self.game_over = True
			self.tags["Result"] = "1-0"
		elif self.black_king.position in ["d4", "d5", "e4", "e5"]:
			self.game_over = True
			self.tags["Result"] = "0-1"
		
		return move


class RacingKings(Game):
	class RacingKingsPiece(Piece):
		def __init__(self, position, piece_type, color, board):
			super(RacingKings.RacingKingsPiece, self).__init__(position, piece_type, color, board)
		
		def moves(self, show_data=False, evaluate_checks=True):
			return [(i if show_data else i.name) for i in super(RacingKings.RacingKingsPiece, self).moves(show_data=True, evaluate_checks=evaluate_checks) if not i.check]

	def __init__(self, fen="8/8/8/8/8/8/krbnNBRK/qrbnNBRQ w - - 0 1", raise_errors=True, evaluate_openings=False, pieces=RacingKingsPiece):
		super(RacingKings, self).__init__(fen=fen, raise_errors=raise_errors, evaluate_openings=evaluate_openings, pieces=pieces)
	
	def move(self, move, evaluate_checks=True, evaluate_opening=True, evaluate_move_checks=True, evaluate_move_checkmate=True):
		move = super(RacingKings, self).move(move=move, evaluate_checks=evaluate_checks, evaluate_opening=evaluate_opening, evaluate_move_checks=evaluate_move_checks, evaluate_move_checkmate=evaluate_move_checkmate)
		if self.white_king.position[1] == "8":
			self.game_over = True
			self.tags["Result"] = "1-0"
		elif self.white_king.position[1] == "8":
			self.game_over = True
			self.tags["Result"] = "1-0"
		return move


class Atomic(Game):
	class AtomicPiece(Piece):
		def __init__(self, position, piece_type, color, board):
			super(Atomic.AtomicPiece, self).__init__(position, piece_type, color, board)
		
		def moves(self, show_data=False, evaluate_checks=True):
			return [(i.name if not show_data else i) for i in super(Atomic.AtomicPiece, self).moves(show_data=True, evaluate_checks=evaluate_checks) if not i.is_capture or (self.board.getKing(self.color).position not in self.board.generateExplosionRadius(i.new_position))]
	
	def __init__(self, fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", raise_errors=True, evaluate_openings=False, pieces=AtomicPiece):
		super(Atomic, self).__init__(fen=fen, raise_errors=raise_errors, evaluate_openings=evaluate_openings, pieces=pieces)
		
	@staticmethod
	def generateExplosionRadius(coordinate):
		"""
		:type coordinate: str
		:return: List[str]
		"""
		if coordinate[0] == "a":
			if coordinate[1] == "1":
				return ["a" + str(int(coordinate[1]) + 1), "b" + str(int(coordinate[1]) + 1), "b" + coordinate[1], coordinate]
			elif coordinate[1] == "8":
				return ["a" + str(int(coordinate[1]) - 1), "b" + str(int(coordinate[1]) - 1), "b" + coordinate[1], coordinate]
			else:
				return ["a" + str(int(coordinate[1]) + 1), "a" + str(int(coordinate[1]) - 1), "b" + str(int(coordinate[1]) + 1), "b" + str(int(coordinate[1]) - 1), "b" + coordinate[1], coordinate]
		if coordinate[0] == "h":
			if coordinate[1] == "1":
				return ["h" + str(int(coordinate[1]) + 1), "g" + str(int(coordinate[1]) + 1), "g" + coordinate[1], coordinate]
			elif coordinate[1] == "8":
				return ["h" + str(int(coordinate[1]) - 1), "g" + str(int(coordinate[1]) - 1), "g" + coordinate[1], coordinate]
			else:
				return ["h" + str(int(coordinate[1]) + 1), "h" + str(int(coordinate[1]) - 1), "g" + str(int(coordinate[1]) + 1), "g" + str(int(coordinate[1]) - 1), "g" + coordinate[1], coordinate]
		if coordinate[1] == "1":
			return [coordinate[0] + str(int(coordinate[1]) + 1), functions.indexToCoordinate([functions.coordinateToIndex(coordinate)[0], functions.coordinateToIndex(coordinate)[1] + 1])[0] + str(int(coordinate[1]) + 1), functions.indexToCoordinate([functions.coordinateToIndex(coordinate)[0], functions.coordinateToIndex(coordinate)[1] - 1])[0] + str(int(coordinate[1]) + 1), functions.indexToCoordinate([functions.coordinateToIndex(coordinate)[0], functions.coordinateToIndex(coordinate)[1] - 1])[0] + coordinate[1], functions.indexToCoordinate([functions.coordinateToIndex(coordinate)[0], functions.coordinateToIndex(coordinate)[1] + 1])[0] + coordinate[1], coordinate]
		if coordinate[1] == "8":
			return [coordinate[0] + str(int(coordinate[1]) - 1), functions.indexToCoordinate([functions.coordinateToIndex(coordinate)[0], functions.coordinateToIndex(coordinate)[1] + 1])[0] + str(int(coordinate[1]) - 1), functions.indexToCoordinate([functions.coordinateToIndex(coordinate)[0], functions.coordinateToIndex(coordinate)[1] - 1])[0] + str(int(coordinate[1]) - 1), functions.indexToCoordinate([functions.coordinateToIndex(coordinate)[0], functions.coordinateToIndex(coordinate)[1] - 1])[0] + coordinate[1], functions.indexToCoordinate([functions.coordinateToIndex(coordinate)[0], functions.coordinateToIndex(coordinate)[1] + 1])[0] + coordinate[1], coordinate]
		return [coordinate[0] + str(int(coordinate[1]) + 1), coordinate[0] + str(int(coordinate[1]) - 1), functions.indexToCoordinate([functions.coordinateToIndex(coordinate)[0], functions.coordinateToIndex(coordinate)[1] + 1])[0] + str(int(coordinate[1]) + 1), functions.indexToCoordinate([functions.coordinateToIndex(coordinate)[0], functions.coordinateToIndex(coordinate)[1] + 1])[0] + str(int(coordinate[1]) - 1), functions.indexToCoordinate([functions.coordinateToIndex(coordinate)[0], functions.coordinateToIndex(coordinate)[1] - 1])[0] + str(int(coordinate[1]) + 1), functions.indexToCoordinate([functions.coordinateToIndex(coordinate)[0], functions.coordinateToIndex(coordinate)[1] - 1])[0] + str(int(coordinate[1]) - 1), functions.indexToCoordinate([functions.coordinateToIndex(coordinate)[0], functions.coordinateToIndex(coordinate)[1] - 1])[0] + coordinate[1], functions.indexToCoordinate([functions.coordinateToIndex(coordinate)[0], functions.coordinateToIndex(coordinate)[1] + 1])[0] + coordinate[1], coordinate]
		
	def move(self, move, evaluate_checks=True, evaluate_opening=True, evaluate_move_checks=True, evaluate_move_checkmate=True):
		move = super(Atomic, self).move(move, evaluate_checks=evaluate_checks, evaluate_opening=evaluate_opening, evaluate_move_checks=evaluate_move_checks, evaluate_move_checkmate=evaluate_move_checkmate)
		if move.is_capture:
			for i in self.generateExplosionRadius(move.new_position):
				if self.pieceAt(i) is not None:
					if self.pieceAt(i).piece_type != PieceEnum.pawn:
						if self.removePiece(i).piece_type == PieceEnum.king:
							self.game_over = True
							self.tags["Result"] = self.turn
		return move
