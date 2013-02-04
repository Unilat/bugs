'''
Created on Sep 8, 2011

@author: calvin
'''


class Tree(object):
    '''
    Tree
    '''

    def __init__(self, root):
        '''
        Constructor
        '''
        self._root = root
        self._array = []

    def add(self, pos, child):
        '''
        Add a tree as a child of the root at position
        '''
        self._array.insert(pos, child)

    def remove(self, pos):
        '''
        Removes and returns a child tree at position
        '''
        return self._array.pop(pos)

    def child_at(self, pos):
        '''
        Returns the child subtree at the given position
        '''
        return self._array[pos]

    def num_children(self):
        '''
        Returns the number of children subtrees
        '''
        return len(self._array)

    def set_root(self, root):
        '''
        Sets the value of the root item in the tree
        '''
        self._root = root

    def get_root(self):
        '''
        Gets the value of the root item in the tree
        '''
        return self._root

    def __len__(self):
        '''
        Returns the length of the entire tree
        '''
        length = 0
        for child in self._array:
            length += len(child)

        return 1 + length

    def __str__(self):
        '''
        Returns a string representation of the tree
        '''
        string = str(self._root) + '('
        for child in self._array:
            string += str(child)
        string += ')'
        return string
