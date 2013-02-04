'''
Created on Nov 4, 2011

@author: Calvin
'''

import Constants
from random import randint
from Enum import enum
from Debug import debug
import Grid

_facing = enum("UP", "DOWN", "LEFT", "RIGHT")

class Bug(object):
    '''
    Represents one Bug game object with PC and stack for code execution.
    '''

    def __init__(self, pos, facing, team):
        '''
        Constructor takes a starting pc and a reference to code array.
        '''
        self.team = team
        self._pc = team.bugCode[0]
        self._code = team.bugCode
        self._stack = []
        self._pos = pos
        self._direction = facing
        
        # Indicate where we've placed the bug is taken
        Grid.set_pos(pos, self)

    def execute(self):

        # Jump conditions don't increment PC
        if self._code[self._pc] >= Constants.codes.JUMP:
            if self._code[self._pc] == Constants.codes.JUMP:
                self._pc = self._code[self._pc + 1]
                debug("JUMP TO " + str(self._pc))
            elif self._code[self._pc] == Constants.codes.JUMP_TO_INSTR:
                # Push PC on to stack (after the jump and jump addr)
                self._stack.append(self._pc + 2)
                
                self._pc = self._code[self._pc + 1]
                debug("JUMP TO INSTR " + str(self._pc))
            elif self._code[self._pc] == Constants.codes.RETURN:
                # pop off PC from the stack and return to it
                self._pc = self._stack.pop()
                debug("RETURN");
            else: # We must evaluate the conditional
                debug("COND " + str(self._code[self._pc]) + " IS " + ("TRUE" if self._check_cond(self._code[self._pc]) else "FALSE"))
                if self._check_cond(self._code[self._pc]):
                    self._pc = self._code[self._pc + 1]
                    debug(self._code[self._pc])
                else:
                    self._pc += 2;
                    debug(self._code[self._pc])
                
        else:
            if self._code[self._pc] == Constants.codes.MOVE:
                self._move()
            elif self._code[self._pc] == Constants.codes.INFECT:
                self._infect()
            elif self._code[self._pc] == Constants.codes.TURNLEFT:
                self._turnleft()
            elif self._code[self._pc] == Constants.codes.TURNRIGHT:
                self._turnright()
            elif self._code[self._pc] == Constants.codes.SKIP:
                debug("SKIP");
            else: # HALT
                return False

            self._pc += 1
        
        return True

    def _one_ahead(self):
        x, y = self._pos

        if self._direction == _facing.LEFT:
            x -= 1
        elif self._direction == _facing.RIGHT:
            x += 1
        elif self._direction == _facing.UP:
            y -= 1
        else:
            y += 1

        return x, y
    
    def _next_is_bug(self):
        nxt =  Grid.get_pos(self._one_ahead())
        
        if nxt != Grid.states.EMPTY and \
            nxt != Grid.states.WALL:
            return nxt
        else:
            # the next position is either a wall or empty
            return 0

    def _check_cond(self, test):

        what_is_next =  Grid.get_pos(self._one_ahead())
        next_bug = self._next_is_bug()

        if test == Constants.codes.JUMP_IF_NOT_NEXT_IS_EMPTY and \
            what_is_next != Grid.states.EMPTY:
            return True
        elif test == Constants.codes.JUMP_IF_NOT_NEXT_IS_NOT_EMPTY and \
            what_is_next == Grid.states.EMPTY:
            return True
        elif test == Constants.codes.JUMP_IF_NOT_NEXT_IS_ENEMY and \
            (not next_bug or next_bug.team.id == self.team.id):
            return True
        elif test == Constants.codes.JUMP_IF_NOT_NEXT_IS_NOT_ENEMY and \
            (next_bug and next_bug.team.id != self.team.id):
            return True
        elif test == Constants.codes.JUMP_IF_NOT_NEXT_IS_FRIEND and \
            (not next_bug or next_bug.team.id != self.team.id):
            return True
        elif test == Constants.codes.JUMP_IF_NOT_NEXT_IS_NOT_FRIEND and \
            (next_bug and next_bug.team.id == self.team.id):
            return True
        elif test == Constants.codes.JUMP_IF_NOT_NEXT_IS_WALL and \
            what_is_next != Grid.states.WALL:
            return True
        elif test == Constants.codes.JUMP_IF_NOT_NEXT_IS_NOT_WALL and \
            what_is_next == Grid.states.WALL:
            return True
        elif test == Constants.codes.JUMP_IF_NOT_RANDOM and \
            randint(0, 1):
            return True
        else: # JUMP IF NOT TRUE
            return False

    def _move(self):
        debug("MOVE");
        pos = self._one_ahead();
        
        if Grid.get_pos(pos) == Grid.states.EMPTY:
            # Set where we were to empty
            Grid.set_pos(self._pos, Grid.states.EMPTY)
            # Set new position to filled
            self._pos = pos
            Grid.set_pos(pos, self)
            

    def _infect(self):
        debug("INFECT");
        next_bug = self._next_is_bug()
        
        if next_bug and next_bug.team.id != self.team.id:
            next_bug.team.dec()
            next_bug.change_team(self)
            self.team.inc()

    def _turnleft(self):
        debug("TURNLEFT");
        if self._direction == _facing.LEFT:
            self._direction = _facing.DOWN
        elif self._direction == _facing.RIGHT:
            self._direction = _facing.UP
        elif self._direction == _facing.UP:
            self._direction = _facing.LEFT
        else:
            self._direction = _facing.RIGHT

    def _turnright(self):
        debug("TURNRIGHT");
        if self._direction == _facing.LEFT:
            self._direction = _facing.UP
        elif self._direction == _facing.RIGHT:
            self._direction = _facing.DOWN
        elif self._direction == _facing.UP:
            self._direction = _facing.RIGHT
        else:
            self._direction = _facing.LEFT
            
    def change_team(self, bug):
        self._code = bug._code
        self._pc = self._code[0]
        self.team = bug.team
