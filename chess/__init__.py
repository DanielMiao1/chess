# -*- coding: utf-8 -*-

import chess.openings

try:
	unicode
except NameError:
	unicode = str


ALL_SQUARES = 0b11111111_11111111_11111111_11111111_11111111_11111111_11111111_11111111

A_FILE = 0b10000000_10000000_10000000_10000000_10000000_10000000_10000000_10000000
B_FILE = 0b01000000_01000000_01000000_01000000_01000000_01000000_01000000_01000000
C_FILE = 0b00100000_00100000_00100000_00100000_00100000_00100000_00100000_00100000
D_FILE = 0b00010000_00010000_00010000_00010000_00010000_00010000_00010000_00010000
E_FILE = 0b00001000_00001000_00001000_00001000_00001000_00001000_00001000_00001000
F_FILE = 0b00000100_00000100_00000100_00000100_00000100_00000100_00000100_00000100
G_FILE = 0b00000010_00000010_00000010_00000010_00000010_00000010_00000010_00000010
H_FILE = 0b00000001_00000001_00000001_00000001_00000001_00000001_00000001_00000001

EIGHTH_RANK = 0b11111111_00000000_00000000_00000000_00000000_00000000_00000000_00000000
SEVENTH_RANK = 0b00000000_11111111_00000000_00000000_00000000_00000000_00000000_00000000
SIXTH_RANK = 0b00000000_00000000_11111111_00000000_00000000_00000000_00000000_00000000
FIFTH_RANK = 0b00000000_00000000_00000000_11111111_00000000_00000000_00000000_00000000
FOURTH_RANK = 0b00000000_00000000_00000000_00000000_11111111_00000000_00000000_00000000
THIRD_RANK = 0b00000000_00000000_00000000_00000000_00000000_11111111_00000000_00000000
SECOND_RANK = 0b00000000_00000000_00000000_00000000_00000000_00000000_11111111_00000000
FIRST_RANK = 0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_11111111


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
	return fillIterative(board, blockers, captures, EIGHTH_RANK, 8)


def fillSouthIterative(board, blockers, captures):
	return fillIterative(board, blockers, captures, FIRST_RANK, 8, False)


def fillEastIterative(board, blockers, captures):
	return fillIterative(board, blockers, captures, A_FILE, 1)


def fillWestIterative(board, blockers, captures):
	return fillIterative(board, blockers, captures, H_FILE, 1, False)


def fillNorthEastIterative(board, blockers, captures):
	return fillIterative(board, blockers, captures, EIGHTH_RANK | A_FILE, 9)


def fillNorthWestIterative(board, blockers, captures):
	return fillIterative(board, blockers, captures, EIGHTH_RANK | H_FILE, 7)


def fillSouthEastIterative(board, blockers, captures):
	return fillIterative(board, blockers, captures, FIRST_RANK | A_FILE, 7, False)


def fillSouthWestIterative(board, blockers, captures):
	return fillIterative(board, blockers, captures, FIRST_RANK | H_FILE, 9, False)


def generatePawnMoves(pieces, blockers, captures, white_move=True):
	allowed_pawn_positions = (ALL_SQUARES ^ EIGHTH_RANK ^ FIRST_RANK)
	occupied_squares = ALL_SQUARES ^ (blockers | captures)
	double_move_rank = SECOND_RANK if white_move else SEVENTH_RANK

	def singleMove(position):
		if white_move:
			return position << 8
		return position >> 8

	moves = 0b0
	moves |= singleMove(pieces & allowed_pawn_positions) & (ALL_SQUARES ^ (blockers | captures))

	moves |= singleMove(singleMove(pieces & double_move_rank) & occupied_squares) & occupied_squares  # Double pawn move

	if white_move:
		moves |= ((pieces & allowed_pawn_positions) << 9) & captures  # West captures
		moves |= ((pieces & allowed_pawn_positions) << 7) & captures  # East captures
	else:
		moves |= ((pieces & allowed_pawn_positions) >> 9) & captures  # West captures
		moves |= ((pieces & allowed_pawn_positions) >> 7) & captures  # East captures

	moves &= ALL_SQUARES ^ blockers

	return moves


def generateKnightMoves(pieces, blockers):
	moves = 0b0
	moves |= (pieces << 15) & (ALL_SQUARES ^ A_FILE)  # North-north-west move
	moves |= (pieces << 17) & (ALL_SQUARES ^ H_FILE)  # North-north-east move
	moves |= (pieces << 6) & (ALL_SQUARES ^ A_FILE ^ B_FILE)  # North-west-west move
	moves |= (pieces << 10) & (ALL_SQUARES ^ H_FILE ^ G_FILE)  # North-east-east move

	moves |= (pieces >> 17) & (ALL_SQUARES ^ A_FILE)  # South-south-west move
	moves |= (pieces >> 15) & (ALL_SQUARES ^ H_FILE)  # South-south-east move
	moves |= (pieces >> 10) & (ALL_SQUARES ^ A_FILE ^ B_FILE)  # South-west-west move
	moves |= (pieces >> 6) & (ALL_SQUARES ^ G_FILE ^ H_FILE)  # South-east-east move

	moves &= ALL_SQUARES ^ blockers

	return moves


def fillBishopMoves(pieces, blockers, captures):
	return (
		fillNorthWestIterative(pieces, blockers, captures) |
		fillNorthEastIterative(pieces, blockers, captures) |
		fillSouthWestIterative(pieces, blockers, captures) |
		fillSouthEastIterative(pieces, blockers, captures)
	)


def fillRookMoves(pieces, blockers, captures):
	return (
		fillNorthIterative(pieces, blockers, captures) |
		fillSouthIterative(pieces, blockers, captures) |
		fillWestIterative(pieces, blockers, captures) |
		fillEastIterative(pieces, blockers, captures)
	)


def fillQueenMoves(pieces, blockers, captures):
	return (
		fillRookMoves(pieces, blockers, captures) |
		fillBishopMoves(pieces, blockers, captures)
	)


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
