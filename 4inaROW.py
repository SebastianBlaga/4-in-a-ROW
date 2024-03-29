import random
import pygame
import numpy as np
import sys

opponent = sys.argv[1]
x_cells = int(sys.argv[2])
y_cells = int(sys.argv[3])
firstPlayer = sys.argv[4]

piece_radius = 50
slot_radius = piece_radius * 2

game_width = x_cells * slot_radius
game_height = y_cells * slot_radius

white_color = pygame.Color(255, 255, 255)
redColor = pygame.Color(255, 0, 0)
blueColor = pygame.Color(0, 0, 255)
blackColor = pygame.Color(0, 0, 0)
yellowColor = (255, 255, 0)

pygame.font.init()
font = pygame.font.SysFont("monospace", 75)
difficulty_font = pygame.font.SysFont("arial", 30)
ai_difficulty = str
easy_font = difficulty_font.render('easy', True, blackColor)
medium_font = difficulty_font.render('medium', True, blackColor)
hard_font = difficulty_font.render('hard', True, blackColor)


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


def next_available_row(board, column):
    for row in range(y_cells):
        if board[row][column] == 0:
            return row


def valid_row(board, column):
    return board[y_cells - 1][column] == 0


# Function taken from https://www.askpython.com/python/examples/connect-four-game
def check_win(board, piece):
    for column in range(x_cells - 3):
        for row in range(y_cells):
            if board[row][column] == piece and \
                    board[row][column + 1] == piece and \
                    board[row][column + 2] == piece and \
                    board[row][column + 3] == piece:
                return True
    for column in range(x_cells):
        for row in range(y_cells - 3):
            if board[row][column] == piece and \
                    board[row + 1][column] == piece and \
                    board[row + 2][column] == piece and \
                    board[row + 3][column] == piece:
                return True
    for column in range(x_cells - 3):
        for row in range(y_cells - 3):
            if board[row][column] == piece and \
                    board[row + 1][column + 1] == piece and \
                    board[row + 2][column + 2] == piece and \
                    board[row + 3][column + 3] == piece:
                return True
    for column in range(x_cells - 3):
        for row in range(3, y_cells):
            if board[row][column] == piece and \
                    board[row - 1][column + 1] == piece and \
                    board[row - 2][column + 2] == piece and \
                    board[row - 3][column + 3] == piece:
                return True


########

def draw_game_board(screen, x, y):
    for column in range(x):
        for row in range(y):
            pygame.draw.circle(screen, blackColor, (column * slot_radius + piece_radius, row * slot_radius
                                                    + piece_radius), piece_radius)


def update_game_board(screen, board):
    for column in range(x_cells):
        for row in range(y_cells):
            if board[row][column] == 1:
                pygame.draw.circle(screen, redColor,
                                   (column * slot_radius + piece_radius, row * slot_radius + piece_radius),
                                   piece_radius)
            if board[row][column] == 2:
                pygame.draw.circle(screen, yellowColor,
                                   (column * slot_radius + piece_radius, row * slot_radius + piece_radius),
                                   piece_radius)


# Inspired by Keith Galli's Connect 4 AI
def score_position(board, piece):
    score = 0
    for row in range(y_cells):
        rows = [row for row in list(board[row, :])]
        for column in range(x_cells - 3):
            group = rows[column:column + 4]
            if group.count(piece) == 4:
                score = score + 100
            elif group.count(piece) == 3 and group.count(0) == 1:
                score = score + 10
    for column in range(x_cells):
        columns = [column for column in list(board[:, column])]
        for row in range(y_cells - 3):
            group = columns[row:row + 4]
            if group.count(piece) == 4:
                score = score + 100
            elif group.count(piece) == 3 and group.count(0) == 1:
                score = score + 10

    return score


