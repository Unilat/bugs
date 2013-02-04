'''
Created on Sep 21, 2011

@author: calvin
'''

if __name__ == '__main__':
    from StatementParse import StatementParse
    from Tokenizer import Tokenizer
    
    t = Tokenizer()
    stmt = StatementParse()
    f = open("../testinputs/statement.bl")
    
    ttext, ttype = t.get_next_non_whitespace(f)
    
    stmt.parse(f, t, ttext, ttype)
    
    print "\n\n" + str(stmt)