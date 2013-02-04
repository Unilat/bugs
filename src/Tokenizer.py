'''
Created on Sep 9, 2011

@author: calvin
'''

from Enum import enum


class Tokenizer(object):
    '''
    Tokenizes text from an input stream into Bug language token types.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self._keywords = ["BEGIN", "DO", "ELSE", "END", "INSTRUCTION",
                     "IF", "IS", "PROGRAM", "THEN", "WHILE"]
        self._conditions = ["next-is-empty", "next-is-not-empty",
                     "next-is-enemy", "next-is-not-enemy",
                     "next-is-friend", "next-is-not-friend",
                     "next-is-wall", "next-is-not-wall",
                     "random", "true"]
        self._states = enum("EMPTY", "ERROR", "WHITESPACE", "COND_KEY_ID",
                            "COMMENT")
        self._types = enum("ERROR", "WHITESPACE", "CONDITION", "KEYWORD",
                           "IDENTIFIER", "COMMENT")
        self._buffer = ""
        self._bufferState = self._states.EMPTY
        self._readyToDispense = 0

    def _buffer_type(self, char):
        '''
        Returns an buffer type based on the initial character
        '''
        if char == '#':
            return self._states.COMMENT
        elif str(char).isspace():
            return self._states.WHITESPACE
        elif str(char).isalpha():
            return self._states.COND_KEY_ID
        else:
            return self._states.ERROR

    def _token_type(self, token):
        '''
        Returns the enumeration of the token type stored in the buffer
        '''
        if self._bufferState == self._states.COMMENT:
            return self._types.COMMENT

        elif self._bufferState == self._states.ERROR:
            return self._types.ERROR

        elif self._bufferState == self._states.WHITESPACE:
            return self._types.WHITESPACE

        else:
            if token in self._keywords:
                return self._types.KEYWORD
            elif token in self._conditions:
                return self._types.CONDITION
            else:
                return self._types.IDENTIFIER

    def insert(self, char):
        '''
        Inserts a character and indicates when a complete token is dispensable
        '''
        if self._bufferState == self._states.EMPTY:
            # Transition to whatever state is indicated by the char
            self._bufferState = self._buffer_type(char)

        elif self._bufferState == self._states.COMMENT:
            # If we're not at a newline just add to the buffer
            if char == '\n':
                self._readyToDispense = 1

        elif self._bufferState == self._states.ERROR:
            # If we already have an error token and we find a non error,
            # we are ready to dispense
            if self._buffer_type(char) != self._states.ERROR:
                self._readyToDispense = 1

        elif self._bufferState == self._states.WHITESPACE:
            # Ready to dispense if new char is not whitespace
            if not str(char).isspace():
                self._readyToDispense = 1

        else: # self._bufferState == self._states.COND_KEY_ID:
            # If we have a cond, key, or id and encounter a comment,
            # whitespace or error, we are ready to dispense
            if not(str(char).isalnum() or char == '-'):
                self._readyToDispense = 1

        # In each case if we still add the current char to the buffer
        self._buffer += char

    def dispense(self):
        '''
        Returns a tuple (Token Text, Token Type)
        '''
        result = (self._buffer[:-1], self._token_type(self._buffer[:-1]))
        self._buffer = self._buffer[-1]
        self._bufferState = self._buffer_type(self._buffer)
        self._readyToDispense = 0

        return result

    def dump(self):
        '''
        Returns a tuple (Token Text, Token Type) of whatever is in the buffer
        '''
        result = (self._buffer, self._token_type(self._buffer))
        self._buffer = ''
        self._bufferState = self._states.EMPTY
        self._readyToDispense = 0

        return result

    def get_next_token(self, f):
        '''
        Reads from file f and returns the next complete token
        '''
        char = f.read(1)
        while char != '':
            self.insert(char)
            if not self.is_ready_to_dispense():
                char = f.read(1)
            else:
                return self.dispense()
        return self.dump()

    def get_next_non_whitespace(self, f):
        '''
        Reads from file f and returns the next complete non whitespace token
        '''
        tt = self.get_next_token(f)
        while tt[1] == self._types.WHITESPACE or tt[1] == self._types.COMMENT:
            tt = self.get_next_token(f)
        return tt

    def is_ready_to_dispense(self):
        '''
        Returns 1 or 0 whether the Tokenizer has a complete token to dispense
        '''
        return self._readyToDispense

    def __len__(self):
        '''
        Returns the current size of the token in the buffer
        '''
        return len(self._buffer)
