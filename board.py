from re import L
import pygame

class board:
    def __init__(self, rows, col, win, screen):
        self.rows = rows
        self.col = col
        self.screen = screen
        self.board = []
        self.boardRect = []
        self.Q = []
        self.actions = ['up', 'down', 'left', 'right']
        self.win = win
        print(win[0])
        
        

        for i in range(self.rows):
            self.board.append([])
            self.boardRect.append([])
            self.Q.append([])
            for j in range(self.col):
                
                self.Q[i].append([])
                self.board[i].append(0)
                self.boardRect[i].append(pygame.Rect((j * 25, i * 25, 20, 20)))

                pygame.draw.rect(self.screen, (0, 0, 255), self.boardRect[i][j])

                for k in self.actions:
                    self.Q[i][j].append(0)
        
        self.board[win[0]][win[1]] = 1
        
        print(self.Q)
        print(self.board)


                
    def draw(self):

        for i in range(self.rows):
            
            for j in range(self.col):

                if self.board[i][j] == '*':
                    color = (0, 0, 0)
                else:
                    color = (0, 0, 255)
                pygame.draw.rect(self.screen, color, self.boardRect[i][j])



class player:

    def __init__(self, rows, col, screen) -> None:
        self.screen = screen 
        self.board = board(rows, col, [3, 5],self.screen)
        self.player = pygame.image.load('index.png')
        self.player = pygame.transform.scale(self.player, (10, 10)).convert()
        self.playerRec = self.player.get_rect()
        self.playerRec.x = self.board.boardRect[0][-1].x + 20
        self.playerRec.y = self.board.boardRect[0][-1].y
        self.screen.blit(self.player, self.playerRec)
    
    def move(self):
        
        for i in range(self.board.rows):
            for j in range(self.board.col):
                if self.board.board[i][j] == 'p':
                    #print('moved')
                    self.playerRec.center = self.board.boardRect[i][j].center
                    #print(self.board.boardRect[i][j].center)
                    self.screen.blit(self.player, self.playerRec)


