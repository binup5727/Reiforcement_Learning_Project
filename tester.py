import pygame
from board import board
from sys import exit


pygame.init()
width, height = 500, 500
screen = pygame.display.set_mode((width,height), pygame.RESIZABLE)
clock = pygame.time.Clock()

#--- Q learning
q_board = board(20, 20, screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i in range(q_board.rows):
                for j in range(q_board.col):
                    if q_board.boardRect[i][j].collidepoint(mouse_pos) and not q_board.board[i][j] == 1 or q_board.board[i][j] == 'p':
                        q_board.board[i][j] = '*'


        #game code
        
        q_board.draw()



        pygame.display.update()
        clock.tick(60)


