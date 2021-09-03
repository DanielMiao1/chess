"""
functions.py
Functions
"""


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
	extra_characters = ""  # Stores extra characters (e.g +, #, =Q, =Q+...)
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
