"""
ChessLibrary.py
Main Python 3 File
"""

import enums
import errors
import functions


class Square:
	def __init__(self, position, board):
		self.position = functions.indexToCoordinate(position)
		self.board = board
		if ((position[0] + position[1]) & 1) == 0:
			self.color = enums.Color.white
		else:
			self.color = enums.Color.black

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


class Piece:
	def __init__(self, position, piece_type, color, board):
		self.position = functions.indexToCoordinate(position)
		self.piece_type, self.color, self.board = piece_type, color, board

	def moves(self, show_data=False):
		moves = []
		if self.piece_type == enums.Piece.pawn:  # Pawn moves
			# Straight pawn moves
			# # Check if pawn is blocked
			for i in self.board.pieces:
				if functions.coordinateToIndex(i.position) == [functions.coordinateToIndex(self.position)[0] - (1 if self.color == enums.Color.white else -1), functions.coordinateToIndex(self.position)[1]]:
					break
			else:  # If pawn is not blocked
				if show_data:
					moves.append(enums.Move(name=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - (1 if self.color == enums.Color.white else -1), functions.coordinateToIndex(self.position)[1]]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - (1 if self.color == enums.Color.white else -1), functions.coordinateToIndex(self.position)[1]]), piece=self))  # Append single pawn move
				else:
					moves.append(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - (1 if self.color == enums.Color.white else -1), functions.coordinateToIndex(self.position)[1]]))  # Append single pawn move
				# Check if pawn is on home rank
				if (int(self.position[1]) == 2 and self.color == enums.Color.white) or (int(self.position[1]) == 7 and self.color == enums.Color.black):
					# Check if pawn double move is blocked
					for i in self.board.pieces:
						if int(i.position[1]) == int(self.position[1]) + (2 if self.color == enums.Color.white else -2):
							break
					else:  # If pawn double move is not blocked
						if show_data:
							moves.append(enums.Move(name=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - (2 if self.color == enums.Color.white else -2), functions.coordinateToIndex(self.position)[1]]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - (2 if self.color == enums.Color.white else -2), functions.coordinateToIndex(self.position)[1]]), piece=self))  # Append double pawn move
						else:
							moves.append(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - (2 if self.color == enums.Color.white else -2), functions.coordinateToIndex(self.position)[1]]))  # Append double pawn move
			# Pawn captures
			capture_found = False  # Set default value of the capture_found variable
			if self.color == enums.Color.white:  # For white pawns
				# Check for left diagonal captures (e.g. e4xd5)
				for i in self.board.pieces:
					if functions.coordinateToIndex(i.position) == [i - 1 for i in functions.coordinateToIndex(self.position)] and i.color == enums.Color.black:
						capture_found = True  # Make capture_found True
						break
				if capture_found:  # If capture is found
					if show_data:
						moves.append(enums.Move(name=functions.indexToCoordinate(functions.coordinateToIndex(self.position))[0] + "x" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] - 1]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] - 1]), piece=self))  # Append pawn capture move
					else:
						moves.append(enums.Move(name=functions.indexToCoordinate(functions.coordinateToIndex(self.position))[0] + "x" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] - 1]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] - 1]), piece=self))  # Append pawn capture move
				capture_found = False  # Reset capture_found variable
				# Check for right diagonal captures (e.g. e4xf5)
				for i in self.board.pieces:
					if functions.coordinateToIndex(i.position) == [functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] + 1] and i.color == enums.Color.black:
						capture_found = True  # Make capture_found True
						break
				if capture_found:
					if show_data:
						moves.append(enums.Move(name=functions.indexToCoordinate(functions.coordinateToIndex(self.position))[0] + "x" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] + 1]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] + 1]), piece=self))  # Append pawn capture move
					else:
						moves.append(functions.indexToCoordinate(functions.coordinateToIndex(self.position))[0] + "x" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] + 1]))  # Append pawn capture move
			else:  # For black pawns
				for i in self.board.pieces:
					if functions.coordinateToIndex(i.position) == [functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] - 1] and i.color == enums.Color.white:
						capture_found = True  # Make capture_found True
						break
				if capture_found:
					if show_data:
						moves.append(enums.Move(name=functions.indexToCoordinate(functions.coordinateToIndex(self.position))[0] + "x" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] - 1]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] - 1]), piece=self))  # Append pawn capture move
					else:
						moves.append(functions.indexToCoordinate(functions.coordinateToIndex(self.position))[0] + "x" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] - 1]))  # Append pawn capture move
				capture_found = False  # Reset capture_found variable
				# Check for right diagonal captures (e.g. exf4)
				for i in self.board.pieces:
					if functions.coordinateToIndex(i.position) == [i + 1 for i in functions.coordinateToIndex(self.position)] and i.color == enums.Color.white:
						capture_found = True  # Make capture_found True
						break
				if capture_found:
					if show_data:
						moves.append(enums.Move(name=functions.indexToCoordinate(functions.coordinateToIndex(self.position))[0] + "x" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] + 1]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] + 1]))) # Append pawn capture move
					else:
						moves.append(functions.indexToCoordinate(functions.coordinateToIndex(self.position))[0] + "x" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] + 1])) # Append pawn capture move
		return moves

	def __str__(self):
		return self.color.title() + " " + self.piece_type[0] + " at " + self.position + " from " + repr(self.board)

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
	def __init__(self, raise_errors=True):
		"""Initialize"""
		self.turn = enums.Color.white
		self.squares, self.pieces = [], []
		for x in range(8):
			row = []
			for y in range(8):
				row.append(Square([x, y], self))
				if x in [0, 7]:
					if y in [0, 7]:
						self.pieces.append(Piece([x, y], enums.Piece.rook, enums.Color.black if x == 0 else enums.Color.white, self))
					elif y in [1, 6]:
						self.pieces.append(Piece([x, y], enums.Piece.knight, enums.Color.black if x == 0 else enums.Color.white, self))
					elif y in [2, 5]:
						self.pieces.append(Piece([x, y], enums.Piece.bishop, enums.Color.black if x == 0 else enums.Color.white, self))
					elif y == 3:
						self.pieces.append(Piece([x, y], enums.Piece.queen, enums.Color.black if x == 0 else enums.Color.white, self))
					elif y == 4:
						self.pieces.append(Piece([x, y], enums.Piece.king, enums.Color.black if x == 0 else enums.Color.white, self))
				elif x in [1, 6]:
					self.pieces.append(Piece([x, y], enums.Piece.pawn, enums.Color.black if x == 1 else enums.Color.white, self))
			self.squares.append(row)
		self.raise_errors = raise_errors

	def FEN(self):
		"""Returns the FEN of the game"""
		return "(FEN TEXT)"

	def error(self, error):
		"""Raises an error if allowed"""
		if self.raise_errors:
			raise error

	def move(self, move):
		"""Moves a piece"""
		if isinstance(move, enums.Move):
			move = move.name
		if not isinstance(move, str):
			self.error(errors.InvalidMove(move))
		move = functions.toSAN(move, self)
		if move not in self.legal_moves():
			self.error(errors.MoveNotPossible(move))
		for i in self.legal_moves(True):
			if i.name == move:
				if i.is_capture:
					self.pieces.remove(self.pieceAt(i.new_position))
				i.piece.position = i.new_position
		self.turn = (enums.Color.white, enums.Color.black)[self.turn == enums.Color.white]

	def legal_moves(self, show_data=False):
		"""Returns all legal moves"""
		return [x for i in self.pieces for x in i.moves(show_data)]

	def pieceAt(self, coordinate):
		"""Returns the piece at coordinate if one exists, otherwise return None"""
		return self.pieces[[i.position for i in self.pieces].index(coordinate)] if coordinate in [i.position for i in self.pieces] else None

	def visualized(self, use_unicode=True):
		return ("---------------------------------\n| " if use_unicode else "-----------------------------------------\n| ") + (" |\n---------------------------------\n| " if use_unicode else " |\n-----------------------------------------\n| ").join(" | ".join([y + ((" " if use_unicode else "  ") if y == "" else "") for y in x]) for x in [["".join([(({"whiteking": "♔", "blackking": "♚", "whitequeen": "♕", "blackqueen": "♛", "whiterook": "♖", "blackrook": "♜", "whitebishop": "♗", "blackbishop": "♝", "whiteknight": "♘", "blackknight": "♞", "whitepawn": "♙", "blackpawn": "♟"}[z.color + z.piece_type[0]]) if use_unicode else (z.color[0].upper() + (z.piece_type[0][0].upper() if z.piece_type[0] != "knight" else "N"))) if functions.coordinateToIndex(z.position) == [x, y] else "" for z in self.pieces]) for y in range(len(self.squares[x]))] for x in range(len(self.squares))]) + (" |\n---------------------------------" if use_unicode else " |\n-----------------------------------------")

	def __str__(self):
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
