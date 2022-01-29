# Author: Israel Kwilinski
# Filename: sieve.py
# Date Created: Jan. 20, 2022
# Description: Visualization tool for the famous "Sieve of Eratosthenes" algorithm.
#              This algorithm "sieves" out primes under a certain limit much faster than individual prime tests.
#              Written in Python3 using pyglet.

import pyglet
import numpy as np
from pyglet.gl import glClearColor
from pyglet.window import key
import sys, argparse

TITLE = "Sieve of Eratosthenes"
TIME_AFTER_COMPLETION = 35
PADDING = [(1, "C") for _ in range(TIME_AFTER_COMPLETION)]
LIGHT_GRAY = [0.2,0.2,0.2,1.0]
WHITE = [0.0,0.0,0.0,1.0]
LIGHT_GREEN = (0,230,0)
LIGHT_BLUE = (153, 255,255)
RED = (255,51,51)



def primeSieve(LIMIT):
    """
    Finds both primes and composite numbers using the Sieve of Eratosthenes.
    Written as a generator that yields both an integer and 'P' or 'C' depending on
    whether the integer was prime or composite.
    Yields the sequence in which to animate the squares on the grid.

    LIMIT - The found primes and composites will be less than LIMIT
    """
    yield 1, "C" # 1 is composite
    sieve = np.zeros(LIMIT - 2,dtype=bool) # We don't need to include 0 and 1.
    startIndex = 0
    while (startIndex < LIMIT - 2):
        if not sieve[startIndex]:
            prime = startIndex + 2
            yield prime , "P"
            for i in range(prime**2 - 2, LIMIT - 2, prime): #  We can start at the prime's square when searching for composites
                sieve[i] = True
                yield i + 2, "C"
        startIndex += 1 if startIndex == 0 else 2 # We can start searching 2 at a time since 2 is only even prime


def drawGrid(lines_list, w, h, N, batch=None):
    """
    Draws N horizontal and N vertical lines to form a grid.

    lines_list - list to to add the created lines
    w - width of the window
    h - height of the Window
    N - dimensions of the sqaures
    batch - batch to insert created lines in
    """
    for i in range(1, N):
        linex = pyglet.shapes.Line((w / N) * i, 0, (w / N) * i, h, width=4, color=LIGHT_GREEN, batch=batch)
        linex.opacity = 150
        liney = pyglet.shapes.Line(0, (w / N) * i, w, (w / N) * i, width=4, color=LIGHT_GREEN, batch=batch)
        liney.opacity = 150
        lines_list.append(linex)
        lines_list.append(liney)

def drawSquares(squares_list, w, h, N, info, batch=None):
    """
    Draws N^2 squares. Sets their visibilty initially to false to reset the animation

    sqaures_list - list to to add the created lines
    w - width of the window
    h - height of the Window
    N - dimensions of the sqaures
    info - dictionary with key representing a number on the grid (0 < key < N^2 + 1) and a
           value being coordinates to draw the square that is labeled. This is in a tuple of (x, y).
    batch - batch to insert created lines in
    """
    for num in range(1, N**2 + 1):
        x, y = info[num]
        currentSquare = pyglet.shapes.Rectangle(x, y, w / N, w / N, LIGHT_BLUE, batch=batch)
        currentSquare.opacity = 128
        currentSquare.visible = False # Set to False to reset the animation
        squares_list.append(currentSquare)


