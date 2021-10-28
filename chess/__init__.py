# -*- coding: utf-8 -*-


"""
Imports
"""

import chess.functions
import chess.enums
import chess.errors
import chess.openings

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
	def __init__(self, position, piece_type, color, board, append=True):
		"""Initialize the piece. Auto-appends piece to the board if the `append` option is True"""
		if append:
			board.pieces.append(self)
		self.position = position if isinstance(position, str) else functions.indexToCoordinate(position)
		self.piece_type, self.color, self.board = piece_type, color, board
		self.moved = False
		self.en_passant = False

	def moves(self, show_data=False, evaluate_checks=True):
		"""Legal moves of the piece"""
		moves = []
		if self.piece_type == enums.Piece.pawn:  # Pawn moves
			moves.extend(self.board.generatePawnCaptures(self.position, self.color, piece=self) + self.board.generatePawnMoves(self.position, self.color, piece=self))
		elif self.piece_type == enums.Piece.knight:  # Knight moves
			moves.extend(self.board.generateKnightMoves(self.position, self.color, piece=self))
		elif self.piece_type == enums.Piece.bishop:  # Bishop moves
			moves.extend(self.board.generateBishopMoves(self.position, self.color, piece=self))
		if self.piece_type == enums.Piece.rook:  # Rook moves
			moves.extend(self.board.generateRookMoves(self.position, self.color, piece=self))
		elif self.piece_type == "queen":  # Queen moves
			moves.extend(self.board.generateQueenMoves(self.position, self.color, piece=self))
		elif self.piece_type == enums.Piece.king:
			if self.position[0] != "h" and self.position[1] != "1":
				if not self.board.attackers(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] + 1]), enums.Color.invert(self.color)):
					if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] + 1])):
						if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] + 1])).color != self.color:
							moves.append(enums.Move(name="Kx" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] + 1]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] + 1]), piece=self, is_capture=True))
					else:
						moves.append(enums.Move(name="K" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] + 1]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] + 1]), piece=self))
			if self.position[0] != "a" and self.position[1] != "8":
				if not self.board.attackers(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] - 1]), enums.Color.invert(self.color)):
					if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] - 1])):
						if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] - 1])).color != self.color:
							moves.append(enums.Move(name="Kx" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] - 1]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] - 1]), piece=self, is_capture=True))
					else:
						moves.append(enums.Move(name="K" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] - 1]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] - 1]), piece=self))
			if self.position[0] != "a" and self.position[1] != "1":
				if not self.board.attackers(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] - 1]), enums.Color.invert(self.color)):
					if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] - 1])):
						if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] - 1])).color != self.color:
							moves.append(enums.Move(name="Kx" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] - 1]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] - 1]), piece=self, is_capture=True))
					else:
						moves.append(enums.Move(name="K" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] - 1]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] - 1]), piece=self))
			if self.position[0] != "h" and self.position[1] != "8":
				if not self.board.attackers(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] + 1]), enums.Color.invert(self.color)):
					if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] + 1])):
						if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] + 1])).color != self.color:
							moves.append(enums.Move(name="Kx" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] + 1]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] + 1]), piece=self, is_capture=True))
					else:
						moves.append(enums.Move(name="K" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] + 1]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] + 1]), piece=self))
			if self.position[0] != "a":
				if not self.board.attackers(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], functions.coordinateToIndex(self.position)[1] - 1]), enums.Color.invert(self.color)):
					if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], functions.coordinateToIndex(self.position)[1] - 1])):
						if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], functions.coordinateToIndex(self.position)[1] - 1])).color != self.color:
							moves.append(enums.Move(name="Kx" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], functions.coordinateToIndex(self.position)[1] - 1]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], functions.coordinateToIndex(self.position)[1] - 1]), piece=self, is_capture=True))
					else:
						moves.append(enums.Move(name="K" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], functions.coordinateToIndex(self.position)[1] - 1]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], functions.coordinateToIndex(self.position)[1] - 1]), piece=self))
			if self.position[0] != "h":
				if not self.board.attackers(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], functions.coordinateToIndex(self.position)[1] + 1]), enums.Color.invert(self.color)):
					if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], functions.coordinateToIndex(self.position)[1] + 1])):
						if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], functions.coordinateToIndex(self.position)[1] + 1])).color != self.color:
							moves.append(enums.Move(name="Kx" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], functions.coordinateToIndex(self.position)[1] + 1]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], functions.coordinateToIndex(self.position)[1] + 1]), piece=self, is_capture=True))
					else:
						moves.append(enums.Move(name="K" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], functions.coordinateToIndex(self.position)[1] + 1]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], functions.coordinateToIndex(self.position)[1] + 1]), piece=self))
			if self.position[1] != "1":
				if not self.board.attackers(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1]]), enums.Color.invert(self.color)):
					if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1]])):
						if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1]])).color != self.color:
							moves.append(enums.Move(name="Kx" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1]]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1]]), piece=self, is_capture=True))
					else:
						moves.append(enums.Move(name="K" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1]]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1]]), piece=self))
			if self.position[1] != "8":
				if not self.board.attackers(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1]]), enums.Color.invert(self.color)):
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
		return moves if show_data else [i.name for i in moves]

	def __str__(self):
		return self.color.title() + " " + self.piece_type + " at " + self.position + " from " + repr(self.board)

	def __lt__(self, other):
		return enums.Piece.value(self.piece_type) < enums.Piece.value(other)

	def __le__(self, other):
		return enums.Piece.value(self.piece_type) <= enums.Piece.value(other)

	def __eq__(self, other):
		return {x: y for x, y in vars(self).items() if x != "board"} == {x: y for x, y in vars(other).items() if x != "board"}

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
		self.opening = ""  # Opening
		self.evaluate_openings = evaluate_openings
		self.squares, self.pieces = [], []  # Pieces and squares
		self.in_check = False  # False if neither side is in check, enums.Color.white if white is in check, otherwise enums.Color.black if black is in check
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
				Piece(functions.indexToCoordinate([i, x]), enums.Piece.pawn if y.lower() == "p" else enums.Piece.knight if y.lower() == "n" else enums.Piece.bishop if y.lower() == "b" else enums.Piece.rook if y.lower() == "r" else enums.Piece.queen if y.lower() == "q" else enums.Piece.king, enums.Color.white if y.isupper() else enums.Color.black, self)
		# Load opening
		if evaluate_opening:
			self.updateOpening()
		return True

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
		fen += " " + str(self.half_moves) + " " + str(self.full_moves)  # Add alfmove and fullmove clock
		return fen

	def error(self, error):
		"""Raises an error if allowed"""
		if self.raise_errors:
			raise error

	def move(self, move, evaluate_checks=True, evaluate_opening=True):
		"""Moves a piece"""
		# If move is a enums.Move object
		if isinstance(move, enums.Move):
			if move.is_capture:
				self.pieces.remove(self.pieceAt(move.new_position))
				self.captured_piece = True
			move.piece.position = move.new_position
			move.piece.moved = True
			if move.castle_rook:
				move.castle_rook.moved = True
				if move.castle == enums.Castle.kingside:
					move.castle_rook.position = "f" + move.castle_rook.position[1]
				else:
					move.castle_rook.position = "d" + move.castle_rook.position[1]
			self.en_passant_positions = None
			for i in self.pieces:
				i.en_passant = False
			if move.double_pawn_move:
				move.piece.en_passant = True
				self.en_passant_positions = move.new_position[0] + str(int(move.new_position[1]) - (1 if move.piece.color == enums.Color.white else -1))
			if move.en_passant:
				self.pieces.remove(self.pieceAt(move.en_passant_position))
				self.captured_piece = True
			if self.castling_rights is not None and move.piece.piece_type == enums.Piece.king:
				if move.piece.color == enums.Color.white:
					self.castling_rights = self.castling_rights.replace("K", "").replace("Q", "")
				else:
					self.castling_rights = self.castling_rights.replace("k", "").replace("q", "")
				if self.castling_rights == "":
					self.castling_rights = None
			if self.castling_rights is not None and move.piece.piece_type == enums.Piece.rook:
				if move.old_position == "a1":
					self.castling_rights = self.castling_rights.replace("Q", "")
				elif move.old_position == "a8":
					self.castling_rights = self.castling_rights.replace("q", "")
				elif move.old_position == "h1":
					self.castling_rights = self.castling_rights.replace("K", "")
				elif move.old_position == "h8":
					self.castling_rights = self.castling_rights.replace("k", "")
			self.raw_move_list.append(move)
			if evaluate_checks:
				if any([True for i in self.legal_moves(show_data=True, color=self.turn) if i.new_position == self.pieceType(enums.Piece.king, color=enums.Color.invert(self.turn))[0].position]):
					move += "+"
					self.in_check = enums.Color.invert(self.turn)
				else:
					self.in_check = False
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
			return move
		# If move is not a string, raise an error
		if not isinstance(move, str):
			self.error(errors.InvalidMove(move))
			return False
		# Convert to SAN if necessary
		move = functions.toSAN(move, self)
		# If move is not possible, raise an error
		if move not in self.legal_moves():
			self.error(errors.MoveNotPossible(move))
			return False
		move_data = None
		# Find the move data
		for i in self.legal_moves(True):
			if i.name == move:
				move_data = i
				if i.is_capture:
					self.pieces.remove(self.pieceAt(i.new_position))
					self.captured_piece = True
				i.piece.position = i.new_position
				i.piece.moved = True
				if i.castle_rook:
					i.castle_rook.moved = True
					if i.castle == enums.Castle.kingside:
						i.castle_rook.position = "f" + i.castle_rook.position[1]
					else:
						i.castle_rook.position = "d" + i.castle_rook.position[1]
				self.en_passant_positions = None
				for x in self.pieces:
					x.en_passant = False
				if i.double_pawn_move:
					i.piece.en_passant = True
					self.en_passant_positions = i.new_position[0] + str(int(i.new_position[1]) - (1 if i.piece.color == enums.Color.white else -1))
				if i.en_passant:
					self.pieces.remove(self.pieceAt(i.en_passant_position))
					self.captured_piece = True
				if self.castling_rights is not None and i.piece.piece_type == enums.Piece.king:
					if i.piece.color == enums.Color.white:
						self.castling_rights = self.castling_rights.replace("K", "").replace("Q", "")
					else:
						self.castling_rights = self.castling_rights.replace("k", "").replace("q", "")
					if self.castling_rights == "":
						self.castling_rights = None
				if self.castling_rights is not None and i.piece.piece_type == enums.Piece.rook:
					if i.old_position == "a1":
						self.castling_rights = self.castling_rights.replace("Q", "")
					elif i.old_position == "a8":
						self.castling_rights = self.castling_rights.replace("q", "")
					elif i.old_position == "h1":
						self.castling_rights = self.castling_rights.replace("K", "")
					elif i.old_position == "h8":
						self.castling_rights = self.castling_rights.replace("k", "")
				self.raw_move_list.append(i)
				break
		if evaluate_checks:
			if any([True for i in self.legal_moves(show_data=True, color=self.turn) if i.new_position == self.pieceType(enums.Piece.king, color=enums.Color.invert(self.turn))[0].position]):
				move += "+"
				self.in_check = enums.Color.invert(self.turn)
			else:
				self.in_check = False
		# Add move to move list and increase fullmove counter if necessary
		if self.turn == enums.Color.white:  # If white moved
			# Add move to move list
			if self.move_list == "":  # If there has not been any moves
				self.move_list += "1. " + move
			else:  # Otherwise
				self.move_list += " " + str(int(self.move_list.split(" ")[-3][0]) + 1) + ". " + move
		else:  # If black moved
			if self.move_list == "":  # Check for custom FENs
				self.move_list += "1. ... " + move  # Add move to move list
			else:
				self.move_list += " " + move  # Add move to move list
			self.full_moves += 1  # Increase fullmove counter
		# Calculate halfmove counter
		if i.is_capture or i.piece.piece_type == enums.Piece.pawn:  # Reset halfmove counter if the move is a pawn move or a capture
			self.half_moves = 0
		else:  # Otherwise, increase the halfmove counter by 1
			self.half_moves += 1
		self.turn = enums.Color.invert(self.turn)  # Invert turn
		# Get opening
		if evaluate_opening:
			self.updateOpening()
		return move_data

	def legal_moves(self, show_data=False, color=enums.Color.current, evaluate_checks=True):
		"""Returns all legal moves"""
		return [y for x in self.pieces if x.color == (self.turn if color == enums.Color.current else color) for y in x.moves(show_data, evaluate_checks=evaluate_checks)]

	def pieceType(self, piece, color=enums.Color.any):
		"""Returns all pieces with type `piece` and color `color`"""
		return [i for i in self.pieces if i.color in (["white", "black"] if color == enums.Color.any else [color]) and i.piece_type == piece]

	def gamePhase(self):
		"""Returns the current game phase"""
		if len(self.raw_move_list) // 2 <= 6 or not self.captured_piece:
			return enums.Phase.opening
		if not self.pieceType(enums.Piece.queen) or [i.piece.piece_type for i in self.raw_move_list].count(enums.Piece.king) > 3:
			return enums.Phase.endgame
		return enums.Phase.middlegame

	def totalMaterial(self):
		"""The total amount of material"""
		return sum(map(enums.Piece.value, [i for i in self.pieces if i.piece_type != enums.Piece.king]))

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
		return self.pieces[[i.position for i in self.pieces].index(coordinate)] if coordinate in [i.position for i in self.pieces] else None

	def takeback(self):
		"""Take backs one move. To take back multiple moves, call the function multiple times."""
		if not self.raw_move_list:
			return
		if self.raw_move_list[-1].is_capture:
			Piece(self.raw_move_list[-1].new_position, self.raw_move_list[-1].captured_piece.piece_type, self.raw_move_list[-1].captured_piece.color, self)
		self.raw_move_list[-1].piece.position = self.raw_move_list[-1].old_position
		self.raw_move_list.pop()
		if self.move_list.split(" ")[-2][-1] == ".":
			self.move_list = " ".join(self.move_list.split(" ")[:-2])
		else:
			self.move_list = " ".join(self.move_list.split(" ")[:-1])
		self.turn = enums.Color.invert(self.turn)
		self.en_passant_positions = None  # Reset en_passant_positions
		# Set opening
		if self.move_list == "":
			self.opening = ""
		else:
			self.updateOpening()

	def updateOpening(self):
		"""Updates the opening if evaluate_openings is True"""
		if self.evaluate_openings:
			opening = None
			for i in openings.openings:
				if i["position"] == self.FEN().split(" ")[0]:
					self.opening = i["eco"] + " " + i["name"]
					opening = i["eco"] + " " + i["name"]
					break
			else:
				return False
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
		"""Returns a list of the pieces that protect the coordinate"""
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
		elif enums.Color.isWhite(color):
			if position[0] not in "ah" and (return_all or (self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 1])) and self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 1])))):
				return [enums.Move(position[0] + "x" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 1]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 1]), piece, is_capture=True), enums.Move(position[0] + "x" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 1]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 1]), piece, is_capture=True)]
			if position[0] != "h" and self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 1])):
				return [enums.Move(position[0] + "x" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 1]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] + 1]), piece, is_capture=True)]
			if position[0] != "a" and self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 1])):
				return [enums.Move(position[0] + "x" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 1]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] - 1, functions.coordinateToIndex(position)[1] - 1]), piece, is_capture=True)]
		elif enums.Color.isBlack(color):
			if position[0] not in "ah" and (return_all or (self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 1])) and self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 1])))):
				return [enums.Move(position[0] + "x" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 1]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 1]), piece, is_capture=True), enums.Move(position[0] + "x" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 1]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 1]), piece, is_capture=True)]
			if position[0] != "h" and self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 1])):
				return [enums.Move(position[0] + "x" + functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 1]), position, functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] + 1]), piece, is_capture=True)]
			if position[0] != "a" and self.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(position)[0] + 1, functions.coordinateToIndex(position)[1] - 1])):
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
			return vars(obj) in map(vars, self.pieces)
		if isinstance(obj, Square):
			return vars(obj) in map(vars, self.squares)
		self.error(TypeError("Invalid type: " + str(obj)))
		return False

	def __unicode__(self):
		return "---------------------------------\n| " + (" |\n---------------------------------\n| ").join(" | ".join([y + ((" ") if y == "" else "") for y in x]) for x in [["".join([((enums.Piece.unicode(z.piece_type, z.color))) if functions.coordinateToIndex(z.position) == [x, y] else "" for z in self.pieces]) for y in range(len(self.squares[x]))] for x in range(len(self.squares))]) + " |\n---------------------------------"

	def __eq__(self, other):
		return self.FEN() == other.FEN()

	__add__ = __radd__ = __sub__ = __rsub__ = __mul__ = __rmul__ = __div__ = __rdiv__ = __truediv__ = __rtruediv__ = __floordiv__ = __rfloordiv__ = __mod__ = __rmod__ = __divmod__ = __rdivmod__ = __pow__ = __rpow__ = __lshift__ = __rlshift__ = __rshift__ = __rrshift__ = __and__ = __rand__ = __or__ = __ror__ = __xor__ = __rxor__ = __iadd__ = __isub__ = __imul__ = __idiv__ = __itruediv__ = __ifloordiv__ = __imod__ = __ipow__ = __iand__ = __ior__ = __ixor__ = __ilshift__ = __irshift__ = __neg__ = __pos__ = __abs__ = __invert__ = __int__ = __long__ = __float__ = __complex__ = __oct__ = __hex__ = __coerce__ = lambda self, *args: self.error(ArithmeticError("Cannot perform arithmetic operations on Game object"))

	__getitem__ = __setitem__ = __delitem__ = __getslice__ = __setslice__ = __delslice__ = lambda self, *args: self.error(IndexError("Cannot perform operation on Game object"))
