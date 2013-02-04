'''
Created on Nov 2, 2011

@author: Calvin
'''

if __name__ == '__main__':
    from ProgramParse import ProgramParse
    from Tokenizer import Tokenizer
    
    t = Tokenizer()
    prog = ProgramParse()
    f = open("../testinputs/program.bl")
    
    prog.parse(f, t)
    
    print "\n\n" + str(prog)