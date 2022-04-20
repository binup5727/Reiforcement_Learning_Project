from re import L


import pygame
import numpy as np
import matplotlib.pyplot as plt


from keras.models import Sequential
from keras.layers import InputLayer
from keras.layers import Dense

class board:
    def __init__(self, rows, col, screen):
        self.rows = rows
        self.col = col
        self.screen = screen
        self.board = []
        self.boardRect = []
        self.win = [3, self.col - 1]
        self.initializeS()

        for i in range(self.rows):

            self.board.append([])
            self.boardRect.append([])
        
            for j in range(self.col):
                
                self.board[i].append(0)
                self.boardRect[i].append(pygame.Rect((j * 25, i * 25, 20, 20)))

                pygame.draw.rect(self.screen, (0, 0, 255), self.boardRect[i][j])


                
    
        self.board[self.win[0]][self.win[1]] = 1

        self.board[self.state[0]][self.state[1]] = 'p'
        self.initialize()

        ##print(win[0])
        

        
    def initializeS(self):
        
        self.state = [3, 0]

    def initializeP(self):
        for i in range(self.rows):
            for j in range(self.col):
                if self.board[i][j] == 'p':
                    self.board[i][j] = 0
                    
        self.board[self.state[0]][self.state[1]] = 'p'

        

        

        
    def initialize(self):
        
        self.Q = []
        self.actions = ['up', 'down', 'left', 'right']
        
        # self.nxtState = []
        self.initializeS()
        self.epsilon = .01

        for i in range(self.rows):
            self.Q.append([])
            for j in range(self.col):
                
                self.Q[i].append([])
                

                for k in range(4):
                    self.Q[i][j].append(0)
                    
        
        self.board[self.win[0]][self.win[1]] = 1

        self.board[self.state[0]][self.state[1]] = 'p'

    def makeQ(self):
        Q = []

        for i in range(self.rows):
            Q.append([])
            for j in range(self.col):
                Q[i].append([])

                for k in range(4):
                    Q[i][j].append(0)

        return Q

        
        
    #reward for state
    def reward(self, state):
        if state == self.win:
            return 1
        else:
            return 0

    #choose a action ep greedy
    def choose(self, state):

        choice = np.random.random()
        
        ##print(self.actions[np.random.randint(len(self.actions))])
        if choice < 1 - self.epsilon:
            #print((self.Q[state[0]][state[1]]))
            if np.sum(self.Q[state[0]][state[1]]) == 0:
                action = self.actions[np.random.randint(0, len(self.actions))]
            else:
                
                action = self.actions[np.argmax(self.Q[state[0]][state[1]])]


        else:
            action = self.actions[np.random.randint(0, len(self.actions))]



        return action

    def choose_doubleq(self, QA, QB, state):

        choice = np.random.random()
        Q = (np.array(QA[state[0]][state[1]]) + np.array(QB[state[0]][state[1]]))
        ##print(Q)
        ##print(self.actions[np.random.randint(len(self.actions))])
        if choice < 1 - self.epsilon:
            
            if np.sum(Q) == 0:
                action = self.actions[np.random.randint(0, len(self.actions))]
            else:
                #print(np.argmax(Q))
                action = self.actions[np.argmax(Q)]


        else:
            action = self.actions[np.random.randint(0, len(self.actions))]



        return action

    def maxQ(self, Q):
        if np.sum(Q) == 0:
            action = np.random.randint(0, len(self.actions))
        else:
            #print(np.argmax(Q))
            action = np.argmax(Q)
        return action




    #take action to get next state.
    # if on edge or goes into wall state doesn't change.
    def nextState(self, action):
        #print(self.state)
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
        self.alpha = .7
        self.gamma = .9

        self.NN_play()

    def play(self):

        rng = 1
        # print('Double Q Learning')
        # self.epcount_double_q = np.zeros(self.episodes)
        # for i in range(rng):

        #     self.epcount_double_q += self.play_double_q()
        
        
        # plt.plot(self.epcount_double_q, label='Double Q learning')

        self.NN_play()

        # print('Q Learning')
        # self.epcount_q = np.zeros(self.episodes)
        # for i in range(rng):
        #     self.epcount_q += self.play_q_learning()
        
        # plt.plot(self.epcount_q, label='Q learning')

        # print('SARSA Learning')
        # self.epcount_sarsa = np.zeros(self.episodes)
        # for i in range(rng):
        #     self.epcount_sarsa += self.play_sarsa()


        

        # plt.xlabel('Episodes')
        # plt.ylabel('Steps per Episode')
        # plt.plot(self.epcount_sarsa, label='SARSA learning')
        # print('q lerning, SARSA, Double q learning')
        # print(np.min(self.epcount_q), np.min(self.epcount_sarsa), np.min(self.epcount_double_q))        
        # plt.legend()
        # plt.show()
        

    def NN_play(self):
        
        stateCalc = lambda s : s[0] * self.board.col + s[1]

        n = self.board.col * self.board.rows
        # self.board.draw()
        # self.board.initialize()
        
        #play q learning to get target q table
        epcount_q = np.zeros(self.episodes)
        epcount_q = self.play_q_learning()
        #print(self.board.Q)

        trueQ = np.zeros((n, 4))
        for i in range(self.board.rows):
            for j in range(self.board.col):
                for k in range(4):
                    #print(stateCalc(self.board.Q))
                    Qpos = [i, j]
                    trueQ[stateCalc(Qpos)][k] = self.board.Q[i][j][k]
        
        #print(trueQ)


        
        self.mod = Sequential()
        self.mod.add(InputLayer(batch_input_shape=(1, n)))
        self.mod.add(Dense(n * 2, activation='relu'))
        self.mod.add(Dense(4, activation='linear'))
        self.mod.compile(loss='mse', optimizer='adam', metrics=['mae'])
        

        

        

        self.mod.fit(np.identity(n), trueQ, epochs=1000)
        
        approxQ = [ [0 for i in range(self.board.col)] for k in range(self.board.rows)]
        for i in range(self.board.rows):
            for j in range(self.board.col):
                pos = [i, j]
                pos = stateCalc(pos)
                #print(self.mod.predict(np.identity(n)[pos:pos+1]))
                approxQ[i][j] = self.mod.predict(np.identity(n)[pos:pos+1])[0]

        approxQ = np.array(approxQ)
        trueQ = np.array(self.board.Q)
        diff = np.abs(trueQ - approxQ)
        print('true Q: ', trueQ, '\n\naprox Q: ', approxQ, '\n\ndifference: ', diff)

        #NN online training.....................................................................
        

        self.mod = Sequential()
        self.mod.add(InputLayer(batch_input_shape=(1, n)))
        self.mod.add(Dense(n * 2, activation='relu'))
        self.mod.add(Dense(4, activation='linear'))
        self.mod.compile(loss='mse', optimizer='adam', metrics=['mae'])
        
        epochs = self.episodes
        epcount_NN = np.zeros(epochs)
        self.board.draw()
        self.board.initialize()
        
        tempEps = .5

        for i in range(epochs):
            print(i, ' cycle')

            self.board.initializeS()
            self.board.initializeP()
            
            
            #state = stateCalc(self.board.state)
            
            reward = 0
            
            
            while reward == 0:
                #print("epsilon: ", tempEps)
                #print(epcount_NN[i], self.board.state)

                state = stateCalc(self.board.state)
                choice = np.random.random()
                
                ##print(self.actions[np.random.randint(len(self.actions))])
                if choice < tempEps:
                    #print('random')
                    actionNum = np.random.randint(0, len(self.board.actions))
                    action = self.board.actions[actionNum]

                else:
                    #print('greedy')
                    actionNum = np.argmax(self.mod.predict(np.identity(n)[state:state + 1]))
                    action = self.board.actions[actionNum]
                #print(actionNum, action, self.mod.predict(np.identity(n)[state:state + 1]))

                
                    

                nxtState = self.board.nextState(action)

                self.board.board[self.board.state[0]][self.board.state[1]] = 0
                self.board.state = nxtState
                self.board.board[self.board.state[0]][self.board.state[1]] = 'p'
                self.showPlayer()
                epcount_NN[i] += 1

                reward = self.board.reward(nxtState)
                nxtState = stateCalc(nxtState)

                

                targ = reward + (self.gamma * (np.max(self.mod.predict(np.identity(n)[nxtState:nxtState+1]))))

                targVec = self.mod.predict(np.identity(n)[state:state + 1])

                targVec[0][actionNum] = targ

                


                self.mod.fit(np.identity(n)[state:state + 1], targVec, epochs=1, verbose=0)

                
            if tempEps > .01:
                tempEps = tempEps * .7
            print(tempEps)
            

        plt.plot(epcount_NN)
        plt.plot(epcount_q)

        plt.show()
        print()

        onlineNNQ = [ [0 for i in range(self.board.col)] for k in range(self.board.rows)]
        for i in range(self.board.rows):
            for j in range(self.board.col):
                pos = [i, j]
                pos = stateCalc(pos)
                #print(self.mod.predict(np.identity(n)[pos:pos+1]))
                onlineNNQ[i][j] = self.mod.predict(np.identity(n)[pos:pos+1])[0]


        onlineNNQ = np.array(onlineNNQ)
        print(onlineNNQ)

        for i in range(self.board.rows):
            for j in range(self.board.col):
                for k in range(4):
                    #print(stateCalc(self.board.Q))
                    Qpos = [i, j]
                    onlineNNQ[stateCalc(Qpos)][k] = self.board.Q[i][j][k]

        plt.plot(onlineNNQ, LineStyle='none', markers='o')
        plt.show()
        


        
    
    def showPlayer(self):
        self.board.draw()
        for i in range(self.board.rows):
            for j in range(self.board.col):
                if self.board.board[i][j] == 'p':
                    ##print('moved')
                    self.playerRec.center = self.board.boardRect[i][j].center
                    ##print(self.board.boardRect[i][j].center)
                    self.screen.blit(self.player, self.playerRec)
        
        pygame.display.update()

    def play_q_learning(self):
        self.board.draw()
        self.board.initialize()
        

        epcount_q = np.zeros(self.episodes)

        for i in range(self.episodes):
            self.board.initializeS()
            self.board.initializeP()
            reward = 0
            while reward == 0:

                action = self.board.choose(self.board.state)
                nxtState = self.board.nextState(action)
                reward = self.board.reward(nxtState)
                # if reward == 1:
                #     #print(reward)
                # #print(self.board.state)

                nxtQ = np.max(self.board.Q[nxtState[0]][nxtState[1]])
                currentQ = self.board.Q[self.board.state[0]][self.board.state[1]]
                ##print(currentQ, nxtQ, self.board.board)

                currentQ[self.board.actions.index(action)] = currentQ[self.board.actions.index(action)] + self.alpha * (reward + self.gamma * nxtQ - currentQ[self.board.actions.index(action)])
                
                self.board.board[self.board.state[0]][self.board.state[1]] = 0
                self.board.state = nxtState
                self.board.board[self.board.state[0]][self.board.state[1]] = 'p'
                self.showPlayer()
                epcount_q[i] += 1
        #self.board.draw()
        #print(self.board.)

        return epcount_q      
        # #print(self.epcount_q)
        # plt.plot(self.epcount_q)


    def play_sarsa(self):
        self.board.draw()
        self.board.initialize()
        

        epcount_q = np.zeros(self.episodes)

        for i in range(self.episodes):
            self.board.initializeS()
            self.board.initializeP()
            action = self.board.choose(self.board.state)

            reward = 0
            while reward == 0:

                
                nxtState = self.board.nextState(action)
                reward = self.board.reward(nxtState)
                # if reward == 1:
                #     #print(reward)
                # #print(self.board.state)

                nxtAction = self.board.choose(nxtState)

                nxtQ = self.board.Q[nxtState[0]][nxtState[1]][self.board.actions.index(nxtAction)]
                currentQ = self.board.Q[self.board.state[0]][self.board.state[1]]
                ##print(currentQ, nxtQ, self.board.board)

                currentQ[self.board.actions.index(action)] = currentQ[self.board.actions.index(action)] + self.alpha * (reward + self.gamma * nxtQ - currentQ[self.board.actions.index(action)])
                
                self.board.board[self.board.state[0]][self.board.state[1]] = 0
                self.board.state = nxtState
                action = nxtAction
                self.board.board[self.board.state[0]][self.board.state[1]] = 'p'
                self.showPlayer()
                epcount_q[i] += 1
        #self.board.draw()
        #print(epcount_q)

        return epcount_q      
        
                
    def play_double_q(self):
        self.board.initialize()

        epcount_q = np.zeros(self.episodes)

        QA = self.board.Q
        QB = self.board.makeQ()

        for i in range(self.episodes):
            self.board.initializeS()
            self.board.initializeP()
            reward = 0
            while reward == 0:
                action = self.board.choose_doubleq(QA, QB, self.board.state)
                nxtState = self.board.nextState(action)
                reward = self.board.reward(nxtState)

                if np.random.random() > .5:
                    #update A
                    print(self.board.maxQ(QA[nxtState[0]][nxtState[1]]))
                    nxtQ = QB[nxtState[0]][nxtState[1]][self.board.maxQ(QA[nxtState[0]][nxtState[1]])]
                    currentQ = QA[self.board.state[0]][self.board.state[1]]
                    ##print(currentQ, nxtQ, self.board.board)

                    currentQ[self.board.actions.index(action)] = currentQ[self.board.actions.index(action)] + self.alpha * (reward + self.gamma * nxtQ - currentQ[self.board.actions.index(action)])
                
                else:
                    nxtQ = QA[nxtState[0]][nxtState[1]][self.board.maxQ(QB[nxtState[0]][nxtState[1]])]
                    currentQ = QB[self.board.state[0]][self.board.state[1]]
                    ##print(currentQ, nxtQ, self.board.board)

                    currentQ[self.board.actions.index(action)] = currentQ[self.board.actions.index(action)] + self.alpha * (reward + self.gamma * nxtQ - currentQ[self.board.actions.index(action)])
                

                self.board.board[self.board.state[0]][self.board.state[1]] = 0
                self.board.state = nxtState
                self.board.board[self.board.state[0]][self.board.state[1]] = 'p'
                self.showPlayer()
                epcount_q[i] += 1
                

        return epcount_q      








# self.board[self.state[0]][self.state[1]] = 0
# self.state = [self.state[0] - 1], [self.state[1]]
# self.board[self.state[0]][self.state[1]] = 'p'