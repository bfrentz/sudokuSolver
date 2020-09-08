#!/usr/bin/env python3

"""
GUI for playing sudoku
Bryce Frentz
September 2020
"""

import pygame
import time
import requests
import json


pygame.font.init()


"""
The basic idea in the backtracking algorithm is to just to test each new solution 
against the constraint and revert to the previous state or step immediately 
if our current solution isn't valid.

Starting with an incomplete board:
1. Find an empty space by iterating like reading a book, L->R, Top->Bot
2. Attempt to place the digits 1-9 in that space
3. Check if that digit is valid in the current spot based on the current board
    a. If the digit is valid, recursively attempt to fill the next space (and eventually the
        whole board) using steps 1-3.
    b. If it is not valid, reset the square you just filled and go back to the previous step.
4. Once the board is full by the definition of this algorithm we have found a solution.
"""


def get_board():
    valid_difficulty = False
    while not valid_difficulty:
        diff = input("What difficulty of sudoku puzzle (1=easy, 2=medium, 3=hard)? \n")
        if diff == '1':
            difficulty = 'easy'
            valid_difficulty = True
        elif diff == '2':
            difficulty = 'medium'
            valid_difficulty = True
        elif diff == '3':
            difficulty = 'hard'
            valid_difficulty = True
        else:
            print("\nPlease input a valid difficulty.\n")

    link = 'https://sugoku.herokuapp.com/board?difficulty='+difficulty
    req = requests.get(link)
    board = json.loads(req.text[9:-2])
    return board

    # #DEBUG
    # print(req.text[9:-2])
    # print(b[2])

# DEBUG
#get_board()


def find_empty(board):
    """
    Finds the next empty space in the board
    input: board: 2d list of ints and empty characters (could be 'X', 0, or whatever)
    output: tuple (int, int) for row col of next empty spot
    """
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)    # (row, column)

    # If there are no more empty spots don't return
    return None

# DEBUG
#print(find_empty(board1))


def valid_number(board, number, position):
    """
    Returns if the attempted move is valid
    input: board: 2d list of ints and empty character (could be 'X', 0, or whatever)
    input: number: int of guess
    input: position: tuple for spot in grid (row, column)
    output: bool
    """


    # Check row
    for i in range(len(board[position[0]])):
        #print(board[position[0]][i], end=' ')
        if board[position[0]][i] == number and position[1] != i:
            #print("Number in row.")
            return False

    #print()

    # Check column
    for j in range(len(board)):
        #print(board[j][position[1]], end='\n')
        if board[j][position[1]] == number and position[0] != j:
            #print("Number in col.")
            return False

    # Check boxes
    # 0,0 | 0,1 | 0,2
    # ---------------
    # 1,0 | 1,1 | 1,2
    # ---------------
    # 2,0 | 2,1 | 2,2

    box_x = position[0] // 3
    box_y = position[1] // 3

    # # DEBUG
    # print()
    # print(box_x, box_y)
    # print()

    for i in range(box_x*3, box_x*3+3):
        for j in range(box_y*3, box_y*3+3):
            # # DEBUG
            # print(i, j)
            # print(board[i][j])
            if board[i][j] == number and position[0] != i and position[1] !=j:
                return False

    return True


# DEBUG
#print(valid_number(board1, 4, (6,0)))



# Grid is...
class Grid:
    board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

    #board = get_board()

    def __init__(self, rows, columns, width, height):
        self.rows = rows
        self.columns = columns
        self.width = width
        self.height = height
        self.model = None
        self.selected = None
        #self.board = get_board()
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(columns)] for i in range(rows)]

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.columns)] for i in range(self.rows)]

    def place(self, val):
        row, column = self.selected
        if self.cubes[row][column].value == 0:
            self.cubes[row][column].set(val)
            self.update_model()

            if valid_number(self.model, val, (row,column)) and self.solve():
                return True
            else:
                self.cubes[row][column].set(0)
                self.cubes[row][column].set_temp(0)
                self.update_model()
                return False

    def sketch(self, val):
        row, column = self.selected
        self.cubes[row][column].set_temp(val)


    def draw(self, win):
        # Draw grid lines
        gap = self.width / 9
        for i in range(self.rows+1):
            if i%3 == 0 and i != 0:
                thickness = 4
            else:
                thickness = 1

            pygame.draw.line(win, (0,0,0), (0,i*gap), (self.width, i*gap), thickness)
            pygame.draw.line(win, (0,0,0), (i*gap, 0), (i*gap, self.height), thickness)

        # Draw cubes
        for i in range(self.rows):
            for j in range(self.columns):
                self.cubes[i][j].draw(win)


    def select(self, row, column):
        # Reset others
        for i in range(self.rows):
            for j in range(self.columns):
                self.cubes[i][j].selected = False

        self.cubes[row][column].selected = True
        self.selected = (row, column)


    def clear(self):
        row, column = self.selected
        if self.cubes[row][column].value == 0:
            self.cubes[row][column].set_temp(0)


    def click(self, position):
        """
        input: position is the tuple of coordinate
        output: int tuple (row, column)
        """

        if position[0] < self.width and position[1] < self.height:
            gap = self.width / 9
            x = position[0] // gap
            y = position[1] // gap
            return (int(y), int(x))
        else:
            return None


    def is_finished(self):
        # Check for any empty spots
        for i in range(self.rows):
            for j in range(self.columns):
                if self.cubes[i][j].value == 0:
                    return False

        return True


    def solve(self):
        """
        Solves a sudoku board recursively using backtracking
        input: board: 2d list of ints and empty character (could be 'X', 0, or whatever)
        output: solved board
        """
        # Check and return for last square
        empty = find_empty(self.model)
        if not empty:
            return True
        else:
            row, column = empty

        # Loop through numbers 1-9 to see if they work
        for i in range(1, 10):
            if valid_number(self.model, i, (row, column)):
                self.model[row][column] = i

                # Recursive check
                if self.solve():
                    return True

                self.model[row][column] = 0

        return False
       


# Cubes are....
class Cube:
    standard = 9

    def __init__(self, value, row, column, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.column = column
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.column * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128,128,128))
            win.blit(text, (x+5, y+5))
        elif not (self.value == 0):
            text = fnt.render(str(self.value), 1, (0,0,0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(win, (255,0,0), (x,y,gap,gap), 3)


    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


def redraw_window(win, board, time, strikes):
    win.fill((255,255,255))

    # Draw time
    fnt = pygame.font.SysFont("comicsans", 40)
    text = fnt.render("Time: " + format_time(time), 1, (0,0,0))
    win.blit(text, (540 - 160, 560))

    # Draw strikes
    text = fnt.render("X " * strikes, 1, (255,0,0))
    win.blit(text, (20, 560))

    # Draw grid and board
    board.draw(win)


def format_time(seconds):
    sec = seconds%60
    minute = sec//60
    hour = minute//60

    elapsed = ' ' + str(minute) + ':' + str(sec)
    return elapsed


# Main game
def main():
    title = 'Sudoku Game!'

    win = pygame.display.set_mode((540, 600))
    pygame.display.set_caption(title)

    board = Grid(9, 9, 540, 540)

    key = None
    run = True
    start = time.time()
    strikes = 0

    while run:

        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            print('Success!')
                        else:
                            print('Incorrect.')
                            strikes += 1
                        key = None

                        if board.is_finished():
                            print('The game has ended.')
                            run = False


            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                clicked = board.click(position)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key != None:
            board.sketch(key)

        redraw_window(win, board, play_time, strikes)
        pygame.display.update()





# Play
main()
pygame.quit()
