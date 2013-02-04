'''
Created on Nov 1, 2011

@author: Calvin
'''

from StatementParse import StatementParse
import Constants


class Program(object):
    '''
    Program contains the state of a Bug Language program loaded from text.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self._name = ""
        self._body = StatementParse()
        self._context = dict()

    def set_name(self, name):
        '''
        Sets the name of the program.
        '''
        self._name = name

    def set_body(self, body):
        '''
        Sets the body statement of the program.
        '''
        self._body = body

    def get_name(self):
        '''
        Gets the name of the program.
        '''
        return self._name

    def get_body(self):
        '''
        Gets the body statement of the program.
        '''
        return self._body

    def add_to_context(self, name, statement):
        '''
        Adds an instruction statement to the program context.
        '''
        self._context[name] = statement

    def is_in_context(self, name):
        '''
        Returns whether the instruction name is in the program context.
        '''
        return name in self._context

    def get_context(self):
        '''
        Returns the keys (names) of the instruction in the program context.
        '''
        return self._context.keys()

    def get_from_context(self, name):
        '''
        Returns the instruction statement corresponding to the given name.
        '''
        return self._context[name]

    def context_length(self):
        '''
        Returns the length of the program context.
        '''
        return len(self._context)

    def pretty_print(self):
        '''
        Returns a pretty string version of the program.
        '''
        pretty = "PROGRAM " + self._name + " IS\n\n"

        for instr in self._context:
            pretty += "INSTRUCTION " + instr + " IS\n"
            pretty += self._context[instr].pretty_print(5)
            pretty += "END " + instr + "\n\n"

        pretty += "BEGIN\n" + \
            self._body.pretty_print(5) + \
            "END " + self._name

        return pretty

    def __str__(self):
        '''
        Calls the pretty print method of the program.
        '''
        return self.pretty_print()
