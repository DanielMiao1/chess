"""
test__.py
Tests File
"""
from . import *

import random


def test():
	game = Game() # Call Game class
	# Test functions
	# # Test coordinateToIndex and indexToCoordinate functions with (0, 0), (7, 7), (4, 4), and a random index
	for i in [[0, 0], [7, 7], [4, 4]]:  # Test with predefined indexes
		assert functions.coordinateToIndex(functions.indexToCoordinate(i)) == i  # Assert
	index = [random.randint(0, 7), random.randint(0, 7)]  # Test with random index
	assert functions.coordinateToIndex(functions.indexToCoordinate(index)) == index  # Assert
	# Test moves
	# # Test with random float
	try:
		game.move(random.random())
	except errors.MoveNotPossible:
		pass
	else:
		raise Exception("Invalid move does not raise a MoveNotPossible error")
