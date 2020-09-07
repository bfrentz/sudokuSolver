#!/usr/bin/env python3

"""
Sudoku solver using the backtracking algorithm
Bryce Frentz
September 2020
"""

import pprint
import requests
import json


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


# Boards will be 2d list of 9 separate lists of ints
# One list for each row
EMPTY = 0
testBoard = [
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
]

def print_board(board):
    """
    Prints the board
    input: board: 2d List of ints and empty characters (could be 0, 0, or whatever)
    output: None
    """
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
    """
    Finds the next empty space in the board
    input: board: 2d list of ints and empty characters (could be 'X', 0, or whatever)
    output: tuple (int, int) for row col of next empty spot
    """
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == EMPTY:
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


def solve(board):
    """
    Solves a sudoku board recursively using backtracking
    input: board: 2d list of ints and empty character (could be 'X', 0, or whatever)
    output: solved board
    """

    # Check and return for last square
    empty = find_empty(board)
    if not empty:
        return True
    else:
        row, col = empty

    # Loop through numbers 1-9 to see if they work
    for i in range(1, 10):
        if valid_number(board, i, (row, col)):
            board[row][col] = i

            # Recursive check
            if solve(board):
                return True

            board[row][col] = EMPTY

    return False


# Print and run nicely
def main():
    b = get_board()
    print()
    print_board(b)
    print()
    solve(b)
    print_board(b)
    print()


# Run
main()


