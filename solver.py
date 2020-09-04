#!/usr/bin/env python3

"""
Sudoku solver using the backtracking algorithm
Bryce Frentz
September 2020
"""

import pprint

# Boards will be list of 9 separate lists
# One list for each row
board1 = [
    [7,8,'X',4,'X','X',1,2,'X'],
    [6,'X','X','X',7,5,'X','X',9],
    ['X','X','X',6,'X',1,'X',7,8],
    ['X','X',7,'X',4,'X',2,6,'X'],
    ['X','X',1,'X',5,'X',9,3,'X'],
    [9,'X',4,'X',6,'X','X','X',5],
    ['X',7,'X',3,'X','X','X',1,2],
    [1,2,'X','X','X',7,4,'X','X'],
    ['X',4,9,2,'X',6,'X','X',7]
]

def print_board(board):
    # Print grid lines around board
    # Print | on edge and after every third number in list
    # Print grid line after every third row
    line = '-------------------------'

    # loop over rows
    for i in range(len(board)):
        if i == 0 or i % 3 == 0:
            print(line)

        # Loop over columns in row
        for j in range(len(board[i])):
            if j == 0 or j % 3 == 0:
                print('|', end=' ')

            if j == 8:
                print(board[i][j], '|')
            else:
                print(board[i][j], end=' ')

    print(line)


print_board(board1)

"""
The basic idea in the backtracking algorithm is to just to test each new solution 
against the constraint and revert to the previous state or step immediately 
if our current solution isn't valid.

Starting with an incomplete board:
1. Find an empty space by iterating like reading a book, L->R, Top->Bot
2. Attempt to place the digits 1-9 in that space
3. Check if that digit is valid in the current spot based on the current board
    a. If the digit is valid, recursively attempt to fill the board using steps 1-3.
    b. If it is not valid, reset the square you just filled and go back to the previous step.
4. Once the board is full by the definition of this algorithm we have found a solution.
"""


