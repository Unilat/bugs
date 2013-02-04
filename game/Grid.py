'''
Created on Nov 7, 2011

@author: Calvin
'''

from Enum import enum
import sys

WIDTH = 20
HEIGHT = 20

_grid = [[0 for row in range(WIDTH)] for col in range(HEIGHT)]

states = enum("EMPTY", "ENEMY", "FRIEND", "WALL")

def get_pos(pos):
    '''
    Returns empty, wall, or a reference to the bug at the given position.
    '''
    if pos[0] < 0 or pos[1] < 0 or pos[0] > HEIGHT-1 or pos[1] > WIDTH-1:
        return states.WALL
    else:
        return _grid[pos[0]][pos[1]]

def set_pos(pos, bug):
    '''
    Sets the given position in the grid.
    '''
    _grid[pos[0]][pos[1]] = bug;

def display():
    '''
    Test function to display in ASCII the grid and its bugs.
    '''
    disp = ""
    for i in range(HEIGHT):
        disp += " "
        for j in range(WIDTH):
            if _grid[j][i] == states.EMPTY:
                disp += ".."
            else:
                bug = _grid[j][i]
                if bug._direction == 0:
                    disp += "^"
                elif bug._direction == 1:
                    disp += "v"
                elif bug._direction == 2:
                    disp += "<"
                else:
                    disp += ">"
                disp += str(_grid[j][i].team)
        disp += "\n"
    print disp,