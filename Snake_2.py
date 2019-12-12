
########################################################################################
# This code is for Snake v 2.0 in python
# Created November 21, 2019
# Edited:
########################################################################################

# import packages
import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox
 

########################################################################################
# define the individual portions that comprise the snake
########################################################################################
class cube(object):
    rows = 20
    w = 500
    def __init__(self,start,dirx=1,diry=0,color=(255,0,0)):
        self.pos = start
        # set it was a direction so that it starts off moving
        self.dirx = 1
        self.diry = 0
        self.color = color
 
       
    def move(self, dirx, diry):
        self.dirx = dirx
        self.diry = diry
        # take the previous position's X,Y coords and get the new position
        self.pos = (self.pos[0] + self.dirx, self.pos[1] + self.diry)
 
    def draw(self, surface, eyes=False):
        dis = self.w // self.rows # same calculation as the grid
        i = self.pos[0] # initial row
        j = self.pos[1] # initial column
 
        # draw a rectangle making sure that the grid lines will remain visible
        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis-2, dis-2))
        
        #     
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)
       
 
########################################################################################
# define the snake itself
########################################################################################
class snake(object):
    # create empty lists
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirx = 0
        self.diry = 1
 
    def move(self):
        # always comes first
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
 
            # grab all the key presses
            keys = pygame.key.get_pressed()
 
            # loop through all the keystrokes
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirx = -1
                    self.diry = 0
                    # add key for current position and define the direction of any turns in turn list
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]
 
                elif keys[pygame.K_RIGHT]:
                    self.dirx = 1
                    self.diry = 0
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]
 
                elif keys[pygame.K_UP]:
                    self.dirx = 0
                    self.diry = -1
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]
 
                elif keys[pygame.K_DOWN]:
                    self.dirx = 0
                    self.diry = 1
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]
 
        # look through all the positions - index & 'cube' object
        for i, c in enumerate(self.body):
            p = c.pos[:] # if this position is in turn list, then the snake turns
            if p in self.turns:
                turn = self.turns[p] # grab the index
                # the direction we move is = the values stored in our turn list
                c.move(turn[0],turn[1])
                # once the last cube goes around the turn, drop the turn
                if i == len(self.body)-1:
                    self.turns.pop(p)
            
            # check whether the snake has reached the edge of the screen
            else:
                if c.dirx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
                elif c.dirx == 1 and c.pos[0] >= c.rows-1: c.pos = (0,c.pos[1])
                elif c.diry == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                elif c.diry == -1 and c.pos[1] <= 0: c.pos = (c.pos[0],c.rows-1)
                else: c.move(c.dirx,c.diry)
       
 
    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirx = 0
        self.diry = 1
 
 
    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirx, tail.diry
 
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))
 
        self.body[-1].dirx = dx
        self.body[-1].diry = dy
       
 
    def draw(self, surface):
        # if it's the first cube -> draws eyes
        for i, c in enumerate(self.body):
            # draws based on the cube-objects defined above
            if i ==0:
                c.draw(surface, True)
            else:
                c.draw(surface)
 

########################################################################################
# define functions to be used
######################################################################################## 
def drawGrid(w, rows, surface):
    # determine the number of rows in the grid
    size_betwn = w // rows
    x = 0
    y = 0
    # draw a line for every loop
    for l in range(rows):
        x = x + size_betwn
        y = y + size_betwn
 
        pygame.draw.line(surface, (255, 255, 255), (x, 0),(x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y),(w, y))
       
 
def redrawWindow(surface):
    global rows, width, s, food
    surface.fill((0, 0, 0)) # use black screen
    s.draw(surface)
    food.draw(surface)
    drawGrid(width,rows, surface) # draw a grid on the screen
    pygame.display.update()
 
 
def randomFood(rows, item):
 
    positions = item.body
 
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
       
    return (x,y)
 
 
def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass
 
 
def main():
    global width, rows, s, food
    # window dimensions
    width = 500
    # height = 500 can draw squares with only width
    rows = 20
    # set the parameters of the window
    win = pygame.display.set_mode((width, width))
    # color & starting position
    s = snake((255,0,0), (10,10))
    food = cube(randomFood(rows, s), color=(0,255,0))

    # define a flag & clock to be used:
    flag = True
    clock = pygame.time.Clock()
   
    while flag:
        pygame.time.delay(50) # delay 50 milliseconds
        clock.tick(10) # game won't run faster than 10 fps
        s.move()
        if s.body[0].pos == food.pos:
            s.addCube()
            food = cube(randomFood(rows, s), color=(0,255,0))
 
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                s.reset((10,10))
                
 
           
        redrawWindow(win)
 
       
    pass
 
 
 
main()