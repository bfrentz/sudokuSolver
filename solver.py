#!/usr/bin/env python3

"""
Sudoku solver using the backtracking algorithm
Bryce Frentz
September 2020
"""

import pprint

# Boards will be list of 9 separate lists
# One list for each row
EMPTY = 'X'
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
    line = '---------------------'
    print()

    # loop over rows
    for i in range(len(board)):
        if i != 0 and i % 3 == 0:
            print(line)

        # Loop over columns in row
        for j in range(len(board[i])):
            if j != 0 and j % 3 == 0:
                print('|', end=' ')

            if j == 8:
                print(board[i][j], end='\n')
            else:
                print(board[i][j], end=' ')

    #print(line)
    print()

# Debug
#print_board(board1)

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

def find_empty(board):
    # Loops through board to find if a position is empty
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == EMPTY:
                return (i, j)    # (row, column)

    # If there are no more empty spots don't return
    return None

# DEBUG
#print(find_empty(board1))

def valid_number(board, number, position):
    # Check against row
    # Check against column
    # Check against box

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

