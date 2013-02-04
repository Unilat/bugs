'''
Created on Nov 1, 2011

@author: Calvin
'''

from Enum import enum

_conditions_text = ["next-is-empty", "next-is-not-empty",
           "next-is-enemy", "next-is-not-enemy",
           "next-is-friend", "next-is-not-friend",
           "next-is-wall", "next-is-not-wall",
           "random", "true"]
_kinds = enum("WHILE", "IF", "IFELSE", "CALL", "BLOCK")
_types = enum("ERROR", "WHITESPACE", "CONDITION", "KEYWORD",
              "IDENTIFIER", "COMMENT")
_calls = ["infect", "move", "skip", "turnright", "turnleft"]

codes = enum("MOVE", "TURNLEFT", "TURNRIGHT", "INFECT",
                "SKIP", "HALT", "JUMP", "JUMP_IF_NOT_NEXT_IS_EMPTY",
                "JUMP_IF_NOT_NEXT_IS_NOT_EMPTY", "JUMP_IF_NOT_NEXT_IS_ENEMY",
                "JUMP_IF_NOT_NEXT_IS_NOT_ENEMY", "JUMP_IF_NOT_NEXT_IS_FRIEND",
                "JUMP_IF_NOT_NEXT_IS_NOT_FRIEND", "JUMP_IF_NOT_NEXT_IS_WALL",
                "JUMP_IF_NOT_NEXT_IS_NOT_WALL", "JUMP_IF_NOT_RANDOM",
                "JUMP_IF_NOT_TRUE", "RETURN", "JUMP_TO_INSTR")
