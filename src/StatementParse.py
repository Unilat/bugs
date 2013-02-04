'''
Created on Nov 1, 2011

@author: Calvin
'''

import Constants
from Debug import debug
from Statement import Statement


class StatementParse(Statement):
    '''
    Extends Statement with parsing capabilities.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        super(StatementParse, self).__init__()

    def _parse_if(self, instream, tokenizer, ttext, ttype):
        '''
        Parse an if statement from the instream.
        '''

        # We expect a condition to follow
        condition, ttype = tokenizer.get_next_non_whitespace(instream)
        if ttype == Constants._types.CONDITION:
            debug(condition, False)
        else:
            exit("Expected a condition after IF")

        # THEN comes next
        ttext, ttype = tokenizer.get_next_non_whitespace(instream)
        debug(ttext)
        if ttype != Constants._types.KEYWORD or ttext != "THEN":
            exit("Expected THEN after IF condition")

        # Parse the conditional block
        ttext, ttype = tokenizer.get_next_non_whitespace(instream)
        stmt = StatementParse()
        ttext, ttype = stmt.parse_block(instream, tokenizer, ttext, ttype)

        # Check to see if this is an IF ELSE statement
        if ttype == Constants._types.KEYWORD and ttext == "ELSE":
            debug("ELSE", False)
            # Parse the conditional block
            ttext, ttype = tokenizer.get_next_non_whitespace(instream)
            elsestmt = StatementParse()
            ttext, ttype = elsestmt.parse_block(instream, tokenizer,
                                                ttext, ttype)
            # Compose the IF ELSE
            self.compose_if_else(Constants._conditions_text.index(condition),
                                 stmt, elsestmt)
        else:
            # Compose the IF
            self.compose_if(Constants._conditions_text.index(condition), stmt)

        # Returned token should be END
        if ttype == Constants._types.KEYWORD and ttext == "END":
            debug("END", False)
        else:
            exit("Expected END to complete the IF statement (But was '" + \
                 ttext + "')")


        # END followed by IF
        ttext, ttype = tokenizer.get_next_non_whitespace(instream)
        if ttype != Constants._types.KEYWORD or ttext != "IF":
            exit("Expected IF after END to complete the IF statement " + \
                 "(But was '" + ttext + "')")
        else:
            debug("IF")

    def _parse_while(self, instream, tokenizer, ttext, ttype):
        '''
        Parse a while statement from the instream.
        '''

        # We expect a condition to follow
        condition, ttype = tokenizer.get_next_non_whitespace(instream)
        if ttype == Constants._types.CONDITION:
            debug(condition, False)
        else:
            exit("Expected a condition after WHILE")

        # DO comes next
        ttext, ttype = tokenizer.get_next_non_whitespace(instream)
        debug(ttext)
        if ttype != Constants._types.KEYWORD or ttext != "DO":
            exit("Expected DO after WHILE condition")

        # Parse the conditional block
        ttext, ttype = tokenizer.get_next_non_whitespace(instream)
        stmt = StatementParse()
        ttext, ttype = stmt.parse_block(instream, tokenizer, ttext, ttype)

        # Returned token should be END
        if ttype != Constants._types.KEYWORD or ttext != "END":
            exit("Expected END to complete the WHILE statement (But was '" + \
                 ttext + "')")
        else:
            debug("END", False)

        # END is followed by WHILE
        ttext, ttype = tokenizer.get_next_non_whitespace(instream)
        if ttype != Constants._types.KEYWORD or ttext != "WHILE":
            exit("Expected WHILE after END to complete the WHILE statement" + \
                 " (But was '" + ttext + "')")
        else:
            debug("WHILE")

        # Compose the IF
        self.compose_while(Constants._conditions_text.index(condition), stmt)

    def _parse_call(self, ttext):
        '''
        Parse a call from the token text.
        '''

        debug(ttext)
        # Compose the call
        self.compose_call(ttext)

    def parse(self, instream, tokenizer, ttext, ttype):
        '''
        Parses text from the in stream and returns the next token
        '''
        if ttype == Constants._types.KEYWORD and ttext == "IF":
            debug("IF", False)
            self._parse_if(instream, tokenizer, ttext, ttype)
        elif ttype == Constants._types.KEYWORD and ttext == "WHILE":
            debug("WHILE", False)
            self._parse_while(instream, tokenizer, ttext, ttype)
        elif ttype == Constants._types.IDENTIFIER:
            self._parse_call(ttext)
        else:
            # Not an expected keyword that starts a statement
            exit("Found " + ttext + ", expected keyword")

        # Get the next token to return
        return tokenizer.get_next_non_whitespace(instream)

    def parse_block(self, instream, tokenizer, ttext, ttype):
        '''
        Parses a block of statements from instream returning next token
        '''

        while ttext != "END" and ttext != "ELSE":
            stmt = StatementParse()
            ttext, ttype = stmt.parse(instream, tokenizer, ttext, ttype)
            self.add_to_block(len(self), stmt)

        return ttext, ttype
