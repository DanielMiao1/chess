# -*- coding: utf-8 -*-


"""
Imports
"""

import chess.enums
import chess.errors
import chess.openings
import chess.functions

"""
Initialization
"""

try:
	unicode
except NameError:
	unicode = str


"""Main"""


class Square:
	"""A square"""
	def __init__(self, position, board):
		"""Initialize the square"""
		self.position = functions.indexToCoordinate(position)
		self.board = board
		if ((position[0] + position[1]) & 1) == 0:
			self.color = enums.Color.white
		else:
			self.color = enums.Color.black

	def __str__(self):
		return self.color.title() + " square from " + str(self.board)

	def __eq__(self, other):
		return self.position == other.position and isinstance(other, Square)

	def __unicode__(self):
		return self.color.title() + " square"

	__lt__ = __le__ = lambda self, *args: self.error(Exception("Cannot compare squares"))

	__add__ = __radd__ = __sub__ = __rsub__ = __mul__ = __rmul__ = __div__ = __rdiv__ = __truediv__ = __rtruediv__ = __floordiv__ = __rfloordiv__ = __mod__ = __rmod__ = __divmod__ = __rdivmod__ = __pow__ = __rpow__ = __lshift__ = __rlshift__ = __rshift__ = __rrshift__ = __and__ = __rand__ = __or__ = __ror__ = __xor__ = __rxor__ = __iadd__ = __isub__ = __imul__ = __idiv__ = __itruediv__ = __ifloordiv__ = __imod__ = __ipow__ = __iand__ = __ior__ = __ixor__ = __ilshift__ = __irshift__ = __neg__ = __pos__ = __abs__ = __invert__ = __int__ = __long__ = __float__ = __complex__ = __oct__ = __hex__ = __coerce__ = lambda self, *args: self.error(ArithmeticError("Cannot perform arithmetic operations on Square object"))

	__getitem__ = __setitem__ = __delitem__ = __getslice__ = __setslice__ = __delslice__ = __contains__ = lambda self, *args: self.error(IndexError("Cannot perform operation on Square"))


class Piece:
	def __init__(self, position, piece_type, color, board):
		"""Initialize the piece"""
		self.position = position if isinstance(position, str) else functions.indexToCoordinate(position)
		self.piece_type, self.color, self.board = piece_type, color, board
		self.moved = False
		self.en_passant = False

	def moveTo(self, position, override_pieces=True, evaluate_opening=True, evaluate_checks=True):
		"""Move the piece to a position"""
		if self.board.pieceAt(position) and override_pieces:
			self.board.pieces.remove(self.board.pieceAt(position))
			self.board.squares_hashtable[position] = False
		elif not override_pieces and self.board.pieceAt(position):
			self.board.pieceAt(position).position = self.position
		self.board.squares_hashtable[self.position], self.board.squares_hashtable[position] = self.board.squares_hashtable[position], self.board.squares_hashtable[self.position]
		self.position = position
		if evaluate_checks:
			for i in self.moves(show_data=True, evaluate_checks=False):
				if i.new_position == self.board.getKing(enums.Color.invert(self.color)).position:
					self.board.in_check = enums.Color.invert(self.color)
					break
		if evaluate_opening:
			self.board.updateOpening()

	def moves(self, show_data=False, evaluate_checks=True):
		"""Legal moves of the piece"""
		moves = []
		if self.piece_type == enums.Piece.pawn:  # Pawn moves
			moves.extend(self.board.generatePawnCaptures(self.position, self.color, piece=self))
			moves.extend(self.board.generatePawnMoves(self.position, self.color, piece=self))
		elif self.piece_type == enums.Piece.knight:  # Knight moves
			moves.extend(self.board.generateKnightMoves(self.position, self.color, piece=self))
		elif self.piece_type == enums.Piece.bishop:  # Bishop moves
			moves.extend(self.board.generateBishopMoves(self.position, self.color, piece=self))
		if self.piece_type == enums.Piece.rook:  # Rook moves
			moves.extend(self.board.generateRookMoves(self.position, self.color, piece=self))
		elif self.piece_type == enums.Piece.queen:  # Queen moves
			moves.extend(self.board.generateQueenMoves(self.position, self.color, piece=self))
		elif self.piece_type == enums.Piece.king:
			if self.position[0] != "h" and self.position[1] != "1":
				valid = False
				if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] + 1])):
					valid = not self.board.protectors(self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] + 1])))
				else:
					valid = not self.board.attackers(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] + 1]), enums.Color.invert(self.color))
				if valid:
					if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] + 1])):
						if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] + 1])).color != self.color:
							moves.append(enums.Move(name="Kx" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] + 1]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] + 1]), piece=self, is_capture=True))
					else:
						moves.append(enums.Move(name="K" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] + 1]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] + 1]), piece=self))
			if self.position[0] != "a" and self.position[1] != "8":
				valid = False
				if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] - 1])):
					valid = not self.board.protectors(self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] - 1])))
				else:
					valid = not self.board.attackers(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] - 1]), enums.Color.invert(self.color))
				if valid:
					if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] - 1])):
						if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] - 1])).color != self.color:
							moves.append(enums.Move(name="Kx" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] - 1]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] - 1]), piece=self, is_capture=True))
					else:
						moves.append(enums.Move(name="K" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] - 1]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] - 1]), piece=self))
			if self.position[0] != "a" and self.position[1] != "1":
				valid = False
				if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] - 1])):
					valid = not self.board.protectors(self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] - 1])))
				else:
					valid = not self.board.attackers(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] - 1]), enums.Color.invert(self.color))
				if valid:
					if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] - 1])):
						if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] - 1])).color != self.color:
							moves.append(enums.Move(name="Kx" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] - 1]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] - 1]), piece=self, is_capture=True))
					else:
						moves.append(enums.Move(name="K" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] - 1]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] - 1]), piece=self))
			if self.position[0] != "h" and self.position[1] != "8":
				valid = False
				if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] + 1])):
					valid = not self.board.protectors(self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] + 1])))
				else:
					valid = not self.board.attackers(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] + 1]), enums.Color.invert(self.color))
				if valid:
					if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] + 1])):
						if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] + 1])).color != self.color:
							moves.append(enums.Move(name="Kx" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] + 1]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] + 1]), piece=self, is_capture=True))
					else:
						moves.append(enums.Move(name="K" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] + 1]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] + 1]), piece=self))
			if self.position[0] != "a":
				valid = False
				if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], functions.coordinateToIndex(self.position)[1] - 1])):
					valid = not self.board.protectors(self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], functions.coordinateToIndex(self.position)[1] - 1])))
				else:
					valid = not self.board.attackers(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], functions.coordinateToIndex(self.position)[1] - 1]), enums.Color.invert(self.color))
				if valid:
					if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], functions.coordinateToIndex(self.position)[1] - 1])):
						if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], functions.coordinateToIndex(self.position)[1] - 1])).color != self.color:
							moves.append(enums.Move(name="Kx" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], functions.coordinateToIndex(self.position)[1] - 1]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], functions.coordinateToIndex(self.position)[1] - 1]), piece=self, is_capture=True))
					else:
						moves.append(enums.Move(name="K" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], functions.coordinateToIndex(self.position)[1] - 1]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], functions.coordinateToIndex(self.position)[1] - 1]), piece=self))
			if self.position[0] != "h":
				valid = False
				if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], functions.coordinateToIndex(self.position)[1] + 1])):
					valid = not self.board.protectors(self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], functions.coordinateToIndex(self.position)[1] + 1])))
				else:
					valid = not self.board.attackers(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], functions.coordinateToIndex(self.position)[1] + 1]), enums.Color.invert(self.color))
				if valid:
					if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], functions.coordinateToIndex(self.position)[1] + 1])):
						if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], functions.coordinateToIndex(self.position)[1] + 1])).color != self.color:
							moves.append(enums.Move(name="Kx" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], functions.coordinateToIndex(self.position)[1] + 1]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], functions.coordinateToIndex(self.position)[1] + 1]), piece=self, is_capture=True))
					else:
						moves.append(enums.Move(name="K" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], functions.coordinateToIndex(self.position)[1] + 1]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], functions.coordinateToIndex(self.position)[1] + 1]), piece=self))
			if self.position[1] != "1":
				valid = False
				if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1]])):
					valid = not self.board.protectors(self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1]])))
				else:
					valid = not self.board.attackers(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1]]), enums.Color.invert(self.color))
				if valid:
					if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1]])):
						if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1]])).color != self.color:
							moves.append(enums.Move(name="Kx" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1]]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1]]), piece=self, is_capture=True))
					else:
						moves.append(enums.Move(name="K" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1]]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1]]), piece=self))
			if self.position[1] != "8":
				valid = False
				if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1]])):
					valid = not self.board.protectors(self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1]])))
				else:
					valid = not self.board.attackers(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1]]), enums.Color.invert(self.color))
				if valid:
					if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1]])):
						if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1]])).color != self.color:
							moves.append(enums.Move(name="Kx" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1]]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1]]), piece=self, is_capture=True))
					else:
						moves.append(enums.Move(name="K" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1]]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1]]), piece=self))
			# Castling
			if self.board.castling_rights is not None and not self.moved and self.board.in_check != self.color:
				valid = True
				for x in self.board.pieceType(enums.Piece.rook, self.color):
					if x.position[1] == self.position[1] and not x.moved:
						if functions.coordinateToIndex(self.position)[1] < functions.coordinateToIndex(x.position)[1] and ((self.color == "white" and "K" in self.board.castling_rights) or (self.color == "black" and "k" in self.board.castling_rights)):
							for y in range(functions.coordinateToIndex(self.position)[1] + 1, functions.coordinateToIndex(x.position)[1]):
								if self.board.attackers(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], y]), enums.Color.invert(self.color)) or self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], y])):
									valid = False
									break
							if valid:
								moves.append(enums.Move("O-O", self.position, "g" + self.position[1], piece=self, castle=enums.Castle.kingside, castle_rook=x))
							else:
								valid = True
								continue
						elif functions.coordinateToIndex(self.position)[1] > functions.coordinateToIndex(x.position)[1] and ((self.color == "white" and "Q" in self.board.castling_rights) or (self.color == "black" and "q" in self.board.castling_rights)):
							for y in range(functions.coordinateToIndex(x.position)[1] + 1, functions.coordinateToIndex(self.position)[1]):
								if self.board.attackers(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], y]), enums.Color.invert(self.color)) or self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], y])):
									valid = False
									break
							if valid:
								moves.append(enums.Move("O-O-O", self.position, "c" + self.position[1], piece=self, castle=enums.Castle.queenside, castle_rook=x))
							else:
								valid = True
								continue
		if evaluate_checks:
			for x in range(len(moves)):
				for y in self.board.pieces:
					if y.piece_type == enums.Piece.pawn:
						if self.board.getKing(enums.Color.invert(self.color)).position in [z.new_position for z in self.board.generatePawnCaptures(moves[x].new_position, self.color)]:
							moves[x].name += "+"
							moves[x].check = True
							break
					elif y.piece_type == enums.Piece.knight:
						if self.board.getKing(enums.Color.invert(self.color)).position in [z.new_position for z in self.board.generateKnightMoves(moves[x].new_position, self.color)]:
							moves[x].name += "+"
							moves[x].check = True
							break
					elif y.piece_type == enums.Piece.bishop:
						if self.board.getKing(enums.Color.invert(self.color)).position in [z.new_position for z in self.board.generateBishopMoves(moves[x].new_position, self.color)]:
							moves[x].name += "+"
							moves[x].check = True
							break
					elif y.piece_type == enums.Piece.rook:
						if self.board.getKing(enums.Color.invert(self.color)).position in [z.new_position for z in self.board.generateRookMoves(moves[x].new_position, self.color)]:
							moves[x].name += "+"
							moves[x].check = True
							break
					elif y.piece_type == enums.Piece.queen:
						if self.board.getKing(enums.Color.invert(self.color)).position in [z.new_position for z in self.board.generateQueenMoves(moves[x].new_position, self.color)]:
							moves[x].name += "+"
							moves[x].check = True
							break
		return moves if show_data else [i.name for i in moves]

	def __str__(self):
		return self.color.title() + " " + self.piece_type + " at " + self.position

	def __lt__(self, other):
		return enums.Piece.value(self.piece_type) < enums.Piece.value(other)

	def __le__(self, other):
		return enums.Piece.value(self.piece_type) <= enums.Piece.value(other)

	def __eq__(self, other):
		if isinstance(other, Piece):
			return {x: y for x, y in vars(self).items() if x != "board"} == {x: y for x, y in vars(other).items() if x != "board"}
		return False

	def __unicode__(self):
		return self.color.title() + " " + self.piece_type

	__add__ = __radd__ = __sub__ = __rsub__ = __mul__ = __rmul__ = __div__ = __rdiv__ = __truediv__ = __rtruediv__ = __floordiv__ = __rfloordiv__ = __mod__ = __rmod__ = __divmod__ = __rdivmod__ = __pow__ = __rpow__ = __lshift__ = __rlshift__ = __rshift__ = __rrshift__ = __and__ = __rand__ = __or__ = __ror__ = __xor__ = __rxor__ = __iadd__ = __isub__ = __imul__ = __idiv__ = __itruediv__ = __ifloordiv__ = __imod__ = __ipow__ = __iand__ = __ior__ = __ixor__ = __ilshift__ = __irshift__ = __neg__ = __pos__ = __abs__ = __invert__ = __int__ = __long__ = __float__ = __complex__ = __oct__ = __hex__ = __coerce__ = lambda self, *args: self.error(ArithmeticError("Cannot perform arithmetic operations on Piece object"))

	__getitem__ = __setitem__ = __delitem__ = __getslice__ = __setslice__ = __delslice__ = __contains__ = lambda self, *args: self.error(IndexError("Cannot perform operation on Piece"))


