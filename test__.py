from . import *


def test_game_class():
	assert Game()


def test_components():
	assert Piece([0, 0], enums.Piece.pawn, enums.Color.white, None), Square([0, 0])
