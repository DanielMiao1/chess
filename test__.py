"""
test__.py
Tests File
"""
from . import *

import random


def test():
	game = Game() # Call Game class
	# Test moves
	# # Test with random float
	try:
		game.move(random.random())
	except errors.MoveNotPossible:
		pass
	else:
		raise Exception
	# # Test with empty string
	try:
		game.move("")
	except errors.MoveNotPossible:
		pass
	else:
		raise Exception
