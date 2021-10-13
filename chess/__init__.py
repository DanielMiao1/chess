# -*- coding: utf-8 -*-


"""
Local Imports
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
		board.pieces.append(self)
		self.position = position if isinstance(position, str) else functions.indexToCoordinate(position)
		self.piece_type, self.color, self.board = piece_type, color, board
		self.moved = False

	def moves(self, show_data=False):
		moves = []
		if self.piece_type == enums.Piece.pawn:  # Pawn moves
			# Straight pawn moves
			# Check if pawn is blocked
			for i in self.board.pieces:
				if functions.coordinateToIndex(i.position) == [functions.coordinateToIndex(self.position)[0] - (1 if self.color == enums.Color.white else -1), functions.coordinateToIndex(self.position)[1]]:
					break
			else:  # If pawn is not blocked
				moves.append(enums.Move(name=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - (1 if self.color == enums.Color.white else -1), functions.coordinateToIndex(self.position)[1]]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - (1 if self.color == enums.Color.white else -1), functions.coordinateToIndex(self.position)[1]]), piece=self))  # Append single pawn move
				# Check if pawn is on home rank
				if (int(self.position[1]) == 2 and self.color == enums.Color.white) or (int(self.position[1]) == 7 and self.color == enums.Color.black):
					# Check if pawn double move is blocked
					for i in self.board.pieces:
						if functions.coordinateToIndex(i.position) == [functions.coordinateToIndex(self.position)[0] - (2 if self.color == enums.Color.white else -2), functions.coordinateToIndex(self.position)[1]]:
							break
					else:  # If pawn double move is not blocked
						moves.append(enums.Move(name=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - (2 if self.color == enums.Color.white else -2), functions.coordinateToIndex(self.position)[1]]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - (2 if self.color == enums.Color.white else -2), functions.coordinateToIndex(self.position)[1]]), piece=self))  # Append double pawn move
			# Pawn captures
			capture_found = False  # Set default value of the capture_found variable
			if self.color == enums.Color.white:  # For white pawns
				# Check for left diagonal captures (e.g. e4xd5)
				for i in self.board.pieces:
					if functions.coordinateToIndex(i.position) == [x - 1 for x in functions.coordinateToIndex(self.position)] and i.color == enums.Color.black:
						capture_found = True  # Make capture_found True
						break
				if capture_found:  # If capture is found
					moves.append(enums.Move(name=functions.indexToCoordinate(functions.coordinateToIndex(self.position))[0] + "x" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] - 1]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] - 1]), piece=self, is_capture=True))  # Append pawn capture move
				capture_found = False  # Reset capture_found variable
				# Check for right diagonal captures (e.g. e4xf5)
				for i in self.board.pieces:
					if functions.coordinateToIndex(i.position) == [functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] + 1] and i.color == enums.Color.black:
						capture_found = True  # Make capture_found True
						break
				if capture_found:
					moves.append(enums.Move(name=functions.indexToCoordinate(functions.coordinateToIndex(self.position))[0] + "x" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] + 1]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] + 1]), piece=self, is_capture=True))  # Append pawn capture move
			else:  # For black pawns
				for i in self.board.pieces:
					if functions.coordinateToIndex(i.position) == [functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] - 1] and i.color == enums.Color.white:
						capture_found = True  # Make capture_found True
						break
				if capture_found:
					moves.append(enums.Move(name=functions.indexToCoordinate(functions.coordinateToIndex(self.position))[0] + "x" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] - 1]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] - 1]), piece=self, is_capture=True))  # Append pawn capture move
				capture_found = False  # Reset capture_found variable
				# Check for right diagonal captures (e.g. exf4)
				for i in self.board.pieces:
					if functions.coordinateToIndex(i.position) == [x + 1 for x in functions.coordinateToIndex(self.position)] and i.color == enums.Color.white:
						capture_found = True  # Make capture_found True
						break
				if capture_found:
					moves.append(enums.Move(name=functions.indexToCoordinate(functions.coordinateToIndex(self.position))[0] + "x" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] + 1]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] + 1]), piece=self, is_capture=True))  # Append pawn capture move
		elif self.piece_type == enums.Piece.knight:  # Knight moves
			found, valid = False, True
			if self.position[1] not in "78" and self.position[0] != "a":
				for i in self.board.pieces:
					if functions.coordinateToIndex(i.position) == [functions.coordinateToIndex(self.position)[0] - 2, functions.coordinateToIndex(self.position)[1] - 1]:
						if i.color == self.color:
							valid = False
						found = True
				if valid:
					moves.append(enums.Move(name="N" + ("x" if found else "") + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 2, functions.coordinateToIndex(self.position)[1] - 1]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 2, functions.coordinateToIndex(self.position)[1] - 1]), piece=self, is_capture=found))
			found, valid = False, True
			if self.position[1] not in "12" and self.position[0] != "a":
				for i in self.board.pieces:
					if functions.coordinateToIndex(i.position) == [functions.coordinateToIndex(self.position)[0] + 2, functions.coordinateToIndex(self.position)[1] - 1]:
						if i.color == self.color:
							valid = False
						found = True
				if valid:
					moves.append(enums.Move(name="N" + ("x" if found else "") + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 2, functions.coordinateToIndex(self.position)[1] - 1]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 2, functions.coordinateToIndex(self.position)[1] - 1]), piece=self, is_capture=found))
			found, valid = False, True
			if self.position[1] not in "78" and self.position[0] != "h":
				for i in self.board.pieces:
					if functions.coordinateToIndex(i.position) == [functions.coordinateToIndex(self.position)[0] - 2, functions.coordinateToIndex(self.position)[1] + 1]:
						if i.color == self.color:
							valid = False
						found = True
				if valid:
					moves.append(enums.Move(name="N" + ("x" if found else "") + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 2, functions.coordinateToIndex(self.position)[1] + 1]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 2, functions.coordinateToIndex(self.position)[1] + 1]), piece=self, is_capture=found))
			found, valid = False, True
			if self.position[1] not in "12" and self.position[0] != "h":
				for i in self.board.pieces:
					if functions.coordinateToIndex(i.position) == [functions.coordinateToIndex(self.position)[0] + 2, functions.coordinateToIndex(self.position)[1] + 1]:
						if i.color == self.color:
							valid = False
						found = True
				if valid:
					moves.append(enums.Move(name="N" + ("x" if found else "") + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 2, functions.coordinateToIndex(self.position)[1] + 1]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 2, functions.coordinateToIndex(self.position)[1] + 1]), piece=self, is_capture=found))
			found, valid = False, True
			if self.position[1] != "8" and self.position[0] not in "ab":
				for i in self.board.pieces:
					if functions.coordinateToIndex(i.position) == [functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] - 2]:
						if i.color == self.color:
							valid = False
						found = True
				if valid:
					moves.append(enums.Move(name="N" + ("x" if found else "") + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] - 2]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] - 2]), piece=self, is_capture=found))
			found, valid = False, True
			if self.position[1] != "1" and self.position[0] not in "ab":
				for i in self.board.pieces:
					if functions.coordinateToIndex(i.position) == [functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] - 2]:
						if i.color == self.color:
							valid = False
						found = True
				if valid:
					moves.append(enums.Move(name="N" + ("x" if found else "") + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] - 2]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] - 2]), piece=self, is_capture=found))
			found, valid = False, True
			if self.position[1] != "1" and self.position[0] not in "gh":
				for i in self.board.pieces:
					if functions.coordinateToIndex(i.position) == [functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] + 2]:
						if i.color == self.color:
							valid = False
						found = True
				if valid:
					moves.append(enums.Move(name="N" + ("x" if found else "") + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] + 2]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] + 2]), piece=self, is_capture=found))
			found, valid = False, True
			if self.position[1] != "8" and self.position[0] not in "gh":
				for i in self.board.pieces:
					if functions.coordinateToIndex(i.position) == [functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] + 2]:
						if i.color == self.color:
							valid = False
						found = True
				if valid:
					moves.append(enums.Move(name="N" + ("x" if found else "") + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] + 2]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] + 2]), piece=self, is_capture=found))
		elif self.piece_type == enums.Piece.bishop:  # Bishop moves
			capture = False
			pos1, pos2 = functions.coordinateToIndex(self.position)
			while pos1 != 0 and pos2 != 0:
				pos1, pos2 = pos1 - 1, pos2 - 1
				for i in self.board.pieces:
					if functions.coordinateToIndex(i.position) == [pos1, pos2]:
						if i.color == self.color:
							break
						capture = True
				else:
					moves.append(enums.Move(name="B" + ("x" if capture else "") + functions.indexToCoordinate([pos1, pos2]), old_position=self.position, new_position=functions.indexToCoordinate([pos1, pos2]), piece=self, is_capture=capture))
					if capture:
						break
					continue
				break
			capture = False
			pos1, pos2 = functions.coordinateToIndex(self.position)
			while pos1 != 7 and pos2 != 7:
				pos1, pos2 = pos1 + 1, pos2 + 1
				for i in self.board.pieces:
					if functions.coordinateToIndex(i.position) == [pos1, pos2]:
						if i.color == self.color:
							break
						capture = True
				else:
					moves.append(enums.Move(name="B" + ("x" if capture else "") + functions.indexToCoordinate([pos1, pos2]), old_position=self.position, new_position=functions.indexToCoordinate([pos1, pos2]), piece=self, is_capture=capture))
					if capture:
						break
					continue
				break
			capture = False
			pos1, pos2 = functions.coordinateToIndex(self.position)
			while pos1 != 0 and pos2 != 7:
				pos1, pos2 = pos1 - 1, pos2 + 1
				for i in self.board.pieces:
					if functions.coordinateToIndex(i.position) == [pos1, pos2]:
						if i.color == self.color:
							break
						capture = True
				else:
					moves.append(enums.Move(name="B" + ("x" if capture else "") + functions.indexToCoordinate([pos1, pos2]), old_position=self.position, new_position=functions.indexToCoordinate([pos1, pos2]), piece=self, is_capture=capture))
					if capture:
						break
					continue
				break
			capture = False
			pos1, pos2 = functions.coordinateToIndex(self.position)
			while pos1 != 7 and pos2 != 0:
				pos1, pos2 = pos1 + 1, pos2 - 1
				for i in self.board.pieces:
					if functions.coordinateToIndex(i.position) == [pos1, pos2]:
						if i.color == self.color:
							break
						capture = True
				else:
					moves.append(enums.Move(name="B" + ("x" if capture else "") + functions.indexToCoordinate([pos1, pos2]), old_position=self.position, new_position=functions.indexToCoordinate([pos1, pos2]), piece=self, is_capture=capture))
					if capture:
						break
					continue
				break
		if self.piece_type == enums.Piece.rook:  # Rook moves
			capture = False
			for x in reversed(range(functions.coordinateToIndex(self.position)[0])):
				for y in self.board.pieces:
					if functions.coordinateToIndex(y.position) == [x, functions.coordinateToIndex(self.position)[1]]:
						if y.color == self.color:
							break
						capture = True
				else:
					moves.append(enums.Move(name="R" + ("x" if capture else "") + functions.indexToCoordinate([x, functions.coordinateToIndex(self.position)[1]]), old_position=self.position, new_position=functions.indexToCoordinate([x, functions.coordinateToIndex(self.position)[1]]), piece=self, is_capture=capture))
					if capture:
						break
					continue
				break
			capture = False
			for x in reversed(range(functions.coordinateToIndex(self.position)[1])):
				for y in self.board.pieces:
					if functions.coordinateToIndex(y.position) == [functions.coordinateToIndex(self.position)[0], x]:
						if y.color == self.color:
							break
						capture = True
				else:
					moves.append(enums.Move(name="R" + ("x" if capture else "") + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], x]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], x]), piece=self, is_capture=capture))
					if capture:
						break
					continue
				break
			capture = False
			for x in range(functions.coordinateToIndex(self.position)[0] + 1, 8):
				for y in self.board.pieces:
					if functions.coordinateToIndex(y.position) == [x, functions.coordinateToIndex(self.position)[1]]:
						if y.color == self.color:
							break
						capture = True
				else:
					moves.append(enums.Move(name="R" + ("x" if capture else "") + functions.indexToCoordinate([x, functions.coordinateToIndex(self.position)[1]]), old_position=self.position, new_position=functions.indexToCoordinate([x, functions.coordinateToIndex(self.position)[1]]), piece=self, is_capture=capture))
					if capture:
						break
					continue
				break
			capture = False
			for x in range(functions.coordinateToIndex(self.position)[1] + 1, 8):
				for y in self.board.pieces:
					if functions.coordinateToIndex(y.position) == [functions.coordinateToIndex(self.position)[0], x]:
						if y.color == self.color:
							break
						capture = True
				else:
					moves.append(enums.Move(name="R" + ("x" if capture else "") + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], x]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], x]), piece=self, is_capture=capture))
					if capture:
						break
					continue
				break
		elif self.piece_type == "queen":  # Queen moves
			capture = False
			pos1, pos2 = functions.coordinateToIndex(self.position)
			while pos1 != 0 and pos2 != 0:
				pos1, pos2 = pos1 - 1, pos2 - 1
				for i in self.board.pieces:
					if functions.coordinateToIndex(i.position) == [pos1, pos2]:
						if i.color == self.color:
							break
						capture = True
				else:
					moves.append(enums.Move(name="Q" + ("x" if capture else "") + functions.indexToCoordinate([pos1, pos2]), old_position=self.position, new_position=functions.indexToCoordinate([pos1, pos2]), piece=self, is_capture=capture))
					if capture:
						break
					continue
				break
			capture = False
			pos1, pos2 = functions.coordinateToIndex(self.position)
			while pos1 != 7 and pos2 != 7:
				pos1, pos2 = pos1 + 1, pos2 + 1
				for i in self.board.pieces:
					if functions.coordinateToIndex(i.position) == [pos1, pos2]:
						if i.color == self.color:
							break
						capture = True
				else:
					moves.append(enums.Move(name="Q" + ("x" if capture else "") + functions.indexToCoordinate([pos1, pos2]), old_position=self.position, new_position=functions.indexToCoordinate([pos1, pos2]), piece=self, is_capture=capture))
					if capture:
						break
					continue
				break
			capture = False
			pos1, pos2 = functions.coordinateToIndex(self.position)
			while pos1 != 0 and pos2 != 7:
				pos1, pos2 = pos1 - 1, pos2 + 1
				for i in self.board.pieces:
					if functions.coordinateToIndex(i.position) == [pos1, pos2]:
						if i.color == self.color:
							break
						capture = True
				else:
					moves.append(enums.Move(name="Q" + ("x" if capture else "") + functions.indexToCoordinate([pos1, pos2]), old_position=self.position, new_position=functions.indexToCoordinate([pos1, pos2]), piece=self, is_capture=capture))
					if capture:
						break
					continue
				break
			capture = False
			pos1, pos2 = functions.coordinateToIndex(self.position)
			while pos1 != 7 and pos2 != 0:
				pos1, pos2 = pos1 + 1, pos2 - 1
				for i in self.board.pieces:
					if functions.coordinateToIndex(i.position) == [pos1, pos2]:
						if i.color == self.color:
							break
						capture = True
				else:
					moves.append(enums.Move(name="Q" + ("x" if capture else "") + functions.indexToCoordinate([pos1, pos2]), old_position=self.position, new_position=functions.indexToCoordinate([pos1, pos2]), piece=self, is_capture=capture))
					if capture:
						break
					continue
				break
			capture = False
			for x in reversed(range(functions.coordinateToIndex(self.position)[0])):
				for y in self.board.pieces:
					if functions.coordinateToIndex(y.position) == [x, functions.coordinateToIndex(self.position)[1]]:
						if y.color == self.color:
							break
						capture = True
				else:
					moves.append(enums.Move(name="Q" + ("x" if capture else "") + functions.indexToCoordinate([x, functions.coordinateToIndex(self.position)[1]]), old_position=self.position, new_position=functions.indexToCoordinate([x, functions.coordinateToIndex(self.position)[1]]), piece=self, is_capture=capture))
					if capture:
						break
					continue
				break
			capture = False
			for x in reversed(range(functions.coordinateToIndex(self.position)[1])):
				for y in self.board.pieces:
					if functions.coordinateToIndex(y.position) == [functions.coordinateToIndex(self.position)[0], x]:
						if y.color == self.color:
							break
						capture = True
				else:
					moves.append(enums.Move(name="Q" + ("x" if capture else "") + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], x]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], x]), piece=self, is_capture=capture))
					if capture:
						break
					continue
				break
			capture = False
			for x in range(functions.coordinateToIndex(self.position)[0] + 1, 8):
				for y in self.board.pieces:
					if functions.coordinateToIndex(y.position) == [x, functions.coordinateToIndex(self.position)[1]]:
						if y.color == self.color:
							break
						capture = True
				else:
					moves.append(enums.Move(name="Q" + ("x" if capture else "") + functions.indexToCoordinate([x, functions.coordinateToIndex(self.position)[1]]), old_position=self.position, new_position=functions.indexToCoordinate([x, functions.coordinateToIndex(self.position)[1]]), piece=self, is_capture=capture))
					if capture:
						break
					continue
				break
			capture = False
			for x in range(functions.coordinateToIndex(self.position)[1] + 1, 8):
				for y in self.board.pieces:
					if functions.coordinateToIndex(y.position) == [functions.coordinateToIndex(self.position)[0], x]:
						if y.color == self.color:
							break
						capture = True
				else:
					moves.append(enums.Move(name="Q" + ("x" if capture else "") + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], x]), old_position=self.position, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], x]), piece=self, is_capture=capture))
					if capture:
						break
					continue
				break
		elif self.piece_type == enums.Piece.king:
			if self.position[0] != "h" and self.position[1] != "1":
				if not self.board.attackers(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] + 1]), enums.Color.invert(self.color)):
					if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] + 1])):
						if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] + 1])).color != self.color:
							moves.append(enums.Move(name="Kx" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] + 1]), old_position=self, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] + 1]), piece=self, is_capture=True))
					else:
						moves.append(enums.Move(name="K" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] + 1]), old_position=self, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] + 1]), piece=self))
			if self.position[0] != "a" and self.position[1] != "8":
				if not self.board.attackers(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] - 1]), enums.Color.invert(self.color)):
					if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] - 1])):
						if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] - 1])).color != self.color:
							moves.append(enums.Move(name="Kx" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] - 1]), old_position=self, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] - 1]), piece=self, is_capture=True))
					else:
						moves.append(enums.Move(name="K" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] - 1]), old_position=self, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] - 1]), piece=self))
			if self.position[0] != "a" and self.position[1] != "1":
				if not self.board.attackers(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] - 1]), enums.Color.invert(self.color)):
					if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] - 1])):
						if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] - 1])).color != self.color:
							moves.append(enums.Move(name="Kx" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] - 1]), old_position=self, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] - 1]), piece=self, is_capture=True))
					else:
						moves.append(enums.Move(name="K" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] - 1]), old_position=self, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1] - 1]), piece=self))
			if self.position[0] != "h" and self.position[1] != "8":
				if not self.board.attackers(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] + 1]), enums.Color.invert(self.color)):
					if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] + 1])):
						if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] + 1])).color != self.color:
							moves.append(enums.Move(name="Kx" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] + 1]), old_position=self, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] + 1]), piece=self, is_capture=True))
					else:
						moves.append(enums.Move(name="K" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] + 1]), old_position=self, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1] + 1]), piece=self))
			if self.position[0] != "a":
				if not self.board.attackers(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], functions.coordinateToIndex(self.position)[1] - 1]), enums.Color.invert(self.color)):
					if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], functions.coordinateToIndex(self.position)[1] - 1])):
						if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], functions.coordinateToIndex(self.position)[1] - 1])).color != self.color:
							moves.append(enums.Move(name="Kx" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], functions.coordinateToIndex(self.position)[1] - 1]), old_position=self, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], functions.coordinateToIndex(self.position)[1] - 1]), piece=self, is_capture=True))
					else:
						moves.append(enums.Move(name="K" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], functions.coordinateToIndex(self.position)[1] - 1]), old_position=self, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], functions.coordinateToIndex(self.position)[1] - 1]), piece=self))
			if self.position[0] != "h":
				if not self.board.attackers(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], functions.coordinateToIndex(self.position)[1] + 1]), enums.Color.invert(self.color)):
					if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], functions.coordinateToIndex(self.position)[1] + 1])):
						if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], functions.coordinateToIndex(self.position)[1] + 1])).color != self.color:
							moves.append(enums.Move(name="Kx" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], functions.coordinateToIndex(self.position)[1] + 1]), old_position=self, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], functions.coordinateToIndex(self.position)[1] + 1]), piece=self, is_capture=True))
					else:
						moves.append(enums.Move(name="K" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], functions.coordinateToIndex(self.position)[1] + 1]), old_position=self, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0], functions.coordinateToIndex(self.position)[1] + 1]), piece=self))
			if self.position[1] != "1":
				if not self.board.attackers(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1]]), enums.Color.invert(self.color)):
					if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1]])):
						if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1]])).color != self.color:
							moves.append(enums.Move(name="Kx" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1]]), old_position=self, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1]]), piece=self, is_capture=True))
					else:
						moves.append(enums.Move(name="K" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1]]), old_position=self, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] + 1, functions.coordinateToIndex(self.position)[1]]), piece=self))
			if self.position[1] != "8":
				if not self.board.attackers(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1]]), enums.Color.invert(self.color)):
					if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1]])):
						if self.board.pieceAt(functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1]])).color != self.color:
							moves.append(enums.Move(name="Kx" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1]]), old_position=self, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1]]), piece=self, is_capture=True))
					else:
						moves.append(enums.Move(name="K" + functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1]]), old_position=self, new_position=functions.indexToCoordinate([functions.coordinateToIndex(self.position)[0] - 1, functions.coordinateToIndex(self.position)[1]]), piece=self))
		return moves if show_data else [i.name for i in moves]

	def __str__(self):
		return self.color.title() + " " + self.piece_type + " at " + self.position + " from " + repr(self.board)

	def __lt__(self, other):
		return enums.Piece.value(self.piece_type) < enums.Piece.value(other)

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


class Game:
	"""Game class"""
	def __init__(self, raise_errors=True, fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
		"""Initialize"""
		if not functions.FENvalid(fen):
			fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
		self.opening = ""  # Opening
		self.squares, self.pieces = [], []  # Pieces and squares
		self.in_check = False  # False if neither side is in check, enums.Color.white if white is in check, otherwise enums.Color.black if black is in check
		# Append squares
		for x in range(8):
			self.squares.append([Square([x, y], self) for y in range(8)])
		self.raise_errors = raise_errors  # Raise errors
		# Load FEN-specific values
		self.loadFEN(fen)

	def loadFEN(self, fen):
		"""Load/Reload with the specified FEN"""
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
		# Add pieces
		for i, j in enumerate(functions.splitNumbers(fen.split(" ")[0]).split("/")):
			for x, y in enumerate(j):
				if unicode(y).isnumeric():
					continue
				Piece(functions.indexToCoordinate([i, x]), enums.Piece.pawn if y.lower() == "p" else enums.Piece.knight if y.lower() == "n" else enums.Piece.bishop if y.lower() == "b" else enums.Piece.rook if y.lower() == "r" else enums.Piece.queen if y.lower() == "q" else enums.Piece.king, enums.Color.white if y.isupper() else enums.Color.black, self)
		# Load opening
		for i in openings.openings:
			if i["fen"] == " ".join(fen.split(" ")[:2]):
				self.opening = i["eco"] + " " + i["name"]

	def loadOpening(self, opening_name):
		"""Load an opening"""
		for i in openings.openings:
			if opening_name.lower().replace("king's pawn game", "open game").replace("queen's pawn game", "closed game").replace("russian game", "petrov's defense") in [i["name"].lower(), i["eco"].lower() + " " + i["name"].lower(), i["eco"].lower() + i["name"].lower(), i["eco"].lower().replace("'", ""), i["eco"].lower() + " " + i["name"].lower().replace("'", ""), i["eco"].lower() + i["name"].lower().replace("'", "")]:
				self.loadFEN(i["fen"] + " - - 0 0")
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
		fen += " -"  # TODO: Castling rights
		fen += " -"  # TODO: En Passant captures
		fen += " " + str(self.half_moves) + " " + str(self.full_moves)  # Add alfmove and fullmove clock
		return fen

	def error(self, error):
		"""Raises an error if allowed"""
		if self.raise_errors:
			raise error

	def move(self, move):
		"""Moves a piece"""
		# If move is a enums.Move object, then redefine move as the name of move
		if isinstance(move, enums.Move):
			move = move.name
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
		# Find the move data
		for i in self.legal_moves(True):
			if i.name == move and i.piece.color == self.turn:
				if i.is_capture:
					self.pieces.remove(self.pieceAt(i.new_position))
					self.captured_piece = True
				i.piece.position = i.new_position
				i.piece.moved = True
				self.raw_move_list.append(i)
				break
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
		for i in openings.openings:
			if i["fen"] == " ".join(self.FEN().split(" ")[:2]) or i["moves"] == self.move_list:
				self.opening = i["eco"] + " " + i["name"]

	def legal_moves(self, show_data=False, color=enums.Color.current):
		"""Returns all legal moves"""
		return [y for x in self.pieces if x.color == (self.turn if color == enums.Color.current else color) for y in x.moves(show_data)]

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

	def materialDifference(self):
		"""Returns the material difference. Positive values indicate white has more material, while negative values indicate black has more."""
		difference = 0
		for i in enums.Piece.all():
			if i == enums.Piece.king:
				continue
			difference += sum([enums.Piece.value(x.piece_type) for x in self.pieceType(i, enums.Color.white)]) - sum([enums.Piece.value(x.piece_type) for x in self.pieceType(i, enums.Color.black)])
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
			self.pieces.append(Piece(self.raw_move_list[-1].new_position, self.raw_move_list[-1].captured_piece.piece_type, self.raw_move_list[-1].captured_piece.color, self))
		self.raw_move_list[-1].piece.position = self.raw_move_list[-1].old_position
		self.raw_move_list.pop()
		if self.move_list.split(" ")[-2][-1] == ".":
			self.move_list = " ".join(self.move_list.split(" ")[:-2])
		else:
			self.move_list = " ".join(self.move_list.split(" ")[:-1])
		self.turn = enums.Color.invert(self.turn)
		if self.move_list == "":
			self.opening = ""
		else:
			for i in openings.openings:
				if i["fen"] == " ".join(self.FEN().split(" ")[:2]) or i["moves"] == self.move_list:
					self.opening = i["eco"] + " " + i["name"]

	def attackers(self, coordinate, color):
		"""Returns the pieces that attack the coordinate"""
		if color not in [enums.Color.white, enums.Color.black]:
			self.error(errors.UndefinedColor(color))
		attackers = []
		for i in self.pieces:
			if i.color != color:
				continue
			if i.piece_type == enums.Piece.pawn:
				if functions.coordinateToIndex(coordinate) in [[functions.coordinateToIndex(i.position)[0] - (1 if i.color == enums.Color.white else -1), functions.coordinateToIndex(i.position)[1] - 1], [functions.coordinateToIndex(i.position)[0] - (1 if i.color == enums.Color.white else -1), functions.coordinateToIndex(i.position)[1] + 1]]:
					attackers.append(i)
			elif i.piece_type == enums.Piece.king:
				if functions.coordinateToIndex(coordinate) in [[functions.coordinateToIndex(i.position)[0] - 1, functions.coordinateToIndex(i.position)[1] - 1], [functions.coordinateToIndex(i.position)[0] - 1, functions.coordinateToIndex(i.position)[1]], [functions.coordinateToIndex(i.position)[0] - 1, functions.coordinateToIndex(i.position)[1] + 1], [functions.coordinateToIndex(i.position)[0], functions.coordinateToIndex(i.position)[1] - 1], [functions.coordinateToIndex(i.position)[0], functions.coordinateToIndex(i.position)[1] + 1], [functions.coordinateToIndex(i.position)[0] + 1, functions.coordinateToIndex(i.position)[1] - 1], [functions.coordinateToIndex(i.position)[0] + 1, functions.coordinateToIndex(i.position)[1]], [functions.coordinateToIndex(i.position)[0] + 1, functions.coordinateToIndex(i.position)[1] + 1]]:
					attackers.append(i)
			elif any([coordinate in x for x in i.moves()]):
				attackers.append(i)
		return attackers

	def visualized(self, use_unicode=True, empty_squares=" ", separators=True):
		return (("---------------------------------\n| " if use_unicode else "-----------------------------------------\n| ") + (" |\n---------------------------------\n| " if use_unicode else " |\n-----------------------------------------\n| ").join(" | ".join([y + ((empty_squares if use_unicode else empty_squares + " ") if y == "" else "") for y in x]) for x in [["".join([((enums.Piece.unicode(z.piece_type, z.color)) if use_unicode else (z.color[0].upper() + (z.piece_type[0].upper() if z.piece_type != "knight" else "N"))) if functions.coordinateToIndex(z.position) == [x, y] else "" for z in self.pieces]) for y in range(len(self.squares[x]))] for x in range(len(self.squares))]) + (" |\n---------------------------------" if use_unicode else " |\n-----------------------------------------")) if separators else ("\n".join(" ".join([y + ((empty_squares if use_unicode else empty_squares + " ") if y == "" else "") for y in x]) for x in [["".join([((enums.Piece.unicode(z.piece_type, z.color)) if use_unicode else (z.color[0].upper() + (z.piece_type[0].upper() if z.piece_type != "knight" else "N"))) if functions.coordinateToIndex(z.position) == [x, y] else "" for z in self.pieces]) for y in range(len(self.squares[x]))] for x in range(len(self.squares))]))

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