class mainWindow(pyglet.window.Window):
    """
    Class representing a window for the animation.
    """
    def __init__(self, *args, **kwargs):
        """
        Assigns default values to each field. Draws the grey background.
        Creates an initial drawing of each type of shape (lines, numbers, squares) by representing them each in a batch.
        """
        super().__init__(*args, **kwargs)
        assert self.width ==  self.height # Only deal with square grids
        glClearColor(*LIGHT_GRAY)
        self.N = 10
        self.numbers = pyglet.graphics.Batch()
        self.grid = pyglet.graphics.Batch()
        self.squares = pyglet.graphics.Batch()
        self.square_coords = self.drawNumbers()
        self.data = list(primeSieve(self.N**2 + 1)) + list(PADDING) # Gets the data for the sequence in which to animate the squares
        self.line_list, self.square_list = [], []
        drawGrid(self.line_list, self.width, self.height, self.N, self.grid)
        drawSquares(self.square_list, self.width, self.height, self.N, self.square_coords, self.squares)
        self.currentIndex = 0 # Current index to start the animation

    def drawNumbers(self):
        """
        Draws the numbers on grid.
        Returns a dictionary of where to put the squares (ie. their coordinates in a tuple)
        """
        coordinate_info = {}
        # Draw numbers on the grid
        font_size = 34 - self.N # Adjust the fontsize to be smaller as the N grows larger
        y_coord, y_decrement = self.height, self.width / self.N
        for number in range(1, self.N**2 + 1):
            x_coord = self.width/self.N * ((number - 1) % self.N)
            center_x = x_coord + (self.width / self.N / 2)
            center_y = y_coord - (self.width / self.N / 2)
            coordinate_info[number] = (x_coord, y_coord - self.width/self.N)
            label = pyglet.text.Label(str(number), font_size=font_size, x=center_x, y=center_y, anchor_x='center', anchor_y='center', batch=self.numbers)
            if number % self.N == 0:
                y_coord -= y_decrement
        return coordinate_info

    def on_key_press(self, symbol, modifiers):
        """
        Enables user to be able to quit the program by hitting 'Q'.
        Allows for user control of the size of the grid (N).
        Minimum size is N = 10 (10 x 10) and maxmimum size is N = 18 (18 x 18).
        When the dimensions (N) are changed the animation resets.
        If the key pressed yields the same dimensions the animation sequence does not reset.
        """
        if symbol == key.Q:
            print("The 'Q' key was pressed. Quitting now...")
            self.close()
        if key._1 <= symbol <= key._9 and int(symbol) - 39 != self.N:
            self.N = int(symbol) - 39 # Convert key that was pressed into a valid N
            self.grid = pyglet.graphics.Batch()
            self.numbers = pyglet.graphics.Batch()
            self.squares = pyglet.graphics.Batch()
            self.square_coords = self.drawNumbers() # Redraw the numbers
            self.line_list, self.square_list = [], []
            drawGrid(self.line_list, self.width, self.height, self.N, self.grid) # Redrawn the grid
            drawSquares(self.square_list, self.width, self.height, self.N, self.square_coords, self.squares) # Redraw the squares
            self.currentIndex = 0
            self.data = list(primeSieve(self.N**2 + 1)) + list(PADDING) # Find the new prime/composite sequence


    def on_draw(self):
        """
        Preforms the whole animation sequence (Note that on_draw is called every 1 / FRAME_RATE ticks per second).
        Utilizes currentIndex to decide which square from the animation sequence (self.data) to make visible.
        Once the animation is complete there is a bit of "padding" included to give some time to see
        the fully filled in grid. After the "padding" been iterated through the animation resets.
        Primes are drawn in red and composites in blue.
        """
        self.clear()
        self.squares.draw()
        self.grid.draw()
        self.numbers.draw()
        currentNum, type = self.data[self.currentIndex]
        self.square_list[currentNum - 1].visible = True
        self.square_list[currentNum - 1].color = LIGHT_BLUE if type == 'C' else RED
        self.currentIndex += 1
        if self.currentIndex == len(self.data): # Ran out of data -> Reset the animation
            self.currentIndex = 0
            self.square_list = []
            drawSquares(self.square_list, self.width, self.height, self.N, self.square_coords, self.squares) # Set squares back to invisible

    def update(self, dt): # Required method to overload
        pass

if __name__ == '__main__':
    """
    Driver for the program.
    Command Line Argments should be of the form: sieve.py [-h] [--frame-rate FRAME_RATE] [--dimensions DIMENSIONS]
    Minimum dimension is 800. Maxmimum dimension is 2000.
    Frame rate should be between 10 and 40.
    """
    parser = argparse.ArgumentParser(description='''Process two flags each containing an integer.
        One flag controls frame rate and the the dimension of the window being drawn.
        Once the animation has started press the 'Q' key to end the program.''')
    parser.add_argument('--frame-rate', type=int, nargs=1, default=[12], help='an integer controlling how my frames per second should be drawn.')
    parser.add_argument('--dimensions', type=int, nargs=1, default=[800], help='an integer controlling the square dimensions of the window.')
    args = vars(parser.parse_args())
    DIMENSIONS = min(max(800, args['dimensions'][0]), 2000)
    FRAME_RATE = min(max(10, args['frame_rate'][0]), 40)
    window = mainWindow(DIMENSIONS, DIMENSIONS, TITLE, resizable=False)
    pyglet.clock.schedule_interval(window.update, 1 / FRAME_RATE) # Sets the fps
    pyglet.app.run()
