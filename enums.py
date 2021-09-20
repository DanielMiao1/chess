"""
enums.py
Type Enumerations
"""
import errors


class Color:
	white, black = "white", "black"

	@staticmethod
	def invert(color):
		if color in ["white", "w"]:
			return Color.black
		elif color in ["black", "b"]:
			return Color.white
		else:
			raise errors.UndefinedColor(color)
		

class Piece:
	pawn, knight, bishop, rook = "pawn", "knight", "bishop", "rook"
	queen, king = "queen", "king"
	unicode_dictionary = {"whiteking": "♔", "blackking": "♚", "whitequeen": "♕", "blackqueen": "♛", "whiterook": "♖", "blackrook": "♜", "whitebishop": "♗", "blackbishop": "♝", "whiteknight": "♘", "blackknight": "♞", "whitepawn": "♙", "blackpawn": "♟"}
	
	@staticmethod
	def unicode(piece, color=Color.white):
		if piece not in [Piece.pawn, Piece.knight, Piece.bishop, Piece.rook, Piece.queen, Piece.king]:
			raise errors.UndefinedPiece(piece)
		if color not in [Color.white, Color.black]:
			raise errors.UndefinedColor(color)
		return Piece.unicode_dictionary[color + piece]
	
	@staticmethod
	def value(piece):
		if piece in [Piece.pawn, Piece.knight, Piece.bishop, Piece.rook, Piece.queen, Piece.king]:
			return {Piece.pawn: 1, Piece.knight: 3, Piece.bishop: 3, Piece.rook: 5, Piece.queen: 9, Piece.king: float("inf")}[piece]
		raise errors.UndefinedPiece(piece)


class Move:
	def __init__(self, name, old_position, new_position, piece, is_capture=False):
		self.piece = piece
		self.name = name
		self.old_position, self.new_position = old_position, new_position
		self.is_capture = is_capture
		if is_capture:
			self.captured_piece = self.piece.board.pieceAt(new_position)
		else:
			self.captured_piece = None
