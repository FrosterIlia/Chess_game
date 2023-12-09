from constants import *

def get_king_pos(board, king_color):
    for col in board:
        for cell in col:
            if cell.piece == "k" and cell.piece_color == king_color:
                return [cell.x, cell.y]


def is_check(board, king_color):
    for col in board:
        for cell in col:
            if cell.piece_color != king_color and cell.piece:  # checking pieces that can attack king
                cell.calc_possible_moves(board)
                if get_king_pos(board, king_color) in cell.get_possible_kills():
                    return True
    return False


def is_threatened(board, color, coords):
    for col in board:
        for cell in col:
            if cell.piece_color == color and cell.piece:  # checking pieces that can attack this square
                cell.calc_possible_moves(board)
                if coords in cell.get_possible_moves():
                    return True
    return False


def calc_checkmate(board, color):
    for col in board:
        for cell in col:
            if cell.piece and cell.piece_color == color:
                cell.calc_moves(board)
                if cell.possible_moves or cell.possible_kills:
                    return False

    return True










