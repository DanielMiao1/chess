"""
test__.py
Tests File
"""
from . import *

import random


def test():
	game = Game()  # Call Game class
	# Test moves
	# # Test with invalid move
	try:
		game.move(random.random())
	except errors.InvalidMove:
		pass
	else:
		raise Exception("Invalid move does not raise a InvalidMove error")
	# Test with random valid move
	game.move(random.choice(game.moves()))
