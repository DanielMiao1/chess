# -*- coding: utf-8 -*-


"""
functions.py
Functions
"""

try:
	unicode
except NameError:
	unicode = str


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
	"""Returns if the coordinate is valid (e.g. e4 -> True, 4e -> False)"""
	return coordinate[0] in ["a", "b", "c", "d", "e", "f", "g", "h"] and coordinate[1] in ["1", "2", "3", "4", "5", "6", "7", "8"]

def toSAN(move, game):
	"""Return the move in standard algebraic notation (e.g. e2e4 -> e4, g1f3 -> Nf3, e4 -> e4)"""
	extra_characters = ""  # Stores extra characters (e.g +,  #, =Q, =Q+...)
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
			if game.pieceAt(move[:2].lower()).piece_type[0] == "pawn":  # If the piece is a pawn
				return move[0] + "x" + move[3:] + extra_characters
			else:
				return {"knight": "N", "bishop": "B", "rook": "R", "queen": "Q", "king": "K"}[game.pieceAt(move[:2].lower()).piece_type[0]] + "x" + move[3:] + extra_characters
	if len(move) == 4:  # Check if the move is not a capture (e.g. e2e4)
		# If the first two (move[:2]) and last two (move[2:]) characters are coordinates
		if coordinateValid(move[:2].lower()) and coordinateValid(move[2:].lower()):
			if game.pieceAt(move[:2].lower()) is None:  # If the piece is not found, return move
				return move + extra_characters
			if game.pieceAt(move[:2].lower()).piece_type[0] == "pawn":  # If the piece is a pawn
				return move[2:] + extra_characters
			else:  # Otherwise
				return {"knight": "N", "bishop": "B", "rook": "R", "queen": "Q", "king": "K"}[game.pieceAt(move[:2].lower()).piece_type[0]] + move[2:] + extra_characters

	return move + extra_characters

def FENvalid(fen):
	if len(fen.split(" ")) < 6:
		return False
	if fen.split(" ")[0].count("/") != 7:
		return False
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
	if len(kings) > 2 or "k" not in kings or "K" not in kings:
		return False
	if fen.split(" ")[1] not in "wb":
		return False
	if (fen.split(" ")[2] != "-" and (not all([i.lower() in "kq" for i in fen.split(" ")[2]]) or len(set(fen.split(" ")[2])) != len(fen.split(" ")[2]))) or (fen.split(" ")[3] != "-" and not coordinateValid(fen.split(" ")[3])) or not unicode(fen.split(" ")[4]).isnumeric() or not unicode(fen.split(" ")[5]).isnumeric():
		return False
	return True