def pick_best_move(board, piece):
    best_score = 0
    valid_locations = get_valid_location(board)
    best_column = random.choice(valid_locations)
    print(valid_locations)
    for column in valid_locations:
        row = next_available_row(board, column)
        temp_board = board.copy()
        update_board(temp_board, column, row, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_column = column
    return best_column


def get_valid_location(board):
    valid_locations = []
    for column in range(x_cells):
        if valid_row(board, column):
            valid_locations.append(column)
    return valid_locations


button_x = game_width / 2 - piece_radius
button_y = game_height / 2


##################################################################################
def main():
    game_running = False
    board = create_board(x_cells, y_cells)
    pygame.init()
    screen = pygame.display.set_mode((game_width, game_height))
    pygame.display.set_caption("Connect 4")

    while not game_running and opponent == "computer":
        pygame.draw.rect(screen, white_color,
                         (int(button_x), int(button_y) - slot_radius, slot_radius, piece_radius))
        screen.blit(easy_font, (button_x, button_y - slot_radius, slot_radius, piece_radius))
        pygame.draw.rect(screen, white_color,
                         (int(button_x), int(button_y), slot_radius, piece_radius))
        screen.blit(medium_font, (button_x, button_y, slot_radius, piece_radius))
        pygame.draw.rect(screen, white_color,
                         (int(button_x), int(button_y) + slot_radius, slot_radius, piece_radius))
        screen.blit(hard_font, (button_x, button_y + slot_radius, slot_radius, piece_radius))

        for event in pygame.event.get():
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos[0])
                if button_x + slot_radius > event.pos[0] > button_x and \
                        button_y - slot_radius + piece_radius > \
                        event.pos[1] > button_y - slot_radius:
                    ai_difficulty = 'easy'
                    game_running = True
                if button_x + slot_radius > event.pos[0] > button_x and \
                        button_y + piece_radius > event.pos[1] > button_y:
                    ai_difficulty = 'medium'
                    game_running = True
                if button_x + slot_radius > event.pos[0] > button_x and \
                        button_y + slot_radius + piece_radius > \
                        event.pos[1] > button_y + slot_radius:
                    ai_difficulty = 'hard'
                    game_running = True

    if firstPlayer == "human":
        turn = 0
    else:
        turn = 1
    game_running = True
    screen.fill(blueColor)
    draw_game_board(screen, x_cells, y_cells)
    while game_running:

        for event in pygame.event.get():
            pygame.display.update()
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if turn == 0:
                    mouse_x = event.pos[0]
                    column = int(mouse_x / slot_radius)
                    row = available_row(board, column, y_cells - 1)
                    update_board(board, column, row, 1)
                    if check_win(board, 1):
                        label = font.render("Player 1 won", True, redColor)
                        screen.blit(label, (0, 0))
                        game_running = False

                    turn = turn + 1
                    turn = turn % 2

                elif opponent == "human" and turn == 1:
                    mouse_x = event.pos[0]
                    column = int(mouse_x / slot_radius)
                    print(column)
                    row = available_row(board, column, y_cells - 1)
                    update_board(board, column, row, 2)
                    if check_win(board, 2):
                        label = font.render("Player 2 won", True, yellowColor)
                        screen.blit(label, (0, 0))
                        game_running = False

                    turn = turn + 1
                    turn = turn % 2
        if opponent == "computer" and turn == 1:
            if ai_difficulty == "easy":
                column = random.randint(0, x_cells - 1)
                row = available_row(board, column, y_cells - 1)
                update_board(board, column, row, 2)
                if check_win(board, 2):
                    label = font.render("The Computer won!", True, yellowColor)
                    screen.blit(label, (0, 0))
                    game_running = False
                turn += 1
                turn = turn % 2

            elif ai_difficulty == "medium":

                column = random.randint(0, x_cells - 1)
                while column-1 is not 0:
                    column = random.randint(0, x_cells - 1)
                row = available_row(board, column, y_cells - 1)
                update_board(board, column, row, 2)
                if check_win(board, 2):
                    label = font.render("The Computer won!", True, yellowColor)
                    screen.blit(label, (0, 0))
                    game_running = False
                turn += 1
                turn = turn % 2

            elif ai_difficulty == "hard":

                column = pick_best_move(board, 2)
                if valid_row(board, column):
                    row = available_row(board, column, y_cells - 1)
                    update_board(board, column, row, 2)

                    if check_win(board, 2):
                        label = font.render("The Computer won!", True, yellowColor)
                        screen.blit(label, (0, 0))
                        game_running = False
                    turn += 1
                    turn = turn % 2

        update_game_board(screen, board)
        if not game_running:
            pygame.display.update()
            pygame.time.wait(30000)


if __name__ == "__main__":
    main()
