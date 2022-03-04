import pygame
from board import board
from sys import exit


pygame.init()
width, height = 500, 500
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()

#--- Q learning
q_board = board(6, 8, screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


        #game code
        




        pygame.display.update()
        clock.tick(60)


