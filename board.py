from re import L
import pygame
import numpy as np
import matplotlib.pyplot as plt
class board:
    def __init__(self, rows, col, screen):
        self.rows = rows
        self.col = col
        self.screen = screen
        
        


        self.initialize()

        

        #print(win[0])
        

        
    def initializeS(self):
        
        self.state = [3, 0]

    def initializeP(self):
        for i in range(self.rows):
            for j in range(self.col):
                if self.board[i][j] == 'p':
                    self.board[i][j] = 0
                    
        self.board[self.state[0]][self.state[1]] = 'p'

        

        

        
    def initialize(self):
        self.board = []
        self.boardRect = []
        self.Q = []
        self.actions = ['up', 'down', 'left', 'right']
        self.win = [3, self.col - 1]
        # self.nxtState = []
        self.initializeS()
        self.epsilon = .01

        for i in range(self.rows):
            self.board.append([])
            self.boardRect.append([])
            self.Q.append([])
            for j in range(self.col):
                
                self.Q[i].append([])
                self.board[i].append(0)
                self.boardRect[i].append(pygame.Rect((j * 25, i * 25, 20, 20)))

                pygame.draw.rect(self.screen, (0, 0, 255), self.boardRect[i][j])

                for k in range(4):
                    self.Q[i][j].append(0)
                    
        
        self.board[self.win[0]][self.win[1]] = 1

        self.board[self.state[0]][self.state[1]] = 'p'
        
        
    #reward for state
    def reward(self, state):
        if state == self.win:
            return 1
        else:
            return 0

    #choose a action ep greedy
    def choose(self):

        choice = np.random.random()
        
        #print(self.actions[np.random.randint(len(self.actions))])
        if choice < 1 - self.epsilon:
            print((self.Q[self.state[0]][self.state[1]]))
            if np.sum(self.Q[self.state[0]][self.state[1]]) == 0:
                action = self.actions[np.random.randint(0, len(self.actions))]
            else:
                
                action = self.actions[np.argmax(self.Q[self.state[0]][self.state[1]])]


        else:
            action = self.actions[np.random.randint(0, len(self.actions))]



        return action

    #take action to get next state.
    # if on edge or goes into wall state doesn't change.
    def nextState(self, action):
        print(self.state)
        if action == 'up' and (self.state[0] > 0 and self.board[self.state[0] - 1][self.state[1]] != 'p'):
            return [self.state[0] - 1, self.state[1]]

        elif action == 'down' and (self.state[0] < self.rows - 1 and self.board[self.state[0] + 1][self.state[1]] != 'p'):
            return [self.state[0] + 1, self.state[1]]

        elif action == 'right' and (self.state[1] < self.col - 1 and self.board[self.state[0]][self.state[1] + 1] != 'p'):
            return [self.state[0], self.state[1] + 1]

        elif action == 'left' and (self.state[1] > 0 and self.board[self.state[0]][self.state[1] - 1] != 'p'):
            return [self.state[0], self.state[1] - 1]

        else:
            return [self.state[0], self.state[1]]

                
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
        self.board = board(rows, col,self.screen)

        self.player = pygame.image.load('index.png')
        self.player = pygame.transform.scale(self.player, (10, 10)).convert()
        self.playerRec = self.player.get_rect()
        self.screen.blit(self.player, self.playerRec)
        self.episodes = 50
        self.alpha = .5
        self.gamma = .9

        self.epcount_q = np.zeros(self.episodes)
        for i in range(4):
            self.epcount_q += self.play_q_learning()
        
        plt.plot(self.epcount_q)

        self.epcount_sarsa = self.play_sarsa()

        
    
    def showPlayer(self):
        self.board.draw()
        for i in range(self.board.rows):
            for j in range(self.board.col):
                if self.board.board[i][j] == 'p':
                    #print('moved')
                    self.playerRec.center = self.board.boardRect[i][j].center
                    #print(self.board.boardRect[i][j].center)
                    self.screen.blit(self.player, self.playerRec)
        
        pygame.display.update()

    def play_q_learning(self):

        self.board.initialize()
        

        epcount_q = np.zeros(self.episodes)

        for i in range(self.episodes):
            self.board.initializeS()
            self.board.initializeP()
            reward = 0
            while reward == 0:

                action = self.board.choose()
                nxtState = self.board.nextState(action)
                reward = self.board.reward(nxtState)
                if reward == 1:
                    print(reward)
                print(self.board.state)

                nxtQ = np.max(self.board.Q[nxtState[0]][nxtState[1]])
                currentQ = self.board.Q[self.board.state[0]][self.board.state[1]]
                #print(currentQ, nxtQ, self.board.board)

                currentQ[self.board.actions.index(action)] = currentQ[self.board.actions.index(action)] + self.alpha * (reward + self.gamma * nxtQ - currentQ[self.board.actions.index(action)])
                
                self.board.board[self.board.state[0]][self.board.state[1]] = 0
                self.board.state = nxtState
                self.board.board[self.board.state[0]][self.board.state[1]] = 'p'
                self.showPlayer()
                epcount_q[i] += 1
        #self.board.draw()

        return epcount_q      
        # print(self.epcount_q)
        # plt.plot(self.epcount_q)


    def play_sarsa(self):

        self.board.initialize()
        

        epcount_q = np.zeros(self.episodes)

        for i in range(self.episodes):
            self.board.initializeS()
            self.board.initializeP()
            reward = 0
            while reward == 0:

                action = self.board.choose()
                nxtState = self.board.nextState(action)
                reward = self.board.reward(nxtState)
                if reward == 1:
                    print(reward)
                print(self.board.state)

                nxtQ = np.max(self.board.Q[nxtState[0]][nxtState[1]])
                currentQ = self.board.Q[self.board.state[0]][self.board.state[1]]
                #print(currentQ, nxtQ, self.board.board)

                currentQ[self.board.actions.index(action)] = currentQ[self.board.actions.index(action)] + self.alpha * (reward + self.gamma * nxtQ - currentQ[self.board.actions.index(action)])
                
                self.board.board[self.board.state[0]][self.board.state[1]] = 0
                self.board.state = nxtState
                self.board.board[self.board.state[0]][self.board.state[1]] = 'p'
                self.showPlayer()
                epcount_q[i] += 1
        #self.board.draw()

        return epcount_q      
        
                











# self.board[self.state[0]][self.state[1]] = 0
# self.state = [self.state[0] - 1], [self.state[1]]
# self.board[self.state[0]][self.state[1]] = 'p'