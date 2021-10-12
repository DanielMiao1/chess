"""
errors.py
Error Classes
"""


class errors:
	class MoveNotPossible(Exception):
		def __init__(self, move):
			super(errors.MoveNotPossible, self).__init__("Move '" + str(move) + "' is not possible")

	class InvalidMove(Exception):
		def __init__(self, move):
			super(errors.InvalidMove, self).__init__("Move '" + str(move) + "' is invalid")

	class UndefinedColor(Exception):
		def __init__(self, color):
			if color.lower() == "w":
				super(errors.UndefinedColor, self).__init__("Color 'w' is invalid. Maybe you meant 'white'?")
			elif color.lower() == "b":
				super(errors.UndefinedColor, self).__init__("Color 'b' is invalid. Maybe you meant 'black'?")
			else:
				super(errors.UndefinedColor, self).__init__("Color '" + str(color) + "' is invalid")

	class UndefinedPiece(Exception):
		def __init__(self, piece):
			super(errors.UndefinedPiece, self).__init__("Piece '" + str(piece) + "' is invalid")

	class UndefinedGamePhase(Exception):
		def __init__(self, phase):
			super(errors.UndefinedGamePhase, self).__init__("Game phase '" + str(phase) + "' is invalid")

	class InvalidFEN(Exception):
		def __init__(self, fen):
			super(errors.InvalidFEN, self).__init__("FEN '" + str(fen) + "' is invalid")
