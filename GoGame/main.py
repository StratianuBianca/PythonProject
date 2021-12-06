import pygame
from go.constants import WIDTH, HEIGHT, WHITE
from go.board import Board
pygame.init()

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


def main():

    run = True
    clock = pygame.time.Clock()
    board = Board()
    board.turn = 1
    b1 = button(WIN, (300, 760), "Pass")
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if b1.collidepoint(pygame.mouse.get_pos()):
                    if board.turn == 1:
                        if not board.pass_op2:
                            print("End game")
                        else:
                            board.turn = 2
                    else:
                        if board.pass_op1:
                            print("End game")
                        else:
                            board.turn = 1
                else:
                    print("Turn ", board.turn)
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    column = board.get_clicked_column(mouse_x)
                    row = board.get_clicked_row(mouse_y)
                    if board.is_ok_move(column, row):
                        print("AAAAAAAAAAAA")
                        board.draw_circle(column, row, WIN)
                        if board.turn == 1:
                            print("SSSS")
                            board.turn = 2
                        else:
                            print("DFDF")
                            board.turn = 1
                # pass
        board.draw_squares(WIN)
        pygame.display.update()

    pygame.quit()


main()
