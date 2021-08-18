"""
enums.py
Type Enumerations
"""


class Color:
	white, black = "white", "black"


class Piece:
	pawn, knight, bishop, rook = ["pawn", 1], ["knight", 3], ["bishop", 3], ["rook", 5]
	queen, king = ["queen", 9], ["king", float("inf")]


class Square:
	light, dark = "light", "dark"
