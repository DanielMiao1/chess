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
