import pygame

class board:
    def __init__(self, rows, col, screen):
        self.rows = rows
        self.col = col
        self.screen = screen
        self.board = []
        self.boardRect = []
        

        for i in range(self.rows):
            self.board.append([])
            self.boardRect.append([])
            for j in range(self.col):
                print(j)
                self.board[i].append(0)
                self.boardRect[i].append(pygame.Rect((j * 50, i * 50, 45, 45)))

                pygame.draw.rect(self.screen, (0, 0, 255), self.boardRect[i][j])

        
                
        
