# -*- coding: utf-8 -*-

import chess.openings

try:
	unicode
except NameError:
	unicode = str


def fillIterative(board, blockers, captures, mask, shift_amount, left_shift=True):
	def singleShift(shiftee):
		if left_shift:
			return shiftee << shift_amount
		return shiftee >> shift_amount

	filled_board = 0
	current_position = board

	while not current_position & captures and not singleShift(current_position) & blockers and current_position & mask != current_position:
		current_position = singleShift(current_position)
		filled_board |= current_position

	return filled_board


def fillNorthIterative(board, blockers, captures):
	mask = 0b11111111_00000000_00000000_00000000_00000000_00000000_00000000_00000000
	return fillIterative(board, blockers, captures, mask, 8)


def fillSouthIterative(board, blockers, captures):
	mask = 0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_11111111
	return fillIterative(board, blockers, captures, mask, 8, False)


def fillEastIterative(board, blockers, captures):
	mask = 0b10000000_10000000_10000000_10000000_10000000_10000000_10000000_10000000
	return fillIterative(board, blockers, captures, mask, 1)


def fillWestIterative(board, blockers, captures):
	mask = 0b00000001_00000001_00000001_00000001_00000001_00000001_00000001_00000001
	return fillIterative(board, blockers, captures, mask, 1, False)


def fillNorthEastIterative(board, blockers, captures):
	mask = 0b11111111_10000000_10000000_10000000_10000000_10000000_10000000_10000000
	return fillIterative(board, blockers, captures, mask, 9)


def fillNorthWestIterative(board, blockers, captures):
	mask = 0b11111111_00000001_00000001_00000001_00000001_00000001_00000001_00000001
	return fillIterative(board, blockers, captures, mask, 7)


def fillSouthEastIterative(board, blockers, captures):
	mask = 0b00000001_10000000_10000000_10000000_10000000_10000000_10000000_11111111
	return fillIterative(board, blockers, captures, mask, 7, False)


def fillSouthWestIterative(board, blockers, captures):
	mask = 0b00000001_00000001_00000001_00000001_00000001_00000001_00000001_11111111
	return fillIterative(board, blockers, captures, mask, 9, False)


class Game:
	def __init__(self):
		(
			self.white_pawns, self.black_pawns,
			self.white_knights, self.black_knights,
			self.white_bishops, self.black_bishops,
			self.white_rooks, self.black_rooks,
			self.white_queens, self.black_queens,
			self.white_kings, self.black_kings
		) = (
			0b11111111_00000000,
			0b11111111_00000000_00000000_00000000_00000000_00000000_00000000,
			0b01000010,
			0b01000010_00000000_00000000_00000000_00000000_00000000_00000000_00000000,
			0b00100100,
			0b00100100_00000000_00000000_00000000_00000000_00000000_00000000_00000000,
			0b10000001,
			0b10000001_00000000_00000000_00000000_00000000_00000000_00000000_00000000,
			0b00010000,
			0b00010000_00000000_00000000_00000000_00000000_00000000_00000000_00000000,
			0b00001000,
			0b00001000_00000000_00000000_00000000_00000000_00000000_00000000_00000000
		)

	def __repr__(self):
		return str(self)

	def __str__(self):
		pieces_list = [" "] * 64

		def appendToString(value, piece_string):
			pieces = str(bin(value))[2:].zfill(64)
			for index in range(len(pieces)):
				if int(pieces[index]):
					pieces_list[index] = piece_string

		appendToString(self.white_pawns, "P")
		appendToString(self.black_pawns, "p")
		appendToString(self.white_knights, "N")
		appendToString(self.black_knights, "n")
		appendToString(self.white_bishops, "B")
		appendToString(self.black_bishops, "b")
		appendToString(self.white_rooks, "R")
		appendToString(self.black_rooks, "r")
		appendToString(self.white_queens, "Q")
		appendToString(self.black_queens, "q")
		appendToString(self.white_kings, "K")
		appendToString(self.black_kings, "k")

		pieces_dimensional_list = [pieces_list[:8], pieces_list[8:16], pieces_list[16:24], pieces_list[24:32], pieces_list[32:40], pieces_list[40:48], pieces_list[48:56], pieces_list[56:64]]

		string = "---------------------------------\n" + "\n|-------------------------------|\n".join(["| " + " | ".join(row) + " |" for row in pieces_dimensional_list]) + "\n---------------------------------"

		return string
