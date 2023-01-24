# -*- coding: utf-8 -*-

import chess.errors
import chess.openings
import chess.functions

try:
	unicode
except NameError:
	unicode = str


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

	@staticmethod
	def fillNorthIterative(board, blockers):
		current_position = board
		mask = 0b11111111_00000000_00000000_00000000_00000000_00000000_00000000_00000000
		while not current_position & blockers:
			yield current_position
			current_position <<= 8

			if current_position & mask == current_position:
				if not current_position & blockers:
					yield current_position

				return

	@staticmethod
	def fillSouthIterative(board, blockers):
		current_position = board
		mask = 0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_11111111
		while not current_position & blockers:
			yield current_position
			current_position >>= 8

			if current_position & mask == current_position:
				if not current_position & blockers:
					yield current_position

				return

	@staticmethod
	def fillEastIterative(board, blockers):
		current_position = board
		mask = 0b10000000_10000000_10000000_10000000_10000000_10000000_10000000_10000000
		while not current_position & blockers:
			yield current_position
			current_position <<= 1

			if current_position & mask == current_position:
				if not current_position & blockers:
					yield current_position

				return

	@staticmethod
	def fillWestIterative(board, blockers):
		current_position = board
		mask = 0b00000001_00000001_00000001_00000001_00000001_00000001_00000001_00000001
		while not current_position & blockers:
			yield current_position
			current_position >>= 1

			if current_position & mask == current_position:
				if not current_position & blockers:
					yield current_position

				return

	@staticmethod
	def fillNorthEastIterative(board, blockers):
		current_position = board
		mask = 0b11111111_10000000_10000000_10000000_10000000_10000000_10000000_10000000
		while not current_position & blockers:
			yield current_position
			current_position <<= 9

			if current_position & mask == current_position:
				if not current_position & blockers:
					yield current_position

				return

	@staticmethod
	def fillNorthWestIterative(board, blockers):
		current_position = board
		mask = 0b11111111_00000001_00000001_00000001_00000001_00000001_00000001_00000001
		while not current_position & blockers:
			yield current_position
			current_position <<= 7

			if current_position & mask == current_position:
				if not current_position & blockers:
					yield current_position

				return

	@staticmethod
	def fillSouthEastIterative(board, blockers):
		current_position = board
		mask = 0b00000001_10000000_10000000_10000000_10000000_10000000_10000000_11111111
		while not current_position & blockers:
			yield current_position
			current_position >>= 7

			if current_position & mask == current_position:
				if not current_position & blockers:
					yield current_position

				return

	@staticmethod
	def fillSouthWestIterative(board, blockers):
		current_position = board
		mask = 0b00000001_00000001_00000001_00000001_00000001_00000001_00000001_11111111
		while not current_position & blockers:
			yield current_position
			current_position >>= 9

			if current_position & mask == current_position:
				if not current_position & blockers:
					yield current_position

				return

	def __repr__(self):
		return str(self)

	def __str__(self):
		pieces_list = [" "] * 64

		def appendToString(value, piece_string):
			pieces = str(bin(value))[2:].zfill(64)
			for index in range(len(pieces)):
				if int(pieces[index]):
					pieces_list[index] = piece_string

		appendToString(self.white_pawns.value, "P")
		appendToString(self.black_pawns.value, "p")
		appendToString(self.white_knights.value, "N")
		appendToString(self.black_knights.value, "n")
		appendToString(self.white_bishops.value, "B")
		appendToString(self.black_bishops.value, "b")
		appendToString(self.white_rooks.value, "R")
		appendToString(self.black_rooks.value, "r")
		appendToString(self.white_queens.value, "Q")
		appendToString(self.black_queens.value, "q")
		appendToString(self.white_kings.value, "K")
		appendToString(self.black_kings.value, "k")

		pieces_dimensional_list = [pieces_list[:8], pieces_list[8:16], pieces_list[16:24], pieces_list[24:32], pieces_list[32:40], pieces_list[40:48], pieces_list[48:56], pieces_list[56:64]]

		string = "---------------------------------\n" + "\n|-------------------------------|\n".join(["| " + " | ".join(row) + " |" for row in pieces_dimensional_list]) + "\n---------------------------------"

		return string
