"""
test__.py
Tests File
"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.curdir))
from chess import *

import random


def test():
	game = Game()  # Create Game
	# Test moves
	# # Test with invalid move
	try:
		game.move(random.random())
	except errors.InvalidMove:
		pass
	else:
		raise Exception("Invalid move does not raise a InvalidMove error")
	# Test with random valid move
	for i in range(3):
		game.move(random.choice(game.legal_moves()))
