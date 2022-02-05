# -*- coding: utf-8 -*-

try:
	unicode
except NameError:
	unicode = str


def getMovesFromString(string):
	"""Returns a list of moves from a move string (e.g. '1. e4 e5 2. Nf3 Nc6 *')"""
	moves = []

	for i in string.split(" "):
		if i in ["*", "1-0", "0-1", "1/2-1/2"]:
			break
		if i[0].isnumeric():
			continue
		moves.append(i)

	return moves


def splitNumbers(string):
	"""Splits numbers in a string"""
	return "".join(["1" * int(i) if unicode(i).isnumeric() else i for i in string])


def combineNumbers(string):
	"""Combine numbers in a string"""
	if "1" not in string:
		return string
	if unicode(string).isnumeric():
		return sum(map(int, string))
	new_string = ""
	index = 0
	for i in range(len(string)):
		if not unicode(string[i]).isnumeric():
			new_string += str(combineNumbers(string[index:i])) + string[i]
			index = i + 1
	if unicode(string[-1]).isnumeric():
		new_string += str(combineNumbers(string[index:]))
	return new_string


def indexToCoordinate(index):
	"""Return a board coordinate (e.g. e4) from index (e.g. [4, 4])"""
	return ("a", "b", "c", "d", "e", "f", "g", "h")[index[1]] + str(abs(index[0] - 8))


def coordinateToIndex(coordinate):
	"""Return a raw index (e.g [4, 4]) from board coordinate (e.g. e4)"""
	return [abs(int(coordinate[1]) - 8), ("a", "b", "c", "d", "e", "f", "g", "h").index(coordinate[0])]


def coordinateValid(coordinate):
	"""Returns if the coordinate is valid"""
	return coordinate[0] in ["a", "b", "c", "d", "e", "f", "g", "h"] and coordinate[1] in ["1", "2", "3", "4", "5", "6", "7", "8"]


def toLAN(move, game):
	"""Return the move in long algebraic notation (e.g. e4 -> e2e4, Nf3 -> g1f3, e2e4 -> e2e4)"""
	trimmed_move = ""
	for i in move:
		if i in ["+", "#", "="]:
			break
		trimmed_move += i
	if move[0] in ["N", "B", "R", "Q", "K"]:
		for i in game.pieceType({"N": "knight", "B": "bishop", "R": "rook", "Q": "queen", "K": "king"}[move[0]]):
			if trimmed_move in i.moves():
				return i.position + move[1:]
		return move
	for i in game.pieceType("pawn"):
		if trimmed_move in i.moves():
			if "x" in trimmed_move:
				return i.position + move[1:]
			return i.position + move
	return move
	

