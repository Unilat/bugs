'''
Created on Nov 1, 2011

@author: Calvin
'''

import Constants
from Debug import debug
from StatementParse import StatementParse
from Program import Program


class ProgramParse(Program):
    '''
    Adds Parse capabilities as an extension to Program
    '''

    def __init__(self):
        '''
        Constructor
        '''
        super(ProgramParse, self).__init__()

    def parse(self, instream, tokenizer):
        '''
        Parse the text from the instream into a Program object
        '''

        # Expect PROGRAM
        ttext, ttype = tokenizer.get_next_non_whitespace(instream)
        if ttype == Constants._types.KEYWORD and ttext == "PROGRAM":
            debug("PROGRAM", False)
        else:
            exit("Expected PROGRAM to begin the program (But was:" + \
                 ttext + ")")

        # Expect program name
        progname, ttype = tokenizer.get_next_non_whitespace(instream)
        if ttype == Constants._types.IDENTIFIER:
            debug(progname, False)
        else:
            exit("Expected identifier program name after PROGRAM (But was:" + \
                 progname + ")")

        self.set_name(progname)

        # Expect IS
        ttext, ttype = tokenizer.get_next_non_whitespace(instream)
        if ttype == Constants._types.KEYWORD and ttext == "IS":
            debug("IS")
        else:
            exit("Expected IS after program name (But was:" + ttext + ")")

        ttext, ttype = tokenizer.get_next_non_whitespace(instream)

        # Loop as long as we continue seeing instructions
        while (ttype == Constants._types.KEYWORD and ttext == "INSTRUCTION"):

            debug(ttext, False)

            # Expect instruction name
            name, ttype = tokenizer.get_next_non_whitespace(instream)
            if ttype == Constants._types.IDENTIFIER:
                debug(name, False)
            else:
                exit("Expected identifier instruction name after " + \
                     "INSTRUCTION (But was:" + name + ")")

            # Expect IS
            ttext, ttype = tokenizer.get_next_non_whitespace(instream)
            if ttype == Constants._types.KEYWORD and ttext == "IS":
                debug(ttext)
            else:
                exit("Expected IS after instruction name (But was" + \
                     ttext + ")")

            # Parse the statement block making up the instruction
            ttext, ttype = tokenizer.get_next_non_whitespace(instream)
            instr = StatementParse()
            ttext, ttype = instr.parse_block(instream, tokenizer, ttext, ttype)
            self.add_to_context(name, instr)

            # Verify we had an END to the instruction
            if ttype == Constants._types.KEYWORD and ttext == "END":
                debug("END", False)
            else:
                exit("Expected END to complete the instruction (But was:" + \
                     ttext + ")")

            # Verify matching instruction name after END
            ttext, ttype = tokenizer.get_next_non_whitespace(instream)
            if ttype == Constants._types.IDENTIFIER and ttext == name:
                debug(ttext)
            else:
                exit("Expected matching instruction name ('" + name + \
                     "') after END (But was:" + ttext + ")")

            ttext, ttype = tokenizer.get_next_non_whitespace(instream)

        # Next token should be BEGIN
        if ttype == Constants._types.KEYWORD and ttext == "BEGIN":
            debug(ttext)
        else:
            exit("Expected BEGIN to initialize the beginning of the " + \
                 "program (But was:" + ttext + ")")

        # Parse the statement block making up the body
        ttext, ttype = tokenizer.get_next_non_whitespace(instream)
        instr = StatementParse()
        ttext, ttype = instr.parse_block(instream, tokenizer, ttext, ttype)
        self.set_body(instr)

        # Verify we had an END to the body
        if ttype == Constants._types.KEYWORD and ttext == "END":
            debug(ttext, False)
        else:
            exit("Expected END to complete the body (But was:" + ttext + ")")

        # Verify matching program name after END
        ttext, ttype = tokenizer.get_next_non_whitespace(instream)
        if ttype == Constants._types.IDENTIFIER and ttext == progname:
            debug(ttext)
        else:
            exit("Expected matching instruction name ('" + progname + \
                 "') after END (But was:" + ttext + ")")
