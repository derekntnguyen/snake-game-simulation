#  -*- coding: utf-8 -*-
'''
Final Project

Multiple snakes of different lengths on a 2D lattice with food to increase their size
Boundary conditions: wall or periodic

Author: Derek Nguyen
Created: 2019-04-30
Modified: 2019-04-30
Due: 2019-05-01
'''

# %% codecell

import random
import numpy as np
import matplotlib # used to create interactive plots in the Hydrogen package of the Atom IDE
matplotlib.use('Qt5Agg') # used to create interactive plots in the Hydrogen package of the Atom IDE
import matplotlib.pyplot as plt

#=============================================================================
class Snake:
    """
    This is a class for to define a snake.
    """
    def __init__(self, position = (10, 10), symbol = 'bo', color = 'b', orientation = 'north', length = 5):
        """
        The constructor for Snake class.
        Parameters:
            position: starting position of the snake
            symbol: symbol for the snake head
            color: color of the snake
            orientation: initial travel direction of the snake
            length: length of the snake
        """
        self.xpos = position[0]
        self.ypos = position[1]

        # Set the initial location and orientation of the snakes as defined by the user
        if orientation == 'north':
            self.linexpos = [position[0]] * (length)
            self.lineypos = np.arange(position[1], position[1] - length, -1)
        elif orientation == 'south':
            self.linexpos = [position[0]] * (length)
            self.lineypos = np.arange(position[1], position[1] + length, 1)
        elif orientation == 'east':
            self.linexpos = np.arange(position[0], position[0] - length, -1)
            self.lineypos = [position[1]] * (length)
        elif orientation == 'west':
            self.linexpos = np.arange(position[0], position[0] + length, 1)
            self.lineypos = [position[1]] * (length)

        self.symbol = symbol
        self.color = color
        self.orientation = orientation
        self.length = length
        self.direction = None
        self.trapped = False
        self.grew = False

    def move(self, xmax, ymax, bc, occupied):
        """
        Function to move the snakes to an open position on the grid.
        Parameters:
            xmax
            ymax
            bc
            occupied

        For each boundary condition option ('wall' or 'periodic'), given a
        snake currently at position (xpos, ypos), determine which directions
        for the next move are disallowed because the site has already been
        occupied.
        """
        disallowed = set() #empty set object; will add disallowed directions
        if bc == 'wall':
            if self.ypos == ymax or occupied[self.xpos, self.ypos+1]:
                disallowed.add('north')
            if self.xpos == xmax or occupied[self.xpos+1, self.ypos]:
                disallowed.add('east')
            if self.ypos == 0 or occupied[self.xpos, self.ypos-1]:
                disallowed.add('south')
            if self.xpos == 0 or occupied[self.xpos-1, self.ypos]:
                disallowed.add('west')
        elif bc == 'periodic':
            if (self.ypos == ymax and occupied[self.xpos, (self.ypos+1) % ymax]) \
            or (self.ypos < ymax and occupied[self.xpos, self.ypos+1]):
                disallowed.add('north')
            if (self.xpos == xmax and occupied[(self.xpos+1) % xmax, self.ypos]) \
            or (self.xpos < xmax and occupied[self.xpos+1, self.ypos]):
                disallowed.add('east')
            if (self.ypos == 0 and occupied[self.xpos, (self.ypos-1) % ymax]) \
            or (self.ypos > 0 and occupied[self.xpos, self.ypos-1]):
                disallowed.add('south')
            if (self.xpos == 0 and occupied[(self.xpos-1) % xmax, self.ypos]) \
            or (self.xpos > 0 and occupied[self.xpos-1, self.ypos]):
                disallowed.add('west')

        # Use the set method 'difference' to get set of allowed directions
        allowed = {'north', 'east', 'south', 'west'}.difference(disallowed)

        if len(allowed) == 0:
            self.trapped = True #snake is trapped!
        else:
            """
            Randomly pick from the allowed directions; need to convert set
            object to a list because random.choice doesn't work on sets
            """

            self.direction = random.choice(list(allowed))
            if self.direction == 'north':
                if (bc == 'wall' and self.ypos < ymax) or bc == 'periodic':
                    self.ypos += 1
            elif self.direction == 'east':
                if (bc == 'wall' and self.xpos < xmax) or bc == 'periodic':
                    self.xpos += 1
            elif self.direction == 'south':
                if (bc == 'wall' and self.ypos > 0) or bc == 'periodic':
                    self.ypos -= 1
            elif self.direction == 'west':
                if (bc == 'wall' and self.xpos > 0) or bc == 'periodic':
                    self.xpos -= 1

            # advance the body of the snake to the previous coordinates of the head by appending those coordinates and subsequently removing the end term
            # based on the self.length variable of the snake if the snake encounters food
            for i in range(self.length-1,0,-1):
                self.linexpos[i] = self.linexpos[i-1]
                self.lineypos[i] = self.lineypos[i-1]

            self.linexpos = np.append(self.xpos, self.linexpos)
            self.lineypos = np.append(self.ypos, self.lineypos)

            """
            With periodic boundary conditions, it's possible that (xpos, ypos) could
            be off the grid (e.g., xpos < 0 or xpos > xmax). The Python modulo
            operator can be used to give exactly what we need for periodic bc. For
            example, suppose xmax = 20; then if xpos = 21, 21 % 20 = 1; if xpos = -1,
            -1 % 20 = 19. (Modulo result on a negative first argument may seem
            strange, but it's intended for exactly this type of application. Cool!)
            If 0 <= xpos < xmax, then modulo simply returns xpos. For example,
            0 % 20 = 0, 14 % 20 = 14, etc. Only special case is when xpos = xmax, in
            which case we want to keep xpos = xmax and not xpos % xmax = 0
            """
            if self.xpos != xmax:
                self.xpos = self.xpos % xmax
            if self.ypos != ymax:
                self.ypos = self.ypos % ymax


