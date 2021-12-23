import numpy as np


def create_board(columns, rows):
    board = np.zeros((rows, columns))
    return board


def update_board(board, column, row, player):
    board[row][column] = player


def available_row(board, column, row):
    if board[row][column] == 0:
        return row
    elif row > 0:
        return available_row(board, column, row - 1)


