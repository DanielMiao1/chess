"""
errors.py
Error Classes
"""


class MoveNotPossible(Exception):
	def __init__(self, move="undefined"):
		super(MoveNotPossible, self).__init__("Move '{}' is not possible".format(move))


class InvalidMove(Exception):
	def __init__(self, move="undefined"):
		super(InvalidMove, self).__init__("Move '{}' is not possible".format(move))
