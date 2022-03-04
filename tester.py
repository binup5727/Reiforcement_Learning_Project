import pygame
from board import player
from sys import exit


pygame.init()
width, height = 800, 800
screen = pygame.display.set_mode((width,height), pygame.RESIZABLE)
clock = pygame.time.Clock()

#--- Q learning
q_board = player(20, 20, screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if q_board.playerRec.collidepoint(mouse_pos):
                row = int(input('row: '))
                col = int(input('column: '))
                q_board.board.board[row][col] = 'p'
                
            for i in range(q_board.board.rows):
                for j in range(q_board.board.col):
                    #print(q_board.board.boardRect[i][j])
                    if q_board.board.boardRect[i][j].collidepoint(mouse_pos) and not (q_board.board.board[i][j] == 1 or q_board.board.board[i][j] == 'p'):
                        q_board.board.board[i][j] = '*'
            


        #game code
        #screen.fill((0,0,0))

        q_board.board.draw()
        q_board.move()
        



        pygame.display.update()
        clock.tick(60)


