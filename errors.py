"""
errors.py
Error Classes
"""


class MoveNotPossible(Exception):
	def __init__(self, move):
		super(MoveNotPossible, self).__init__("Move '" + str(move) + "' is not possible")


class InvalidMove(Exception):
	def __init__(self, move):
		super(InvalidMove, self).__init__("Move '" + str(move) + "' is not valid")
