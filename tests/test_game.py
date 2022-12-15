"""
/tests/test_game.py
Test game and board logic
"""

import chess

import random
import pytest


def randomGame():
	random_game = chess.Game()

	while not random_game.game_over:
		random_game.move(random.choice(random_game.legal_moves()))


def test():
	# randomGame()

	game = chess.Game()
	game.loadPGN("[header \"value\"]\n1. e4 e5 2. Nf3 Nc6")
	assert game.FEN() == "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3"
	assert game.PGN().startswith("1. e4 e5 2. Nf3 Nc6")
	assert game.move_list == "1. e4 e5 2. Nf3 Nc6"
	assert not game.game_over

	game.loadPGN("1. e4 e5 2. Qh5 Nc6 3. Bc4 Nf6 4. Qxf7+ *")
	assert game.FEN() == "r1bqkb1r/pppp1Qpp/2n2n2/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4"
	assert game.PGN().startswith("1. e4 e5 2. Qh5 Nc6 3. Bc4 Nf6 4. Qxf7")
	assert game.move_list.startswith("1. e4 e5 2. Qh5 Nc6 3. Bc4 Nf6 4. Qxf7")
	assert game.game_over
	assert game.is_checkmate
	assert not game.is_stalemate
	assert not game.is_seventyfive_move
	assert not game.is_fivefold_repetition

	with pytest.raises(chess.errors.InvalidPGNMove):
		game.loadPGN("1. e4 e4")

	game.loadPGN("[header 'value']\n1. e4 e5", quotes="'")

	with pytest.raises(ValueError):
		game.loadPGN("[header 'value']\n1. e4 e5")

	game.loadFEN("8/7K/8/8/8/8/8/k7 w k - 0 1")
	assert game.FEN() == "8/7K/8/8/8/8/8/k7 w k - 0 1"

	with pytest.raises(chess.errors.InvalidFEN):
		game.loadFEN("8/K/8/8/8/8/8/8 w k - 0 2")
