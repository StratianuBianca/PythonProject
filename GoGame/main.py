import pygame
import sys
from go.constants import WIDTH, HEIGHT, WHITE, BLACK
from go.board import Board


sys.setrecursionlimit(2500)
pygame.init()
print(sys.getrecursionlimit())
FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
print(WIN)
pygame.display.set_caption("Go Game")


def button(screen, position, text):
    font = pygame.font.SysFont("Arial", 30)
    text_render = font.render(text, 1, (255, 0, 0))
    x, y, w, h = text_render.get_rect()
    x, y = position
    pygame.draw.line(screen, (150, 150, 150), (x, y), (x + w, y), 5)
    pygame.draw.line(screen, (150, 150, 150), (x, y - 2), (x, y + h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x, y + h), (x + w, y + h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x + w, y + h), [x + w, y], 5)
    pygame.draw.rect(screen, (100, 100, 100), (x, y, w, h))
    return screen.blit(text_render, (x, y))


def page1():
    clock = pygame.time.Clock()
    board = Board()
    button1 = button(WIN, (250, 400), "Opponent")
    button2 = button(WIN, (450, 400), "Computer")
    running = True

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button1.collidepoint(pygame.mouse.get_pos()):
                    board.ai_activate = False
                    game(board)
                elif button2.collidepoint(pygame.mouse.get_pos()):
                    board.ai_activate = True
                    game(board)
        pygame.display.update()


def game(board):
    #board = Board()
    run = True
    clock = pygame.time.Clock()
    board.turn = 1
    WIN.fill(BLACK)
    print(board.ai_activate)
    b1 = button(WIN, (300, 760), "Pass")
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if b1.collidepoint(pygame.mouse.get_pos()):
                    if board.turn == 1:
                        if board.pass_op2:
                            print("End game")
                            board.calculateScore()
                            print(board.whiteScore)
                            print(board.blackScore)
                            print("End game")
                        else:
                            board.pass_op1 = True
                            board.turn = 2
                    else:
                        if board.pass_op1:
                            print("End game")
                            board.calculateScore()
                            print(board.whiteScore)
                            print(board.blackScore)
                            print("End game")
                        else:
                            board.pass_op2 = True
                            board.turn = 1
                else:
                    print("Turn ", board.turn)
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    column = board.get_clicked_column(mouse_x)
                    row = board.get_clicked_row(mouse_y)
                    if board.is_ok_move(column, row):
                        board.draw_circle(column, row, WIN)
                        if board.turn == 1 and not board.ai_activate:
                            board.turn = 2
                        elif board.turn == 2:
                            board.turn = 1
                        if board.ai_activate and board.turn == 1:
                            row, column = board.generateAI()
                            if row == -1 and column == -1:
                                board.pass_op2 = True
                            board.turn = 1
                # pass
        board.draw_squares(WIN)
        pygame.display.update()

    pygame.quit()


#game()
page1()