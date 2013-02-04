'''
Created on Nov 2, 2011

@author: Calvin
'''

if __name__ == '__main__':
    from GenerateCode import GenerateCode
    from Tokenizer import Tokenizer
    
    t = Tokenizer()
    prog = GenerateCode()
    fileName = raw_input("Enter File Name: ")
    f = open("../testinputs/" + fileName + ".bl")
    
    prog.parse(f, t)
    
    prog.generate_code("../" + fileName + ".bo")