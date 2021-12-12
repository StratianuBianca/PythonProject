import pygame
import sys
from go.constants import WIDTH, HEIGHT, WHITE, BLACK
from go.board import Board, get_clicked_column, get_clicked_row

sys.setrecursionlimit(2500)
pygame.init()
print(sys.getrecursionlimit())
FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
print(WIN)
pygame.display.set_caption("Go Game")
font = pygame.font.SysFont("Arial", 30)


def button(screen, position, text):
    text_render = font.render(text, True, (255, 0, 0))
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


def end(board):
    WIN.fill(BLACK)
    if board.whiteScore > board.blackScore:
        line1 = "1.White : " + str(board.whiteScore)
        line2 = " 2.Black : " + str(board.blackScore)
    else:
        line2 = "2.White : " + str(board.whiteScore)
        line1 = " 1.Black : " + str(board.blackScore)

    line1 = font.render(line1, True, WHITE)
    text_rect1 = line1.get_rect()
    line2 = font.render(line2, True, WHITE)
    text_rect2 = line2.get_rect()
    text_rect1.center = (WIDTH // 2, HEIGHT // 2)
    text_rect2.center = (WIDTH // 2, HEIGHT // 2 + 50)
    clock = pygame.time.Clock()
    WIN.blit(line1, text_rect1)
    WIN.blit(line2, text_rect2)
    button1 = button(WIN, (450, 700), "Close")
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
                    exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button1.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    exit()
        pygame.display.update()


def game(board):
    pass1 = font.render('Player 1 pass', True, WHITE)
    pass2 = font.render('Player 2 pass', True, WHITE)
    run = True
    clock = pygame.time.Clock()
    board.turn = 1
    WIN.fill(BLACK)
    b1 = button(WIN, (300, 760), "Pass")
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if b1.collidepoint(pygame.mouse.get_pos()):
                    if board.turn == 1:
                        if board.pass_op2 and board.previously_move_pass:
                            board.calculate_score()
                            end(board)
                        else:
                            board.previously_move_pass = True
                            board.pass_op1 = True
                            WIN.blit(pass1, (600, 50))
                            pygame.display.update()
                            pygame.time.wait(500)
                            pygame.draw.rect(WIN, BLACK, (600, 50, 700, 70))
                            pygame.display.update()
                            board.turn = 2
                    else:
                        if board.pass_op1 and board.previously_move_pass:
                            board.calculate_score()
                            end(board)
                        else:
                            board.previously_move_pass = True
                            board.pass_op2 = True
                            WIN.blit(pass2, (600, 50))
                            pygame.display.update()
                            pygame.time.wait(500)
                            pygame.draw.rect(WIN, BLACK, (600, 50, 700, 100))
                            pygame.display.update()
                            board.turn = 1
                else:
                    board.previously_move_pass = False
                    print("Turn ", board.turn)
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    column = get_clicked_column(mouse_x)
                    row = get_clicked_row(mouse_y)
                    if board.is_ok_move(column, row):
                        board.draw_circle(column, row)
                        if board.turn == 1 and not board.ai_activate:
                            board.turn = 2
                        elif board.turn == 2:
                            board.turn = 1
                        if board.ai_activate and board.turn == 1:
                            row, column = board.generate_AI()
                            if row == -1 and column == -1:
                                print("pass")
                                board.pass_op2 = True
                                if board.pass_op1 and board.previously_move_pass:
                                    board.calculate_score()
                                    end(board)
                                else:
                                    board.previously_move_pass = True
                                    board.pass_op2 = True
                                    WIN.blit(pass2, (600, 50))
                                    pygame.display.update()
                                    pygame.time.wait(500)
                                    pygame.draw.rect(WIN, BLACK, (600, 50, 700, 100))
                                    pygame.display.update()
                                    board.turn = 1
                            else:
                                board.draw_circle(column, row)
                            board.turn = 1
        board.draw_squares(WIN)
        pygame.display.update()

    pygame.quit()


page1()
