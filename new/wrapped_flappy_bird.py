#####################################################################
#  SNAKER.py  - A simple SNAKE game written in Python and Pygame
#  This is my first Python / Pygame game written as a learning
#  exercise.
#  Version: 0.1
#  Date:  24 August 2008
#  Author:  R Brooks
#  Author email:  rsbrooks@gmail.com
#####################################################################



import numpy as np
import sys
import random
import pygame
import pygame.surfarray as surfarray
from pygame.locals import *
from itertools import cycle
import os,sys

os.environ["SDL_VIDEODRIVER"]="dummy"


counter = 0


FPS = 1000000000000




######## CONSTANTS

WINSIZE = [480, 480]
SCREENWIDTH  = WINSIZE[0]
SCREENHEIGHT = WINSIZE[1]

WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
RED = [255, 0, 0]
GREEN = [0, 255, 0]

BLOCKSIZE = [15, 15]

UP = 1
DOWN = 3
RIGHT = 2
LEFT = 4

MAXX = WINSIZE[0]
MINX = 0
MAXY = WINSIZE[1]
MINY = 0

SNAKESTEP = 20

X_apple = WINSIZE[0] / SNAKESTEP
Y_apple = WINSIZE[1] / SNAKESTEP

TRUE = 1
FALSE = 0

LEN_MEAN = np.array([])

prevDir = RIGHT

_test = 1

######## ######## ########

pygame.init()

#TODO Delete one of them FPSCLOCK to CLOCK
# FPSCLOCK = pygame.time.Clock()
# SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
# pygame.display.set_caption('SNAKE GAME')

clock = pygame.time.Clock()
screen = pygame.display.set_mode(WINSIZE)
pygame.display.set_caption('SNAKER')
screen.fill(BLACK)


class GameState:
    def __init__(self):
        self.direction = RIGHT  # 1=up,2=right,3=down,4=left
        self.snakexy = [100, 20]
        self.snakelist = [[100, 20], [80, 20], [60, 20]]
        self.counter = 0
        self.score = 0
        self.appleonscreen = 0
        self.newdirection = RIGHT
        self.snakedead = FALSE
        self.gameregulator = 6
        self.gamepaused = 0
        self.growsnake = 0  # added to grow tail by two each time
        self.snakegrowunit = 2  # added to grow tail by two each time
        self.applexy = [-20,-20]
        self.step = 0
        DEATH = False

    def frame_step(self, input_actions):

        # pygame.event.pump()

        reward = 0

        terminal = False

        if sum(input_actions) != 1:
            raise ValueError('Multiple input actions!')

        #TODO Check the output layer has 4 elements
        # 1=up,2=right,3=down,4=left
        # input_actions[0] == 1: do nothing
        # input_actions[1] == 1: snake up
        # input_actions[2] == 1: snake right
        # input_actions[3] == 1: snake down
        # input_actions[4] == 1: snake left


        # print(self.snakexy,self.snakedead,"dir :",self.direction,"input :", input_actions)



        #direction Change it depends on input direction
        if input_actions[4] == 1 and (not self.direction == RIGHT):
            self.direction = LEFT
            prevDir = LEFT
        elif input_actions[2] == 1 and (not self.direction == LEFT):
            self.direction = RIGHT
            prevDir = RIGHT
        elif input_actions[1] == 1 and (not self.direction == DOWN):
            self.direction = UP
            prevDir = UP
        elif input_actions[3] == 1 and (not self.direction == UP):
            self.direction = DOWN
            prevDir = DOWN

        if self.direction == RIGHT:
            self.snakexy[0] = self.snakexy[0] + SNAKESTEP
            if self.snakexy[0] >= MAXX:
                self.snakedead = TRUE

        elif self.direction == LEFT:
            self.snakexy[0] = self.snakexy[0] - SNAKESTEP
            if self.snakexy[0] < MINX:
                self.snakedead = TRUE

        elif self.direction == UP:
            self.snakexy[1] = self.snakexy[1] - SNAKESTEP
            if self.snakexy[1] < MINY:
                self.snakedead = TRUE

        elif self.direction == DOWN:
            self.snakexy[1] = self.snakexy[1] + SNAKESTEP
            if self.snakexy[1] >= MAXY:
                self.snakedead = TRUE

        if len(self.snakelist) > 3 and self.snakelist.count(self.snakexy) > 0:
            self.snakedead = TRUE

        if self.appleonscreen == 0:
            good = FALSE
            while good == FALSE:
                x = random.randrange(1, X_apple)
                y = random.randrange(1, Y_apple)
                self.applexy = [int(x * SNAKESTEP), int(y * SNAKESTEP)]
                if self.snakelist.count(self.applexy) == 0:
                    good = TRUE
            self.appleonscreen = 1

        self.snakelist.insert(0, list(self.snakexy))
        # print(self.snakexy,self.applexy)
        # TODO ADD reward
        if self.snakexy[0] == self.applexy[0] and self.snakexy[1] == self.applexy[1]:
            self.appleonscreen = 0
            self.score = self.score + 1
            self.growsnake = self.growsnake + 1
            reward = 1 *len(self.snakelist)
            self.step = 0
        # elif self.growsnake > 0:
        #     self.growsnake = self.growsnake + 1
        #     if self.growsnake == self.snakegrowunit:
        #         self.growsnake = 0
        else:
            self.snakelist.pop()

        global LEN_MEAN
        global _test
        if self.snakedead:
            terminal = True
            LEN_MEAN = np.append(LEN_MEAN ,len(self.snakelist))
            if(LEN_MEAN.shape[0]>1000):
                LEN_MEAN = np.delete(LEN_MEAN,0)	
            print(WINSIZE,"=>", "avg : ","%.2f" %round(np.mean(LEN_MEAN),2),"MAX :", np.amax(LEN_MEAN),"MIN : ", np.amin(LEN_MEAN), "   " ,end = "")

            _test = _test%9+1
            for value in range(_test):
                print(">",end = "")
            for value in range(10-_test):
                print("@",end = "")
            print("")
            self.__init__()
            reward = -1
        elif self.step > (WINSIZE[0]/SNAKESTEP)*(WINSIZE[1]/SNAKESTEP):
            #print("step over", self.step)
            reward = -0.8
        else:
            _temp = 0
            #print("", self.step)



        test = self.growsnake

        #render
        ###### RENDER THE SCREEN ###############

        # Clear the screen
        screen.fill(BLACK)
        # Output the array elements to the screen as rectangles ( the snake)
        for element in self.snakelist:
            pygame.draw.rect(screen, RED, Rect(element, BLOCKSIZE))

        # Draw the apple
        pygame.draw.rect(screen, GREEN, Rect(self.applexy, BLOCKSIZE))

        # Flip the screen to display everything we just changed
        pygame.display.flip()

        image_data = pygame.surfarray.array3d(pygame.display.get_surface())
        # pygame.display.update()
	#clock.tick(FPS)




        self.step = self.step+1
        return image_data, reward, terminal,len(self.snakelist)
