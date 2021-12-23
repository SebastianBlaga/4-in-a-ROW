import pygame

import gameState as gm

circleRadius = 50
slotScale = circleRadius * 2

redColor = pygame.Color(255, 0, 0)
blueColor = pygame.Color(0, 0, 255)
blackColor = pygame.Color(0, 0, 0)
yellowColor = (255, 255, 0)


def main():
    board = gm.create_board(7, 5)

    pygame.init()
    screen = pygame.display.set_mode((slotScale * 7, slotScale * 5))
    pygame.display.set_caption("Connect 4")
    screen.fill(blueColor)

    for column in range(7):
        for row in range(5):
            pygame.draw.circle(screen, blackColor, (column * slotScale + circleRadius, row * slotScale + circleRadius),
                               circleRadius)

    turn = 0
    game_running = True
    while game_running:

        for column in range(7):
            for row in range(5):
                if board[row][column] == 1:
                    pygame.draw.circle(screen, redColor,
                                       (column * slotScale + circleRadius, row * slotScale + circleRadius),
                                       circleRadius)
                if board[row][column] == 2:
                    pygame.draw.circle(screen, yellowColor,
                                       (column * slotScale + circleRadius, row * slotScale + circleRadius),
                                       circleRadius)

        for event in pygame.event.get():
            pygame.display.update()
            if event.type == pygame.QUIT:
                game_running = False
            if event.type == pygame.MOUSEMOTION:
                mouseX = event.pos[0]

                if turn == 0:
                    pygame.draw.circle(screen, redColor, (mouseX, slotScale * 7), circleRadius)
                else:
                    pygame.draw.circle(screen, yellowColor, (mouseX, slotScale * 7), circleRadius)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if turn == 0:
                    mouseX = event.pos[0]
                    column = int(mouseX/slotScale)
                    row = gm.available_row(board, column, 4)
                    gm.update_board(board, column, row, 1)

                else:
                    mouseX = event.pos[0]
                    column = int(mouseX/slotScale)
                    row = gm.available_row(board, column, 4)
                    gm.update_board(board, column, row, 2)

                turn = turn + 1
                turn = turn % 2


if __name__ == "__main__":
    main()