#=============================================================================
class Grid:
    """
    This is a class to define a grid for which the snake(s) can move about.
    """
    def __init__(self, snakes, gridsize = (20, 20), bc = 'wall', nSteps = 400, foodNum = 100):
        """
        Constructor for the Grid class.
        Parameters:
            snakes: tuple of snakes
            gridsize: tuple of numbers to define size of grid
            bc: periodic or wall
            nSteps: number of steps the snakes will slither
            foodNum: number of foods initially available to the snakes randomly distributed
        """
        self.snakes = snakes
        self.xmax = gridsize[0]
        self.ymax = gridsize[1]
        self.bc = bc
        self.nSteps = nSteps
        self.foodNum = foodNum
        self.food = []

        # creates 2 array ofs points for which the food is randomly distributed
        self.foodx = np.random.uniform(1, self.xmax, self.foodNum) # rows x columns
        self.foody = np.random.uniform(1, self.ymax, self.foodNum) # rows x columns

        self.point = []
        self.lines = []
        self.foodpoints = []
        #array to keep track of points that are occupied
        self.occupied = np.zeros([self.xmax + 1, self.ymax + 1], dtype = bool)

        plt.figure() #create new figure window if one is already open
        ax = plt.axes(xlim = (0, self.xmax), ylim = (0, self.ymax))
        f, = ax.plot(self.foodx,self.foody, marker = 'x', ls = '')
        self.foodpoints.append(f)

        for w in self.snakes: # plot the snake heads and snake bodies
            p, = ax.plot([w.xpos], [w.ypos], w.symbol)
            l, = ax.plot(w.linexpos, w.lineypos)
            self.occupied[w.xpos, w.ypos] = True
            self.occupied[w.linexpos,w.lineypos] = True
            self.point.append(p)
            self.lines.append(l)

        plt.title('Feeding Frenzy nStep = {}'.format(nSteps))

    def isCollision(self,x1,y1,x2,y2):
        '''
        Function to determine if 2 sets of points are the same, utilzied to check if snake head == food
        Parameters;
            x1: food x coordinate
            x2: food y coordinate
            y1: snake head x coordinate
            y2: snake head y coordinate
        '''
        if x1 == x2:
            if y1 == y2:
                return True
        return False

    def myfinal(self):
        """
        Function to advance the main program, calls the go function from the snake class to advance the snakes
        compares if the snakes come into contact with food, if they come into contact with food the length of
        the snake will increase
        """
        while not all([w.trapped for w in self.snakes]):
            for j in range(self.nSteps): # iterate for a set number of steps
                counter = self.nSteps - j
                plt.title('Feeding Frenzy nStep = {}'.format(counter))

                for i, w in enumerate(self.snakes):

                    w.move(self.xmax, self.ymax, self.bc, self.occupied) # moves the snakes

                    for x in range(len(self.foodx)): # iterates through all the points of food and checks if the head of the snake has come into contact with the food
                        for y in range(len(self.foody)):
                            if self.isCollision(x,y,w.xpos, w.ypos): # if the head = food, increase the length of the snake by 1
                                w.length += 1

                    self.occupied[w.linexpos[-1], w.lineypos[-1]] = False # set the previously occupied space by the snakes to be moveable=

                    # self.foodx = np.delete(self.foodx, x)
                    # self.foody = np.delete(self.foody, y)
                    # self.foodpoints.set_data(self.foodx, self.foody)

                    if not w.trapped: # if not trapped, set the following conditions
                        self.point[i].set_data(w.xpos, w.ypos)
                        self.lines[i].set_data(w.linexpos, w.lineypos)
                        self.occupied[w.xpos, w.ypos] = True
                        self.occupied[w.linexpos,w.lineypos] = True
                        """
                        When using periodic boundary conditions, a position on a
                        wall is identical to the corresponding position on the
                        opposite wall. So if a snake visits (x, ymax) then
                        (x, 0) must also be marked as occupied; if a snake vists
                        (0, y) then (xmax, y) must also be marked as occupied; etc.
                        """
                        if self.bc == 'periodic':
                            if w.xpos == self.xmax:
                                self.occupied[0, w.ypos] = True
                            elif w.xpos == 0:
                                self.occupied[self.xmax, w.ypos] = True
                            if w.ypos == self.ymax:
                                self.occupied[w.xpos, 0] = True
                            elif w.ypos == 0:
                                self.occupied[w.xpos, self.ymax] = True

                plt.pause(0.2)
            break
# Main program =================================================================
bigsnec = Snake(position = (5, 5), symbol = 'bo', color = 'b', orientation = 'north', length = 3)
largesnek = Snake(position = (15, 15), symbol = 'ro', color = 'r', orientation = 'south', length = 3)
fatsneck = Snake(position = (5, 15), symbol = 'go', color = 'g', orientation = 'east', length = 3)
snakes = (bigsnec, largesnek, fatsneck)
walk = Grid(snakes)
walk.myfinal()