def toSAN(move, game):
	"""Return the move in standard algebraic notation (e.g. e2e4 -> e4, g1f3 -> Nf3, e4 -> e4)"""
	extra_characters = ""  # Stores extra characters (e.g +,  #, =Q, =Q+...)
	if move in ["O-O", "0-0", "O-O-O", "0-0-0"]:
		return move.replace("0", "O")
	if move in ["O-O", "O-O-O"]:
		return move
	if move in ["o-o", "o-o-o"]:
		return move.replace("o", "O")
	if move.endswith("+"):  # If a "+" is found
		extra_characters = "+"
		move = move[:-1]
	if move.endswith("#"):  # If a "#" is found
		extra_characters = "#"
		move = move[:-1]
	if len(move) > 1:  # Check for "=N/B/R/Q"
		if move[-2] == "=" and move[-1] in ["N", "B", "R", "Q"]:
			extra_characters = move[-2:] + extra_characters
			move = move[:-2]
	if len(move) == 5:
		# Remove the hyphen if one is present (e2-e4 -> e2e4)
		if move[2] == "-":
			move = move[:2] + move[3:]
		# Check if the move is a capture (e.g. e4xd5)
		# If the middle character (move[2]) is "x", and the first two (move[:2]) and last two (move[3:])
		# characters are coordinates
		if move[2] == "x" and coordinateValid(move[:2].lower()) and coordinateValid(move[3:].lower()):
			if game.pieceAt(move[:2].lower()) is None:  # If the piece is not found, return move
				return move + extra_characters
			if game.pieceAt(move[:2].lower()).piece_type == "pawn":  # If the piece is a pawn
				return move[0] + "x" + move[3:] + extra_characters
			else:
				return {"knight": "N", "bishop": "B", "rook": "R", "queen": "Q", "king": "K"}[game.pieceAt(move[:2].lower()).piece_type] + "x" + move[3:] + extra_characters
	if len(move) == 4:
		# If the first two (move[:2]) and last two (move[2:]) characters are coordinates
		if coordinateValid(move[:2].lower()) and coordinateValid(move[2:].lower()):
			if game.pieceAt(move[:2].lower()) is None:  # If the piece is not found, return move
				return move + extra_characters
			if game.pieceAt(move[:2].lower()).piece_type == "king":  # If the piece is a king
				if game.pieceAt(move[:2].lower()).color == "white" and move[:2] == "e1":
					if move[2:] == "g1" and "K" in game.castling_rights:
						return "O-O"
					elif move[2:] == "c1" and "Q" in game.castling_rights:
						return "O-O-O"
				if game.pieceAt(move[:2].lower()).color == "black" and move[:2] == "e8":
					if move[2:] == "g8" and "k" in game.castling_rights:
						return "O-O"
					elif move[2:] == "c8" and "q" in game.castling_rights:
						return "O-O-O"
			if game.pieceAt(move[:2].lower()).piece_type == "pawn":  # If the piece is a pawn
				if game.pieceAt(move[2:].lower()) is not None:  # If the move is a capture
					return move[0] + "x" + move[2:] + extra_characters
				return move[2:] + extra_characters
			else:  # Otherwise
				if game.pieceAt(move[2:].lower()) is not None:  # If the move is a capture
					return {"knight": "N", "bishop": "B", "rook": "R", "queen": "Q", "king": "K"}[game.pieceAt(move[:2].lower()).piece_type] + "x" + move[2:] + extra_characters
				return {"knight": "N", "bishop": "B", "rook": "R", "queen": "Q", "king": "K"}[game.pieceAt(move[:2].lower()).piece_type] + move[2:] + extra_characters

	return move + extra_characters


def FENvalid(fen):
	"""Check if the FEN is valid"""
	if len(fen.split(" ")) < 6:  # If there are more that 6 space-separated entries
		return False
	if fen.split(" ")[0].count("/") != 7:  # If there is not exactly 7 "/" separators
		return False
	# Check the number of kings
	kings = []
	for x in fen.split(" ")[0].split("/"):
		if not all([y.lower() in "pnbrqk" or (unicode(y).isnumeric() and int(y) < 9) for y in x]) or len(splitNumbers(x)) != 8:
			return False
		if "k" in x:
			if x.count("k") > 1:
				kings.append("k")
			kings.append("k")
		if "K" in x:
			if x.count("K") > 1:
				kings.append("k")
			kings.append("K")
	if len(kings) > 2 or "k" not in kings or "K" not in kings:  # If there are more than two kings, or if there is more than one king of each color
		return False
	if fen.split(" ")[1] not in "wb":  # If the side to move is invalid
		return False
	if (fen.split(" ")[2] != "-" and (not all([i.lower() in "kq" for i in fen.split(" ")[2]]) or len(set(fen.split(" ")[2])) != len(fen.split(" ")[2]))) or (fen.split(" ")[3] != "-" and not coordinateValid(fen.split(" ")[3])) or not unicode(fen.split(" ")[4]).isnumeric() or not unicode(fen.split(" ")[5]).isnumeric():  # If the en passant squares or castling rights are invalid
		return False
	return True  # If all the checks pass, the FEN is valid


def isLine(pos1, pos2):
	"""Check if pos1 and pos2 form a horizontal, vertical, or diagonal line"""
	if pos1[0] == pos2[0] or pos1[1] == pos2[1]:  # If pos1 and pos2 form a vertical or horizontal line
		return True
	return abs(coordinateToIndex(pos1)[0] - coordinateToIndex(pos2)[0]) == abs(coordinateToIndex(pos1)[1] - coordinateToIndex(pos2)[1])  # If the distance between the files of pos1 and pos2 is equal to the distance between the ranks of pos1 and pos2, pos1 and pos2 form a diagonal line.
