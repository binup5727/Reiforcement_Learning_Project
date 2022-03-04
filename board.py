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
                self.boardRect[i].append(pygame.Rect((j * 25, i * 25, 20, 20)))

                pygame.draw.rect(self.screen, (0, 0, 255), self.boardRect[i][j])

        
                
    def draw(self):

        for i in range(self.rows):
            
            for j in range(self.col):

                if self.board[i][j] == '*':
                    color = (0, 0, 0)
                else:
                    color = (0, 0, 255)
                pygame.draw.rect(self.screen, color, self.boardRect[i][j])


