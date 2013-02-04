'''
Created on Sep 11, 2011

@author: calvin
'''

if __name__ == '__main__':
    
    from Tokenizer import Tokenizer
    
    t = Tokenizer()
    
    types = ("ERROR", "WHITESPACE", "CONDITION", "KEYWORD",
             "IDENTIFIER", "COMMENT")
    
    f = open("../testinputs/program.bl")
    
    token = t.get_next_non_whitespace(f)
    
    while token[0] != '':
        print repr(token[0]) + " : " + types[token[1]]
        token = t.get_next_non_whitespace(f)
        