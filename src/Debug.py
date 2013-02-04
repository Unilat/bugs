'''
Created on Oct 30, 2011

@author: Calvin
'''

'''
Determines whether debug information should be displayed.
'''
ON = True


def debug(message, newline=True):

    '''
    Prints a debug message to the console if debug mode is enabled.
    '''
    if ON:
        print message,
        if newline:
            print "\n",
