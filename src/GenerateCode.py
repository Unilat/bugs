'''
Created on Nov 3, 2011

@author: Calvin
'''

import Constants
import binascii
from ProgramParse import ProgramParse


class GenerateCode(ProgramParse):
    '''
    Static class for generating a Program's object code.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        # Instruction table for storing addresses of instruction definitions
        self._instr_table = dict()

        # Array of hex characters representing our object code
        self._code = []

        super(GenerateCode, self).__init__()

    def _replace_loc(self, index, value):
        '''
        Replaces the index in the list with the provided value.
        '''
        self._code.pop(index)
        self._code.insert(index, value)

    def _get_hex2(self, value):
        '''
        Returns a 2 hex character string of the integer value.
        '''
        hex_str = hex(value)[2:]

        if len(hex_str) < 2:
            hex_str = "0" + hex_str

        return hex_str

    def _get_hex_string(self):
        '''
        Converts the array of hex instructions to a hex string.
        '''
        result = ""
        for i in self._code:
            result += i
        return result

    def _generate_block(self, block):
        '''
        Generates the code for a block of statements.
        '''
        for i in range(0, len(block)):
            stmt = block.get_from_block(i)
            if stmt.kind() == Constants._kinds.IF:
                self._generate_if(stmt)
            elif stmt.kind() == Constants._kinds.IFELSE:
                self._generate_if_else(stmt)
            elif stmt.kind() == Constants._kinds.WHILE:
                self._generate_while(stmt)
            else:
                self._generate_call(stmt)

    def _generate_instruction(self, stmt):
        '''
        Generates the instruction code with a return to previous PC.
        '''

        # First generate the block of statements inside instruction
        self._generate_block(stmt)

        # Then append a return operation
        self._code.append(self._get_hex2(Constants.codes.RETURN))

    def _generate_if(self, stmt):
        '''
        Generates the instruction code for an if statement.
        '''
        test, child = stmt.decompose_if()

        # Encode the jump test
        self._generate_test(test)

        # Insert a spot for the jump addr
        self._code.append("")

        # Remember this spot, it is where the jump to location will be placed
        jump_addr = len(self._code) - 1

        # Generate code for the conditional block
        self._generate_block(child)

        # Go back and set the jump address to the current location
        self._replace_loc(jump_addr, self._get_hex2(len(self._code)))

    def _generate_if_else(self, stmt):
        '''
        Generates the instruction code for an if-else statement.
        '''
        test, ifchild, elsechild = stmt.decompose_if_else()

        # Encode the jump test
        self._generate_test(test)

        # Insert a spot for the jump addr to else
        self._code.append("")

        # Remember this spot, it is where the jump to else will be placed
        jump_to_else = len(self._code) - 1

        # Generate code for the true conditional block
        self._generate_block(ifchild)

        # Next 2 spots for unconditional jump past else block
        self._code.append(self._get_hex2(Constants.codes.JUMP))
        self._code.append("")

        # Remember this spot, it is where the jump past else will be placed
        jump_past_else = len(self._code) - 1

        # Go back and set the else jump address to the current location
        self._replace_loc(jump_to_else, self._get_hex2(len(self._code)))

        # Generate code for the false conditional block
        self._generate_block(elsechild)

        # Go back and set the jump past else address to the current location
        self._replace_loc(jump_past_else, self._get_hex2(len(self._code)))

    def _generate_while(self, stmt):
        '''
        Generates the instruction code for a while statement.
        '''
        # Remember the location of the start of the while
        start = len(self._code)

        test, child = stmt.decompose_while()

        # Encode the jump test
        self._generate_test(test)

        # Insert a spot for the jump addr
        self._code.append("")

        # Remember this spot, it is where the jump to location will be placed
        jump_addr = len(self._code) - 1

        # Generate code for the conditional block
        self._generate_block(child)

        # Insert unconditional jump back to beginning of the while
        self._code.append(self._get_hex2(Constants.codes.JUMP))
        self._code.append(self._get_hex2(start))

        # Go back and set the jump address to the new location counter
        self._replace_loc(jump_addr, self._get_hex2(len(self._code)))

    def _generate_call(self, stmt):
        '''
        Generates the instruction code for a call statement.
        '''
        call = stmt.decompose_call()
        if call in Constants._calls:
            self._code.append(self._get_hex2(
                                Constants.codes.__dict__[call.upper()]))
        else:
            # Encode unconditional jump to where instruction begins
            self._code.append(self._get_hex2(Constants.codes.JUMP_TO_INSTR))
            self._code.append(self._get_hex2(self._instr_table[call]))

    def _generate_test(self, test):
        '''
        Generates the instruction code for the test condition.
        '''
        self._code.append(self._get_hex2(
                            Constants.codes.__dict__["JUMP_IF_NOT_" + \
                            Constants._conditions_text[test].upper().replace("-","_")]))

    def generate_code(self, out):
        '''
        Generates the code of the program
        '''

        # Reserve space for starting execution address
        self._code.append("")

        for name in self.get_context():
            # Location of the instruction is the current location counter
            self._instr_table[name] = len(self._code)

            # Convert the instruction to code

            self._generate_instruction(self.get_from_context(name))

        # Store the current location as starting address.
        self._replace_loc(0, self._get_hex2(len(self._code)))

        # Generate code for body
        self._generate_block(self.get_body())

        # HALT
        self._code.append(self._get_hex2(Constants.codes.HALT))

        f = open(out, "wb")

        print self._code
        print self._instr_table

        f.write(binascii.a2b_hex(self._get_hex_string()))
        f.close()