class Game:
	"""Game class"""
	def __init__(self, raise_errors=True, fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", evaluate_openings=False):
		"""Initialize"""
		if not functions.FENvalid(fen):
			fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
		self.tags = {"Result": "*"}
		self.opening = ""  # Opening
		self.evaluate_openings = evaluate_openings
		self.squares, self.pieces = [], []  # Pieces and squares
		self.squares_hashtable = {(x + str(y)): False for x in "abcdefgh" for y in range(1, 9)}  # Squares hashtable
		self.in_check = False  # False if neither side is in check, enums.Color.white if white is in check, otherwise enums.Color.black if black is in check
		self.checking_piece = None  # The piece checking a king, or None
		self.white_king = self.black_king = None
		# Append squares
		for x in range(8):
			self.squares.append([Square([x, y], self) for y in range(8)])
		self.raise_errors = raise_errors  # Raise errors
		# Load FEN-specific values
		self.loadFEN(fen, evaluate_opening=fen != "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

	def loadFEN(self, fen, evaluate_opening=True):
		"""Load/Reload with the specified FEN. Returns True if the FEN loaded successfully, otherwise False."""
		self.move_list, self.raw_move_list = "", []  # Move lists
		if not functions.FENvalid(fen):
			self.error(errors.InvalidFEN(fen))
			return False
		self.starting_fen = fen  # Set the starting FEN
		# Reset self.pieces
		if self.pieces:
			self.pieces = []
		self.captured_piece = sum([int(not unicode(y).isnumeric()) for x in fen.split(" ")[0].split("/") for y in x]) < 32  # If a piece has been captured
		self.turn = enums.Color.white if fen.split(" ")[-5].lower() == "w" else enums.Color.black  # The side to move
		self.half_moves = int(fen.split(" ")[-2])  # Halfmove clock
		self.full_moves = int(fen.split(" ")[-1])  # Fullmove clock
		self.castling_rights = fen.split(" ")[2] if fen.split(" ")[2] != "-" else None  # Castling rights
		self.en_passant_positions = fen.split(" ")[3] if fen.split(" ")[3] != "-" else None  # En passant pawns
		# Add pieces
		for i, j in enumerate(functions.splitNumbers(fen.split(" ")[0]).split("/")):
			for x, y in enumerate(j):
				if unicode(y).isnumeric():
					continue
				self.pieces.append(Piece(functions.indexToCoordinate([i, x]), enums.Piece.pawn if y.lower() == "p" else enums.Piece.knight if y.lower() == "n" else enums.Piece.bishop if y.lower() == "b" else enums.Piece.rook if y.lower() == "r" else enums.Piece.queen if y.lower() == "q" else enums.Piece.king, enums.Color.white if y.isupper() else enums.Color.black, self))
				self.squares_hashtable[functions.indexToCoordinate([i, x])] = self.pieces[-1]
				if self.pieces[-1].piece_type == enums.Piece.king:
					if self.pieces[-1].color == enums.Color.white:
						self.white_king = self.pieces[-1]
					else:
						self.black_king = self.pieces[-1]
		# Load opening
		if evaluate_opening:
			self.updateOpening()
		return True

	def loadPGN(self, pgn=None, file=None, quotes="\""):
		"""Loads the specified pgn. If the file argument is specified (is not None), loads the text of the file instead."""
		if file is pgn is None:
			return

		if file is not None:
			pgn = open(file).read()
		self.__init__()
		for x, y in enumerate(pgn.splitlines()):
			if y.strip() == "":
				continue
			if y.strip().startswith("[") and y.strip().endswith("]"):
				self.tags[y[1:y.index(quotes) - 1]] = y[y.index(quotes) + 1:-1]
			if y.startswith("1."):
				moves = functions.getMovesFromString(y)
				for x, y in enumerate(moves):
					try:
						if x == len(moves) - 1:
							self.move(y)
						else:
							self.move(y, evaluate_checks=False, evaluate_opening=False)
					except:
						self.error(errors.InvalidPGNMove(y, x))
						return False
			else:
				self.error(errors.InvalidPGNLine(y, x + 1))
				return False

	def loadOpening(self, opening_name):
		"""Load an opening"""
		for i in openings.openings:
			if opening_name.lower().replace("king's pawn game", "open game").replace("queen's pawn game", "closed game").replace("russian game", "petrov's defense") in [i["name"].lower(), i["eco"].lower() + " " + i["name"].lower(), i["eco"].lower() + i["name"].lower(), i["eco"].lower().replace("'", ""), i["eco"].lower() + " " + i["name"].lower().replace("'", ""), i["eco"].lower() + i["name"].lower().replace("'", "")]:
				self.loadFEN(i["fen"] + " - 0 1")
				return True
		return False

	def reset(self):
		"""Reset game"""
		self.loadFEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

	def FEN(self):
		"""Returns the FEN of the game"""
		fen = ""  # Set fen variable
		# Get squares
		for x in self.squares:
			for y in x:
				if self.pieceAt(y.position):
					fen += (self.pieceAt(y.position).piece_type[0] if self.pieceAt(y.position).piece_type != enums.Piece.knight else "n").upper() if self.pieceAt(y.position).color == enums.Color.white else (self.pieceAt(y.position).piece_type[0] if self.pieceAt(y.position).piece_type != enums.Piece.knight else "n")
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
		"""Returns the PGN of the game."""
		pgn = ""
		for i in kwargs:
			pgn += "[" + i + " \"" + str(kwargs[i]) + "\"]\n"
		pgn += ("\n" if kwargs else "") + self.move_list + str(self.tags["Result"])
		return pgn

	def error(self, error):
		"""Raises an error if allowed"""
		if self.raise_errors:
			raise error

	def placePiece(self, coordinate, color, piece_type):
		"""Places a piece with the specified properties at position `coordinate`, overriding any existing pieces on the coordinate."""
		self.pieces.append(Piece(coordinate, piece_type, color, self))
		self.squares_hashtable[coordinate] = self.pieces[-1]

	def getKing(self, color):
		"""Get the king of color `color`"""
		if not enums.Color.valid(color):
			self.error(errors.UndefinedColor(color))
			return None

		if color == enums.Color.white:
			return self.white_king
		return self.black_king

	def checkLine(self):
		if not self.in_check:
			return False
		return enums.Line(self.checking_piece.position, self.getKing(self.in_check).position, jump=self.checking_piece.piece_type == enums.Piece.knight)

	def move(self, move, evaluate_checks=True, evaluate_opening=True, evaluate_move_checks=True):
		"""Moves the specified move, if possible"""
		if isinstance(move, enums.Move):  # If move is a enums.Move object
			if move.is_capture:  # If the move is a capture
				self.pieces.remove(self.squares_hashtable[move.new_position])  # Remove the captured piece from the list of pieces
				self.squares_hashtable[move.new_position] = False  # Remove the hash of the captured piece from the hashes list
				self.captured_piece = True  # Set captured piece to True

			move.piece.position = move.new_position  # Move the position of the piece to the new position
			self.squares_hashtable[move.piece.position], self.squares_hashtable[move.new_position] = self.squares_hashtable[move.new_position], self.squares_hashtable[move.piece.position]  # Move the piece in the hashtable
			move.piece.moved = True

			if move.castle_rook:  # If the move is a castle
				move.castle_rook.moved = True
				if move.castle == enums.Castle.kingside:  # Kingside castling
					# Move the rook's position to the f-file
					move.castle_rook.position = "f" + move.castle_rook.position[1]
					self.squares_hashtable[move.castle_rook.position], self.squares_hashtable["f" + move.castle_rook.position[1]] = self.squares_hashtable["f" + move.castle_rook.position[1]], self.squares_hashtable[move.castle_rook.position]
				else:  # Queenside castling
					# Move the rook's position to the d-file
					move.castle_rook.position = "d" + move.castle_rook.position[1]
					self.squares_hashtable[move.castle_rook.position], self.squares_hashtable["d" + move.castle_rook.position[1]] = self.squares_hashtable["d" + move.castle_rook.position[1]], self.squares_hashtable[move.castle_rook.position]

			# Reset piece giving check
			self.checking_piece = None

			# Reset en passant positions
			self.en_passant_positions = None
			for i in self.pieces:
				i.en_passant = False

			if move.double_pawn_move:  # If the move is a double pawn push
				move.piece.en_passant = True  # Enable en passant for the piece
				self.en_passant_positions = move.new_position[0] + str(int(move.new_position[1]) - (1 if move.piece.color == enums.Color.white else -1))  # Append position to en passant positions

			if move.en_passant:  # If the move is an en passant capture
				# Remove captured pawn
				self.pieces.remove(self.squares_hashtable[move.en_passant_position])
				self.squares_hashtable[move.en_passant_position] = False
				self.captured_piece = True

			if self.castling_rights is not None and move.piece.piece_type == enums.Piece.king:  # If the king moved
				if move.piece.color == enums.Color.white:  # If the king is white
					self.castling_rights = self.castling_rights.replace("K", "").replace("Q", "")  # Disable white castling
				else:  # If the king is black
					self.castling_rights = self.castling_rights.replace("k", "").replace("q", "")  # Disable black castling

				if self.castling_rights == "":  # If the castling rights variable becomes an empty string
					self.castling_rights = None  # Set the variable to None

			if self.castling_rights is not None and move.piece.piece_type == enums.Piece.rook:  # If the rook moved
				if move.old_position == "a1":  # If the rook was on a1
					self.castling_rights = self.castling_rights.replace("Q", "")  # Disable white queenside castling
				elif move.old_position == "a8":  # If the rook was on a8
					self.castling_rights = self.castling_rights.replace("q", "")  # Disable black queenside castling
				elif move.old_position == "h1":  # If the rook was on h1
					self.castling_rights = self.castling_rights.replace("K", "")  # Disable white kingside castling
				elif move.old_position == "h8":  # If the rook was on h8
					self.castling_rights = self.castling_rights.replace("k", "")  # Disable black kingside castling

			self.raw_move_list.append(move)  # Append move to the raw move list
			if evaluate_checks:  # If the evaluate_checks parameter is True
				if any([True for i in self.legal_moves(show_data=True, color=self.turn, evaluate_checks=evaluate_move_checks) if i.new_position == self.pieceType(enums.Piece.king, color=enums.Color.invert(self.turn))[0].position]):  # If any move can capture the king
					move.name += "+"  # Append a check symbol to the end of the move name
					self.in_check = enums.Color.invert(self.turn)  # Set self.in_check variable to the side in check
					self.checking_piece = move.piece
				else:  # Otherwise
					self.in_check = False  # Reset the self.in_check variable

			if self.turn == enums.Color.white:  # If white moved
				# Add move to move list
				if self.move_list == "":  # If there has not been any moves
					self.move_list += "1. " + move.name
				else:  # Otherwise
					self.move_list += " " + str(int(self.move_list.split(" ")[-3][0]) + 1) + ". " + move.name
			else:  # If black moved
				if self.move_list == "":  # Check for custom FENs
					self.move_list += "1. ... " + move.name  # Add move to move list
				else:
					self.move_list += " " + move.name  # Add move to move list
				self.full_moves += 1  # Increase fullmove counter
			# Calculate halfmove counter
			if move.is_capture or move.piece.piece_type == enums.Piece.pawn:  # Reset halfmove counter if the move is a pawn move or a capture
				self.half_moves = 0
			else:  # Otherwise, increase the halfmove counter by 1
				self.half_moves += 1
			self.turn = enums.Color.invert(self.turn)  # Invert turn
			# Get opening
			if evaluate_opening:
				self.updateOpening()
			return move  # Return the applied move

		if not isinstance(move, str):  # If move is not a string, raise an error and return False
			self.error(errors.InvalidMove(move))
			return False

		move = functions.toSAN(move, self)  # Convert to SAN
		legal_moves = self.legal_moves(show_data=True, evaluate_checks=evaluate_move_checks)  # Store legal moves in legal_moves variable
		move_data = None

		# Iterate through the legal moves
		for i in legal_moves:
			if i.name == move:  # If the name of the current move is the move specified
				move_data = i  # Set move_data equal to the current move
				if i.is_capture:  # If the move is a capture
					# Remove the captured piece
					self.pieces.remove(self.squares_hashtable[i.new_position])
					self.squares_hashtable[i.new_position] = False
					self.captured_piece = True

				self.squares_hashtable[i.piece.position], self.squares_hashtable[i.new_position] = self.squares_hashtable[i.new_position], self.squares_hashtable[i.piece.position]
				i.piece.position = i.new_position
				i.piece.moved = True
				if i.castle_rook:  # If the move is a castle
					i.castle_rook.moved = True
					if i.castle == enums.Castle.kingside:  # Kingside castling
						# Move the rook's position to the f-file
						i.castle_rook.position = "f" + i.castle_rook.position[1]
						self.squares_hashtable[i.castle_rook.position], self.squares_hashtable["f" + i.castle_rook.position[1]] = self.squares_hashtable["f" + i.castle_rook.position[1]], self.squares_hashtable[i.castle_rook.position]
					else:  # Queenside castling
						# Move the rook's position to the d-file
						i.castle_rook.position = "d" + i.castle_rook.position[1]
						self.squares_hashtable[i.castle_rook.position], self.squares_hashtable["d" + i.castle_rook.position[1]] = self.squares_hashtable["d" + i.castle_rook.position[1]], self.squares_hashtable[i.castle_rook.position]

				# Clear en passant positions
				self.en_passant_positions = None
				for x in self.pieces:
					x.en_passant = False

				# Reset piece giving check
				self.checking_piece = None

				# If the move was a double pawn push
				if i.double_pawn_move:
					i.piece.en_passant = True  # Set en_passant variable of moved piece to true
					self.en_passant_positions = i.new_position[0] + str(int(i.new_position[1]) - (1 if i.piece.color == enums.Color.white else -1))  # Append en passant position to en_passant_positions variable

				# If the move was an en passant capture
				if i.en_passant:
					# Remove the captured piece
					self.pieces.remove(self.squares_hashtable[i.en_passant_position])
					self.squares_hashtable[i.en_passant_position] = False
					self.captured_piece = True

				if self.castling_rights is not None and i.piece.piece_type == enums.Piece.king:  # If the piece moved was a king
					if i.piece.color == enums.Color.white:  # If moved side is white
						self.castling_rights = self.castling_rights.replace("K", "").replace("Q", "")  # Disable white castling
					else:  # Otherwise (if moved side is black)
						self.castling_rights = self.castling_rights.replace("k", "").replace("q", "")  # Disable black castling
					if self.castling_rights == "":  # If the castling_rights variable is now an empty string
						self.castling_rights = None  # Set the castling_rights variable to None

				if self.castling_rights is not None and i.piece.piece_type == enums.Piece.rook:  # If the piece moved was a rook
					if i.old_position == "a1":  # If the rook was on a1
						self.castling_rights = self.castling_rights.replace("Q", "")  # Disable white queenside castling
					elif i.old_position == "a8":  # If the rook was on a8
						self.castling_rights = self.castling_rights.replace("q", "")  # Disable black queenside castling
					elif i.old_position == "h1":  # If the rook was on h1
						self.castling_rights = self.castling_rights.replace("K", "")  # Disable white kingside castling
					elif i.old_position == "h8":  # If the rook was on h8
						self.castling_rights = self.castling_rights.replace("k", "")  # Disable black kingside castling

				self.raw_move_list.append(i)  # Append the move to the raw_move_list list
				break  # Break from the loop

		if move_data is None:  # If move_data is None (no move was found), raise an error and return False
			self.error(errors.MoveNotPossible(move))
			return False

		if evaluate_checks:  # If the evaluate_checks parameter is True
			if any([True for i in self.legal_moves(show_data=True, color=self.turn, evaluate_checks=evaluate_move_checks) if i.new_position == self.pieceType(enums.Piece.king, color=enums.Color.invert(self.turn))[0].position]):  # If the king can be captured
				move += "+"  # Append a check symbol to the end of the move
				self.in_check = enums.Color.invert(self.turn)  # Set in_check variable
				self.checking_piece = move_data.piece
			else:  # Otherwise
				self.in_check = False  # Set in_check to False

		# Add move to move list and increase fullmove counter if necessary
		if self.turn == enums.Color.white:  # If white moved
			# Add move to move list
			if self.move_list == "":  # If there has not been any moves
				self.move_list += "1. " + move  # Add a "1. " before the move string to the moves list
			else:  # Otherwise
				self.move_list += " " + str(int(self.move_list.split(" ")[-3][0]) + 1) + ". " + move  # Add a space character, the move number, followed by a period before the move string to the moves list
		else:  # If black moved
			if self.move_list == "":  # If there has not been any moves (a custom FEN)
				self.move_list += "1. ... " + move  # Add a "1. ..." string before the move name to the moves list
			else:  # Otherwise
				self.move_list += " " + move  # Add move name (preceded by a space) to move list

			self.full_moves += 1  # Increase the fullmove counter

		# Calculate halfmove counter
		if move_data.is_capture or move_data.piece.piece_type == enums.Piece.pawn:  # Reset halfmove counter if the move is a pawn move or a capture
			self.half_moves = 0
		else:  # Otherwise, increase the halfmove counter by 1
			self.half_moves += 1

		self.turn = enums.Color.invert(self.turn)  # Invert turn

		if evaluate_opening:  # If the evaluate_opening parameter is True
			self.updateOpening()  # Update the opening using the updateOpening function

		return move_data  # Return the move data (enums.Move object)

	def legal_moves(self, show_data=False, color=enums.Color.current, evaluate_checks=True, piece_type=enums.Piece.all()):
		"""Returns all legal moves by pieces of type(s) piece_type"""
		moves = []  # Define empty moves list

		if color == enums.Color.current:
			color = self.turn

		if isinstance(piece_type, (list, set, tuple)):  # If the piece_type parameter is an iterable
			pieces = {"pawn": [], "knight": [], "bishop": [], "rook": [], "queen": [], "king": []}  # Define hashtable of piece types

			for i in self.pieces:  # Iterate through pieces
				if color == enums.Color.any or i.color == color:
					pieces[i.piece_type].append(i)  # Append piece to respective list in pieces hashtable

			for x in piece_type:  # Iterate through the piece types
				for y in pieces[x]:  # Iterate through the pieces of this type
					moves.extend(y.moves(show_data, evaluate_checks=evaluate_checks))  # Append the piece moves
		elif piece_type in enums.Piece.all():  # If the piece type is a single type
			for i in self.pieceType(piece_type):  # Iterate through the pieces of the specified type
				if color == enums.Color.any or i.color == color:  # If the specified color(s) includes the piece color
					moves.extend(i.moves(show_data, evaluate_checks=evaluate_checks))  # Append the piece moves

		return moves  # Return result

	def pieceType(self, piece, color=enums.Color.any):
		"""Returns all pieces with type `piece` and color `color`"""
		if color == enums.Color.any:
			color = [enums.Color.white, enums.Color.black]
		elif color == enums.Color.current:
			color = [self.turn]
		else:
			color = [color]

		return [i for i in self.pieces if i.color in color and i.piece_type == piece]

	def gamePhase(self):
		"""Returns the current game phase"""
		# The game is in the opening phase if there are less than 7 full moves or a piece has not been captured
		if len(self.raw_move_list) // 2 <= 6 or not self.captured_piece:
			return enums.Phase.opening

		# If the game is not in the opening phase, it is in the endgame phase if both sides do not have a queen, or if the king moved more than three times
		if not self.pieceType(enums.Piece.queen) or [i.piece.piece_type for i in self.raw_move_list].count(enums.Piece.king) > 3:
			return enums.Phase.endgame

		return enums.Phase.middlegame  # Otherwise, the game must be in the middlegame phase

	def totalMaterial(self):
		"""The total amount of material"""
		material = 0
		for i in self.pieces:
			if i.piece_type != enums.Piece.king:
				material += enums.Piece.value(i.piece_type)
		return material

	def materialDifference(self):
		"""Returns the material difference. Positive values indicate white has more material, while negative values indicate black has more."""
		difference = 0
		for i in enums.Piece.all():
			if i == enums.Piece.king:
				continue

			difference += sum([enums.Piece.value(x) for x in self.pieceType(i, enums.Color.white)]) - sum([enums.Piece.value(x) for x in self.pieceType(i, enums.Color.black)])

		return difference

	def evaluate(self):
		"""Evaluates the current position"""
		evaluation_centipawns = (self.materialDifference() * 100) + (0.1 * (len(self.legal_moves(color=enums.Color.white)) - len(self.legal_moves(color=enums.Color.black))))  # Material difference + piece mobility

		for i in self.pieces:
			evaluation_centipawns += enums.Piece.evaluate_piece_position(i.piece_type, i.position, i.color, self.gamePhase()) / 10

		return round(evaluation_centipawns / 100, 5)

	def pieceAt(self, coordinate):
		"""Returns the piece at coordinate if one exists, otherwise return None"""
		if not functions.coordinateValid(coordinate):  # If the coordinate is not valid, raise an error and return None
			self.error(errors.InvalidCoordinate(coordinate))
			return None
		if self.squares_hashtable[coordinate]:
			return self.squares_hashtable[coordinate]
		return None

	def takeback(self):
		"""Take backs one move. To take back multiple moves, call the function multiple times."""
		if not self.raw_move_list:  # If there has not been any moves, return
			return

		# Reset the moved piece's position
		self.squares_hashtable[self.raw_move_list[-1].piece.position], self.squares_hashtable[self.raw_move_list[-1].old_position] = self.squares_hashtable[self.raw_move_list[-1].old_position], self.squares_hashtable[self.raw_move_list[-1].piece.position]
		self.raw_move_list[-1].piece.position = self.raw_move_list[-1].old_position

		if self.raw_move_list[-1].is_capture:  # If the last move was a capture
			# Bring back the captured piece
			self.pieces.append(Piece(self.raw_move_list[-1].new_position, self.raw_move_list[-1].captured_piece.piece_type, self.raw_move_list[-1].captured_piece.color, self))
			self.squares_hashtable[self.raw_move_list[-1].new_position] = self.pieces[-1]

		self.raw_move_list.pop()  # Remove the last move from the raw move list

		# Remove the last move from the move list
		if self.move_list.split(" ")[-2][-1] == ".":
			self.move_list = " ".join(self.move_list.split(" ")[:-2])
		else:
			self.move_list = " ".join(self.move_list.split(" ")[:-1])

		self.turn = enums.Color.invert(self.turn)  # Invert the turn
		self.en_passant_positions = None  # Reset en_passant_positions
		# Set opening
		if self.move_list == "":
			self.opening = ""
		else:
			self.updateOpening()

	def updateOpening(self):
		"""Updates the opening if evaluate_openings is True"""
		if self.evaluate_openings:
			opening = False
			for i in openings.openings:
				if i["position"] == self.FEN().split(" ")[0]:
					self.opening = i["eco"] + " " + i["name"]
					opening = i["eco"] + " " + i["name"]
					break
			return opening
		else:
			return False

	def attackers(self, coordinate, color):
		"""Returns a list of the pieces that attack the coordinate"""
		if color == enums.Color.current:
			color = self.turn
		if color not in [enums.Color.white, enums.Color.black]:
			self.error(errors.UndefinedColor(color))
			return []
		if self.pieceAt(coordinate) and self.pieceAt(coordinate).color == color:
			self.error(errors.InvalidColor("The color " + str(color) + " is invalid, as the piece at " + str(coordinate) + " has the same color. Perhaps you meant to use the protectors() function?"))
			return []
		attackers = []
		for i in self.pieces:
			if i.color != color:
				continue
			if i.piece_type == enums.Piece.pawn:  # Pawn capture squares
				if coordinate in [i.new_position for i in self.generatePawnCaptures(i.position, color, return_all=True)]:
					attackers.append(i)
			elif i.piece_type == enums.Piece.knight:  # Knight capture squares
				if coordinate in [i.new_position for i in self.generateKnightMoves(i.position, color)]:
					attackers.append(i)
			elif i.piece_type == enums.Piece.bishop:  # Bishop capture squares
				if coordinate in [i.new_position for i in self.generateBishopMoves(i.position, color)]:
					attackers.append(i)
			elif i.piece_type == enums.Piece.rook:  # Rook capture squares
				if coordinate in [i.new_position for i in self.generateRookMoves(i.position, color)]:
					attackers.append(i)
			elif i.piece_type == enums.Piece.queen:  # Queen capture squares
				if coordinate in [i.new_position for i in self.generateQueenMoves(i.position, color)]:
					attackers.append(i)
			elif i.piece_type == enums.Piece.king:  # King capture squares
				if functions.coordinateToIndex(coordinate) in [[functions.coordinateToIndex(i.position)[0] - 1, functions.coordinateToIndex(i.position)[1] - 1], [functions.coordinateToIndex(i.position)[0] - 1, functions.coordinateToIndex(i.position)[1]], [functions.coordinateToIndex(i.position)[0] - 1, functions.coordinateToIndex(i.position)[1] + 1], [functions.coordinateToIndex(i.position)[0], functions.coordinateToIndex(i.position)[1] - 1], [functions.coordinateToIndex(i.position)[0], functions.coordinateToIndex(i.position)[1] + 1], [functions.coordinateToIndex(i.position)[0] + 1, functions.coordinateToIndex(i.position)[1] - 1], [functions.coordinateToIndex(i.position)[0] + 1, functions.coordinateToIndex(i.position)[1]], [functions.coordinateToIndex(i.position)[0] + 1, functions.coordinateToIndex(i.position)[1] + 1]]:
					attackers.append(i)
		return attackers

	def protectors(self, piece):
		"""Returns a list of the pieces that protect the piece"""
		if not isinstance(piece, Piece):
			self.error(errors.InvalidPiece(piece))
		protectors = []
		for x in self.pieces:
			if x.color != piece.color:
				continue
			if x.piece_type == enums.Piece.pawn:
				if piece.position in [i.new_position for i in self.generatePawnCaptures(x.position, x.color, return_all=True)]:
					protectors.append(x)
			elif x.piece_type == enums.Piece.knight:
				if piece.position in [i.new_position for i in self.generateKnightMoves(x.position, x.color, return_all=True)]:
					protectors.append(x)
			elif x.piece_type == enums.Piece.bishop:
				if piece.position in [i.new_position for i in self.generateBishopMoves(x.position, x.color, stop=enums.Stop.piece)]:
					protectors.append(x)
			elif x.piece_type == enums.Piece.rook:
				if piece.position in [i.new_position for i in self.generateRookMoves(x.position, x.color, stop=enums.Stop.piece)]:
					protectors.append(x)
			elif x.piece_type == enums.Piece.queen:
				if piece.position in [i.new_position for i in self.generateQueenMoves(x.position, x.color, stop=enums.Stop.piece)]:
					protectors.append(x)
		return protectors

	def visualized(self, print_result=False, use_unicode=True, empty_squares=" ", separators=True):
		if empty_squares == "":
			empty_squares = " "
		empty_squares = empty_squares[0]
		if print_result:
			print((("---------------------------------\n| " if use_unicode else "-----------------------------------------\n| ") + (" |\n---------------------------------\n| " if use_unicode else " |\n-----------------------------------------\n| ").join(" | ".join([y + ((empty_squares if use_unicode else empty_squares + " ") if y == "" else "") for y in x]) for x in [["".join([((enums.Piece.unicode(z.piece_type, z.color)) if use_unicode else (z.color[0].upper() + (z.piece_type[0].upper() if z.piece_type != "knight" else "N"))) if functions.coordinateToIndex(z.position) == [x, y] else "" for z in self.pieces]) for y in range(len(self.squares[x]))] for x in range(len(self.squares))]) + (" |\n---------------------------------" if use_unicode else " |\n-----------------------------------------")) if separators else ("\n".join(" ".join([y + ((empty_squares if use_unicode else empty_squares + " ") if y == "" else "") for y in x]) for x in [["".join([((enums.Piece.unicode(z.piece_type, z.color)) if use_unicode else (z.color[0].upper() + (z.piece_type[0].upper() if z.piece_type != "knight" else "N"))) if functions.coordinateToIndex(z.position) == [x, y] else "" for z in self.pieces]) for y in range(len(self.squares[x]))] for x in range(len(self.squares))])))
		else:
			return (("---------------------------------\n| " if use_unicode else "-----------------------------------------\n| ") + (" |\n---------------------------------\n| " if use_unicode else " |\n-----------------------------------------\n| ").join(" | ".join([y + ((empty_squares if use_unicode else empty_squares + " ") if y == "" else "") for y in x]) for x in [["".join([((enums.Piece.unicode(z.piece_type, z.color)) if use_unicode else (z.color[0].upper() + (z.piece_type[0].upper() if z.piece_type != "knight" else "N"))) if functions.coordinateToIndex(z.position) == [x, y] else "" for z in self.pieces]) for y in range(len(self.squares[x]))] for x in range(len(self.squares))]) + (" |\n---------------------------------" if use_unicode else " |\n-----------------------------------------")) if separators else ("\n".join(" ".join([y + ((empty_squares if use_unicode else empty_squares + " ") if y == "" else "") for y in x]) for x in [["".join([((enums.Piece.unicode(z.piece_type, z.color)) if use_unicode else (z.color[0].upper() + (z.piece_type[0].upper() if z.piece_type != "knight" else "N"))) if functions.coordinateToIndex(z.position) == [x, y] else "" for z in self.pieces]) for y in range(len(self.squares[x]))] for x in range(len(self.squares))]))

	def generatePawnMoves(self, position, color, return_all=False, piece=None):
		if (color == enums.Color.black and position[1] == "1") or (color == enums.Color.white and position[1] == "8"):
			return []
		if not functions.coordinateValid(position):
			self.error(errors.InvalidCoordinate(position))
			return []
		elif enums.Color.isWhite(color):
			if not return_all and self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1]])):
				return []
			if position[1] == "2" and ((not return_all and not self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 2, functions.coordinateToIndex(position)[1]]))) or return_all):
				return [enums.Move(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1]]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1]]), piece), enums.Move(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 2, functions.coordinateToIndex(position)[1]]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 2, functions.coordinateToIndex(position)[1]]), piece, double_pawn_move=True)]
			return [enums.Move(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1]]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1]]), piece)]
		elif enums.Color.isBlack(color):
			if not return_all and self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1]])):
				return []
			if position[1] == "7" and ((not return_all and not self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 2, functions.coordinateToIndex(position)[1]]))) or return_all):
				return [enums.Move(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1]]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1]]), piece), enums.Move(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 2, functions.coordinateToIndex(position)[1]]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 2, functions.coordinateToIndex(position)[1]]), piece, double_pawn_move=True)]
			return [enums.Move(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1]]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1]]), piece)]
		else:
			self.error(errors.UndefinedColor(color))
			return []

	def generatePawnCaptures(self, position, color, return_all=False, piece=None):
		if (color == enums.Color.black and position[1] == "1") or (color == enums.Color.white and position[1] == "8"):
			return []

		if not functions.coordinateValid(position):
			self.error(errors.InvalidCoordinate(position))
			return []

		if enums.Color.isWhite(color):
			if position[0] not in "ah" and (return_all or (self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 1])) and self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 1])) and self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 1])).color != color and self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 1])).color != color)):
				return [enums.Move(position[0] + "x" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 1]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 1]), piece, is_capture=True), enums.Move(position[0] + "x" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 1]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 1]), piece, is_capture=True)]

			if position[0] != "h" and self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 1])) and self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 1])).color != color:
				return [enums.Move(position[0] + "x" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 1]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 1]), piece, is_capture=True)]

			if position[0] != "a" and self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 1])) and self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 1])).color != color:
				return [enums.Move(position[0] + "x" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 1]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 1]), piece, is_capture=True)]
		elif enums.Color.isBlack(color):
			if position[0] not in "ah" and (return_all or (self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 1])) and self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 1])) and self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 1])).color != color and self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 1])).color != color)):
				return [enums.Move(position[0] + "x" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 1]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 1]), piece, is_capture=True), enums.Move(position[0] + "x" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 1]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 1]), piece, is_capture=True)]

			if position[0] != "h" and self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 1])) and self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 1])).color != color:
				return [enums.Move(position[0] + "x" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 1]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 1]), piece, is_capture=True)]

			if position[0] != "a" and self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 1])) and self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 1])).color != color:
				return [enums.Move(position[0] + "x" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 1]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 1]), piece, is_capture=True)]
		else:
			self.error(errors.UndefinedColor(color))

		return []

	def generateKnightMoves(self, position, color, return_all=False, piece=None):
		if not functions.coordinateValid(position):
			self.error(errors.InvalidCoordinate(position))
			return []
		if not enums.Color.valid(color):
			self.error(errors.UndefinedColor(color))
			return []
		moves = []
		if position[0] != "h" and position[1] not in ["1", "2"]:
			if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 2, functions.coordinateToIndex(position)[1] + 1])) and not return_all:
				if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 2, functions.coordinateToIndex(position)[1] + 1])).color == enums.Color.invert(color):
					moves.append(enums.Move("Nx" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 2, functions.coordinateToIndex(position)[1] + 1]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 2, functions.coordinateToIndex(position)[1] + 1]), piece, is_capture=True))
			else:
				moves.append(enums.Move("N" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 2, functions.coordinateToIndex(position)[1] + 1]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 2, functions.coordinateToIndex(position)[1] + 1]), piece))
		if position[0] not in ["g", "h"] and position[1] != "1":
			if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 2])) and not return_all:
				if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 2])).color == enums.Color.invert(color):
					moves.append(enums.Move("Nx" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 2]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 2]), piece, is_capture=True))
			else:
				moves.append(enums.Move("N" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 2]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 2]), piece))
		if position[0] != "a" and position[1] not in ["7", "8"]:
			if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 2, functions.coordinateToIndex(position)[1] - 1])) and not return_all:
				if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 2, functions.coordinateToIndex(position)[1] - 1])).color == enums.Color.invert(color):
					moves.append(enums.Move("Nx" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 2, functions.coordinateToIndex(position)[1] - 1]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 2, functions.coordinateToIndex(position)[1] - 1]), piece, is_capture=True))
			else:
				moves.append(enums.Move("N" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 2, functions.coordinateToIndex(position)[1] - 1]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 2, functions.coordinateToIndex(position)[1] - 1]), piece))
		if position[0] not in ["a", "b"] and position[1] != "8":
			if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 2])) and not return_all:
				if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 2])).color == enums.Color.invert(color):
					moves.append(enums.Move("Nx" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 2]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 2]), piece, is_capture=True))
			else:
				moves.append(enums.Move("N" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 2]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 2]), piece))
		if position[0] != "a" and position[1] not in ["1", "2"]:
			if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 2, functions.coordinateToIndex(position)[1] - 1])) and not return_all:
				if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 2, functions.coordinateToIndex(position)[1] - 1])).color == enums.Color.invert(color):
					moves.append(enums.Move("Nx" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 2, functions.coordinateToIndex(position)[1] - 1]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 2, functions.coordinateToIndex(position)[1] - 1]), piece, is_capture=True))
			else:
				moves.append(enums.Move("N" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 2, functions.coordinateToIndex(position)[1] - 1]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 2, functions.coordinateToIndex(position)[1] - 1]), piece))
		if position[0] not in ["a", "b"] and position[1] != "1":
			if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 2])) and not return_all:
				if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 2])).color == enums.Color.invert(color):
					moves.append(enums.Move("Nx" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 2]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 2]), piece, is_capture=True))
			else:
				moves.append(enums.Move("N" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 2]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 2]), piece))
		if position[0] != "h" and position[1] not in ["7", "8"]:
			if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 2, functions.coordinateToIndex(position)[1] + 1])) and not return_all:
				if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 2, functions.coordinateToIndex(position)[1] + 1])).color == enums.Color.invert(color):
					moves.append(enums.Move("Nx" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 2, functions.coordinateToIndex(position)[1] + 1]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 2, functions.coordinateToIndex(position)[1] + 1]), piece, is_capture=True))
			else:
				moves.append(enums.Move("N" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 2, functions.coordinateToIndex(position)[1] + 1]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 2, functions.coordinateToIndex(position)[1] + 1]), piece))
		if position[0] not in ["g", "h"] and position[1] != "8":
			if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 2])) and not return_all:
				if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 2])).color == enums.Color.invert(color):
					moves.append(enums.Move("Nx" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 2]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 2]), piece, is_capture=True))
			else:
				moves.append(enums.Move("N" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 2]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 2]), piece))
		return moves

	def generateBishopMoves(self, position, color, stop=enums.Stop.capture_piece, piece=None):
		moves = []
		capture, (pos1, pos2), piece_found = False, functions.coordinateToIndex(position), 0
		while pos1 != 0 and pos2 != 0:
			pos1, pos2 = pos1 - 1, pos2 - 1
			if stop == enums.Stop.piece:
				moves.append(enums.Move("B" + functions.indexToCoordinate([pos1, pos2]), position, functions.indexToCoordinate([pos1, pos2]), piece))
				if self.pieceAt(functions.indexToCoordinate([pos1, pos2])):
					break
			elif stop != enums.Stop.never:
				for i in self.pieces:
					if functions.coordinateToIndex(i.position) == [pos1, pos2]:
						if stop == enums.Stop.capture_piece:
							if i.color == color:
								break
							capture = True
						elif stop == enums.Stop.no_capture:
							break
				else:
					moves.append(enums.Move("B" + ("x" if capture else "") + functions.indexToCoordinate([pos1, pos2]), position, functions.indexToCoordinate([pos1, pos2]), piece, is_capture=capture))
					if capture:
						break
					continue
				break
			else:
				moves.append(enums.Move("B" + functions.indexToCoordinate([pos1, pos2]), position, functions.indexToCoordinate([pos1, pos2]), piece))
		capture, (pos1, pos2) = False, functions.coordinateToIndex(position)
		while pos1 != 7 and pos2 != 7:
			pos1, pos2 = pos1 + 1, pos2 + 1
			if stop == enums.Stop.piece:
				moves.append(enums.Move("B" + functions.indexToCoordinate([pos1, pos2]), position, functions.indexToCoordinate([pos1, pos2]), piece))
				if self.pieceAt(functions.indexToCoordinate([pos1, pos2])):
					break
			elif stop != enums.Stop.never:
				for i in self.pieces:
					if functions.coordinateToIndex(i.position) == [pos1, pos2]:
						if stop == enums.Stop.capture_piece:
							if i.color == color:
								break
							capture = True
						elif stop == enums.Stop.no_capture:
							break
				else:
					moves.append(enums.Move("B" + ("x" if capture else "") + functions.indexToCoordinate([pos1, pos2]), position, functions.indexToCoordinate([pos1, pos2]), piece, is_capture=capture))
					if capture:
						break
					continue
				break
			else:
				moves.append(enums.Move("B" + functions.indexToCoordinate([pos1, pos2]), position, functions.indexToCoordinate([pos1, pos2]), piece))
		capture, (pos1, pos2) = False, functions.coordinateToIndex(position)
		while pos1 != 0 and pos2 != 7:
			pos1, pos2 = pos1 - 1, pos2 + 1
			if stop == enums.Stop.piece:
				moves.append(enums.Move("B" + functions.indexToCoordinate([pos1, pos2]), position, functions.indexToCoordinate([pos1, pos2]), piece))
				if self.pieceAt(functions.indexToCoordinate([pos1, pos2])):
					break
			elif stop != enums.Stop.never:
				for i in self.pieces:
					if functions.coordinateToIndex(i.position) == [pos1, pos2]:
						if stop == enums.Stop.capture_piece:
							if i.color == color:
								break
							capture = True
						elif stop == enums.Stop.no_capture:
							break
				else:
					moves.append(enums.Move("B" + ("x" if capture else "") + functions.indexToCoordinate([pos1, pos2]), position, functions.indexToCoordinate([pos1, pos2]), piece, is_capture=capture))
					if capture:
						break
					continue
				break
			else:
				moves.append(enums.Move("B" + functions.indexToCoordinate([pos1, pos2]), position, functions.indexToCoordinate([pos1, pos2]), piece))
		capture, (pos1, pos2) = False, functions.coordinateToIndex(position)
		while pos1 != 7 and pos2 != 0:
			pos1, pos2 = pos1 + 1, pos2 - 1
			if stop == enums.Stop.piece:
				moves.append(enums.Move("B" + functions.indexToCoordinate([pos1, pos2]), position, functions.indexToCoordinate([pos1, pos2]), piece))
				if self.pieceAt(functions.indexToCoordinate([pos1, pos2])):
					break
			elif stop != enums.Stop.never:
				for i in self.pieces:
					if functions.coordinateToIndex(i.position) == [pos1, pos2]:
						if stop == enums.Stop.capture_piece:
							if i.color == color:
								break
							capture = True
						elif stop == enums.Stop.no_capture:
							break
				else:
					moves.append(enums.Move("B" + ("x" if capture else "") + functions.indexToCoordinate([pos1, pos2]), position, functions.indexToCoordinate([pos1, pos2]), piece, is_capture=capture))
					if capture:
						break
					continue
				break
			else:
				moves.append(enums.Move("B" + functions.indexToCoordinate([pos1, pos2]), position, functions.indexToCoordinate([pos1, pos2]), piece))
		return moves

	def generateRookMoves(self, position, color, stop=enums.Stop.capture_piece, piece=None):
		moves = []
		capture = False
		for x in reversed(range(functions.coordinateToIndex(position)[0])):
			if stop == enums.Stop.piece:
				moves.append(enums.Move("R" + functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]]), position, functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]]), piece))
				if self.pieceAt(functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]])):
					break
			elif stop != enums.Stop.never:
				for y in self.pieces:
					if functions.coordinateToIndex(y.position) == [x, functions.coordinateToIndex(position)[1]]:
						if y.color == color or stop == enums.Stop.no_capture:
							break
						capture = True
				else:
					moves.append(enums.Move("R" + ("x" if capture else "") + functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]]), position, functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]]), piece, is_capture=capture))
					if capture:
						break
					continue
				break
			else:
				moves.append(enums.Move("R" + functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]]), position, functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]]), piece))
		capture = False
		for x in reversed(range(functions.coordinateToIndex(position)[1])):
			if stop == enums.Stop.piece:
				moves.append(enums.Move("R" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x]), piece))
				if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x])):
					break
			elif stop != enums.Stop.never:
				for y in self.pieces:
					if functions.coordinateToIndex(y.position) == [functions.coordinateToIndex(position)[0], x]:
						if y.color == color or stop == enums.Stop.no_capture:
							break
						capture = True
				else:
					moves.append(enums.Move("R" + ("x" if capture else "") + functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x]), piece, is_capture=capture))
					if capture:
						break
					continue
				break
			else:
				moves.append(enums.Move("R" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x]), piece))
		capture = False
		for x in range(functions.coordinateToIndex(position)[0] + 1, 8):
			if stop == enums.Stop.piece:
				moves.append(enums.Move("R" + functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]]), position, functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]]), piece))
				if self.pieceAt(functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]])):
					break
			elif stop != enums.Stop.never:
				for y in self.pieces:
					if functions.coordinateToIndex(y.position) == [x, functions.coordinateToIndex(position)[1]]:
						if y.color == color or stop == enums.Stop.no_capture:
							break
						capture = True
				else:
					moves.append(enums.Move("R" + ("x" if capture else "") + functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]]), position, functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]]), piece, is_capture=capture))
					if capture:
						break
					continue
				break
			else:
				moves.append(enums.Move("R" + functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]]), position, functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]]), piece))
		capture = False
		for x in range(functions.coordinateToIndex(position)[1] + 1, 8):
			if stop == enums.Stop.piece:
				moves.append(enums.Move("R" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x]), piece))
				if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x])):
					break
			elif stop != enums.Stop.never:
				for y in self.pieces:
					if functions.coordinateToIndex(y.position) == [functions.coordinateToIndex(position)[0], x]:
						if y.color == color or stop == enums.Stop.no_capture:
							break
						capture = True
				else:
					moves.append(enums.Move("R" + ("x" if capture else "") + functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x]), piece, is_capture=capture))
					if capture:
						break
					continue
				break
			else:
				moves.append(enums.Move("R" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x]), piece))
		return moves

	def generateQueenMoves(self, position, color, stop=enums.Stop.capture_piece, piece=None):
		moves = []
		# Diagonal moves
		capture, (pos1, pos2), piece_found = False, functions.coordinateToIndex(position), 0
		while pos1 != 0 and pos2 != 0:
			pos1, pos2 = pos1 - 1, pos2 - 1
			if stop == enums.Stop.piece:
				moves.append(enums.Move("Q" + functions.indexToCoordinate([pos1, pos2]), position, functions.indexToCoordinate([pos1, pos2]), piece))
				if self.pieceAt(functions.indexToCoordinate([pos1, pos2])):
					break
			elif stop != enums.Stop.never:
				for i in self.pieces:
					if functions.coordinateToIndex(i.position) == [pos1, pos2]:
						if stop == enums.Stop.capture_piece:
							if i.color == color:
								break
							capture = True
						elif stop == enums.Stop.no_capture:
							break
				else:
					moves.append(enums.Move("Q" + ("x" if capture else "") + functions.indexToCoordinate([pos1, pos2]), position, functions.indexToCoordinate([pos1, pos2]), piece, is_capture=capture))
					if capture:
						break
					continue
				break
			else:
				moves.append(enums.Move("Q" + functions.indexToCoordinate([pos1, pos2]), position, functions.indexToCoordinate([pos1, pos2]), piece))
		capture, (pos1, pos2) = False, functions.coordinateToIndex(position)
		while pos1 != 7 and pos2 != 7:
			pos1, pos2 = pos1 + 1, pos2 + 1
			if stop == enums.Stop.piece:
				moves.append(enums.Move("Q" + functions.indexToCoordinate([pos1, pos2]), position, functions.indexToCoordinate([pos1, pos2]), piece))
				if self.pieceAt(functions.indexToCoordinate([pos1, pos2])):
					break
			elif stop != enums.Stop.never:
				for i in self.pieces:
					if functions.coordinateToIndex(i.position) == [pos1, pos2]:
						if stop == enums.Stop.capture_piece:
							if i.color == color:
								break
							capture = True
						elif stop == enums.Stop.no_capture:
							break
				else:
					moves.append(enums.Move("Q" + ("x" if capture else "") + functions.indexToCoordinate([pos1, pos2]), position, functions.indexToCoordinate([pos1, pos2]), piece, is_capture=capture))
					if capture:
						break
					continue
				break
			else:
				moves.append(enums.Move("Q" + functions.indexToCoordinate([pos1, pos2]), position, functions.indexToCoordinate([pos1, pos2]), piece))
		capture, (pos1, pos2) = False, functions.coordinateToIndex(position)
		while pos1 != 0 and pos2 != 7:
			pos1, pos2 = pos1 - 1, pos2 + 1
			if stop == enums.Stop.piece:
				moves.append(enums.Move("Q" + functions.indexToCoordinate([pos1, pos2]), position, functions.indexToCoordinate([pos1, pos2]), piece))
				if self.pieceAt(functions.indexToCoordinate([pos1, pos2])):
					break
			elif stop != enums.Stop.never:
				for i in self.pieces:
					if functions.coordinateToIndex(i.position) == [pos1, pos2]:
						if stop == enums.Stop.capture_piece:
							if i.color == color:
								break
							capture = True
						elif stop == enums.Stop.no_capture:
							break
				else:
					moves.append(enums.Move("Q" + ("x" if capture else "") + functions.indexToCoordinate([pos1, pos2]), position, functions.indexToCoordinate([pos1, pos2]), piece, is_capture=capture))
					if capture:
						break
					continue
				break
			else:
				moves.append(enums.Move("Q" + functions.indexToCoordinate([pos1, pos2]), position, functions.indexToCoordinate([pos1, pos2]), piece))
		capture, (pos1, pos2) = False, functions.coordinateToIndex(position)
		while pos1 != 7 and pos2 != 0:
			pos1, pos2 = pos1 + 1, pos2 - 1
			if stop == enums.Stop.piece:
				moves.append(enums.Move("Q" + functions.indexToCoordinate([pos1, pos2]), position, functions.indexToCoordinate([pos1, pos2]), piece))
				if self.pieceAt(functions.indexToCoordinate([pos1, pos2])):
					break
			elif stop != enums.Stop.never:
				for i in self.pieces:
					if functions.coordinateToIndex(i.position) == [pos1, pos2]:
						if stop == enums.Stop.capture_piece:
							if i.color == color:
								break
							capture = True
						elif stop == enums.Stop.no_capture:
							break
				else:
					moves.append(enums.Move("Q" + ("x" if capture else "") + functions.indexToCoordinate([pos1, pos2]), position, functions.indexToCoordinate([pos1, pos2]), piece, is_capture=capture))
					if capture:
						break
					continue
				break
			else:
				moves.append(enums.Move("Q" + functions.indexToCoordinate([pos1, pos2]), position, functions.indexToCoordinate([pos1, pos2]), piece))
		# Straight moves
		capture = False
		for x in reversed(range(functions.coordinateToIndex(position)[0])):
			if stop == enums.Stop.piece:
				moves.append(enums.Move("Q" + functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]]), position, functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]]), piece))
				if self.pieceAt(functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]])):
					break
			elif stop != enums.Stop.never:
				for y in self.pieces:
					if functions.coordinateToIndex(y.position) == [x, functions.coordinateToIndex(position)[1]]:
						if y.color == color or stop == enums.Stop.no_capture:
							break
						capture = True
				else:
					moves.append(enums.Move("Q" + ("x" if capture else "") + functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]]), position, functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]]), piece, is_capture=capture))
					if capture:
						break
					continue
				break
			else:
				moves.append(enums.Move("Q" + functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]]), position, functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]]), piece))
		capture = False
		for x in reversed(range(functions.coordinateToIndex(position)[1])):
			if stop == enums.Stop.piece:
				moves.append(enums.Move("Q" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x]), piece))
				if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x])):
					break
			elif stop != enums.Stop.never:
				for y in self.pieces:
					if functions.coordinateToIndex(y.position) == [functions.coordinateToIndex(position)[0], x]:
						if y.color == color or stop == enums.Stop.no_capture:
							break
						capture = True
				else:
					moves.append(enums.Move("Q" + ("x" if capture else "") + functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x]), piece, is_capture=capture))
					if capture:
						break
					continue
				break
			else:
				moves.append(enums.Move("Q" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x]), piece))
		capture = False
		for x in range(functions.coordinateToIndex(position)[0] + 1, 8):
			if stop == enums.Stop.piece:
				moves.append(enums.Move("Q" + functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]]), position, functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]]), piece))
				if self.pieceAt(functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]])):
					break
			elif stop != enums.Stop.never:
				for y in self.pieces:
					if functions.coordinateToIndex(y.position) == [x, functions.coordinateToIndex(position)[1]]:
						if y.color == color or stop == enums.Stop.no_capture:
							break
						capture = True
				else:
					moves.append(enums.Move("Q" + ("x" if capture else "") + functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]]), position, functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]]), piece, is_capture=capture))
					if capture:
						break
					continue
				break
			else:
				moves.append(enums.Move("Q" + functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]]), position, functions.indexToCoordinate([x, functions.coordinateToIndex(position)[1]]), piece))
		capture = False
		for x in range(functions.coordinateToIndex(position)[1] + 1, 8):
			if stop == enums.Stop.piece:
				moves.append(enums.Move("Q" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x]), piece))
				if self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x])):
					break
			elif stop != enums.Stop.never:
				for y in self.pieces:
					if functions.coordinateToIndex(y.position) == [functions.coordinateToIndex(position)[0], x]:
						if y.color == color or stop == enums.Stop.no_capture:
							break
						capture = True
				else:
					moves.append(enums.Move("Q" + ("x" if capture else "") + functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x]), piece, is_capture=capture))
					if capture:
						break
					continue
				break
			else:
				moves.append(enums.Move("Q" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0], x]), piece))
		return moves

	def __str__(self):
		return "Chess Game with FEN " + self.FEN()

	def __lt__(self, other):
		return self.totalMaterial() < other.totalMaterial()

	def __le__(self, other):
		return self.totalMaterial() <= other.totalMaterial()

	def __contains__(self, obj):
		if isinstance(obj, Piece):
			return self.squares_hashtable[obj.position] == obj
		if isinstance(obj, Square):
			return vars(obj) in map(vars, self.squares)

		self.error(TypeError("Invalid type: " + str(obj)))
		return False

	def __unicode__(self):
		return "---------------------------------\n| " + " |\n---------------------------------\n| ".join(" | ".join([y + (" " if y == "" else "") for y in x]) for x in [["".join([(enums.Piece.unicode(z.piece_type, z.color)) if functions.coordinateToIndex(z.position) == [x, y] else "" for z in self.pieces]) for y in range(len(self.squares[x]))] for x in range(len(self.squares))]) + " |\n---------------------------------"

	def __eq__(self, other):
		return self.FEN() == other.FEN()

	__add__ = __radd__ = __sub__ = __rsub__ = __mul__ = __rmul__ = __div__ = __rdiv__ = __truediv__ = __rtruediv__ = __floordiv__ = __rfloordiv__ = __mod__ = __rmod__ = __divmod__ = __rdivmod__ = __pow__ = __rpow__ = __lshift__ = __rlshift__ = __rshift__ = __rrshift__ = __and__ = __rand__ = __or__ = __ror__ = __xor__ = __rxor__ = __iadd__ = __isub__ = __imul__ = __idiv__ = __itruediv__ = __ifloordiv__ = __imod__ = __ipow__ = __iand__ = __ior__ = __ixor__ = __ilshift__ = __irshift__ = __neg__ = __pos__ = __abs__ = __invert__ = __int__ = __long__ = __float__ = __complex__ = __oct__ = __hex__ = __coerce__ = lambda self, *args: self.error(ArithmeticError("Cannot perform arithmetic operations on Game object"))

	__getitem__ = __setitem__ = __delitem__ = __getslice__ = __setslice__ = __delslice__ = lambda self, *args: self.error(IndexError("Cannot perform operation on Game object"))
