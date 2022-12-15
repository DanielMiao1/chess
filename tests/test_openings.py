"""
/tests/test_game.py
Test opening interpretation logic
"""

import chess


def test():
	game = chess.Game(evaluate_openings=True)
	assert not game.opening

	game.move("e4")
	assert game.opening == "B00 King's Pawn"

	game.move("a6")
	game.move("h3")
	assert game.opening == "B00 St. George Defense"
