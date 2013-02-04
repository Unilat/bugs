'''
Created on Sep 15, 2011

@author: calvin
'''

from Tree import Tree
import Constants


class StatementLabel(object):
    '''
    Stores the test, kind, and instruction of the root of the statement.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.test = Constants._conditions_text.index("true")
        self.kind = Constants._kinds.BLOCK
        self.instruction = ""

    def __str__(self):
        '''
        Returns a nice formatted string representation of the statement label.
        '''
        return "{" + str(self.kind) + "," + \
            Constants._conditions_text[self.test] + \
            ",'" + self.instruction + "'}"


class Statement(object):
    '''
    Represents the state of a Bug language statement.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self._treeRep = Tree(StatementLabel())

    def _current(self):
        '''
        Returns the statement label at the root of the statement tree.
        '''
        return self._treeRep.get_root()

    def add_to_block(self, pos, statement):
        '''
        Adds a statement to the block.
        '''
        self._treeRep.add(pos, statement)

    def get_from_block(self, pos):
        '''
        Returns the statement at pos from the block.
        '''
        return self._treeRep.child_at(pos)

    def __len__(self):
        '''
        Returns the length of the block.
        '''
        return self._treeRep.num_children()

    def kind(self):
        '''
        Returns the statement kind.
        '''
        return self._current().kind

    def compose_if(self, condition, block):
        '''
        Composes an if statement with condition and block.
        '''
        self._current().kind = Constants._kinds.IF
        self._current().test = condition
        self._treeRep.add(0, block)

    def decompose_if(self):
        '''
        Returns a tuple of the if statement test and block.
        '''
        return (self._current().test, self._treeRep.child_at(0))

    def compose_if_else(self, condition, if_block, else_block):
        '''
        Composes an if else statement with condition and true/false blocks.
        '''
        self._current().kind = Constants._kinds.IFELSE
        self._current().test = condition
        self._treeRep.add(0, if_block)
        self._treeRep.add(1, else_block)

    def decompose_if_else(self):
        '''
        Returns a tuple of the if else statement's test and true/false blocks.
        '''
        return (self._current().test, self._treeRep.child_at(0),
                self._treeRep.child_at(1))

    def compose_while(self, condition, block):
        '''
        Composes a while statement with condition and block.
        '''
        self._current().kind = Constants._kinds.WHILE
        self._current().test = condition
        self._treeRep.add(0, block)

    def decompose_while(self):
        '''
        Returns a tuple of the while statement test and block.
        '''
        return (self._current().test, self._treeRep.child_at(0))

    def compose_call(self, instr):
        '''
        Composes a call instruction.
        '''
        self._current().kind = Constants._kinds.CALL
        self._current().instruction = instr

    def decompose_call(self):
        '''
        Returns the text of the call.
        '''
        return self._current().instruction

    def pretty_print(self, indent):
        '''
        Returns a pretty string version of the statement.
        '''
        pretty = ""

        if self.kind() == Constants._kinds.IF:
            pretty = " " * indent
            pretty += "IF " + \
                Constants._conditions_text[self._current().test] + \
                " THEN\n" + self._treeRep.child_at(0).pretty_print(indent + 5)
            pretty += " " * indent + "END IF"
        elif self.kind() == Constants._kinds.IFELSE:
            pretty = " " * indent
            pretty += "IF " + \
                Constants._conditions_text[self._current().test] + \
                " THEN\n" + self._treeRep.child_at(0).pretty_print(indent + 5)
            pretty += "ELSE\n" + " " * indent + \
                self._treeRep.child_at(1).pretty_print(indent + 5)
            pretty += " " * indent + "END IF"
        elif self.kind() == Constants._kinds.WHILE:
            pretty = " " * indent
            pretty += "WHILE " + \
                Constants._conditions_text[self._current().test] + \
                " DO\n" + self._treeRep.child_at(0).pretty_print(indent + 5)
            pretty += " " * indent + "END WHILE"
        elif self.kind() == Constants._kinds.BLOCK:
            for i in range(0, self._treeRep.num_children()):
                pretty += self._treeRep.child_at(i).pretty_print(indent) + "\n"
        else: # IDENTIFIER
            pretty = " " * indent
            pretty += self._current().instruction

        return pretty

    def __str__(self):
        '''
        Calls the pretty_print method of the statement.
        '''
        return self.pretty_print(0)
