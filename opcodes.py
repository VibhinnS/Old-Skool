import logging

class Opcodes:
    def __init__(self, chip8):
        self.chip8 = chip8
        self.funcmap = {
            0x0000: self._0ZZZ,
            0x00e0: self._0ZZ0,
            0x00ee: self._0ZZE,
            0x1000: self._1ZZZ,
        }

    def _0ZZZ(self):
        extracted_op = self.chip8.opcode & 0xf0ff
        try:
            self.funcmap[extracted_op]()
        except KeyError:
            print("Unknown opcode: {}".format(hex(self.chip8.opcode)))

    def _0ZZ0(self):
        logging.log(logging.INFO, "Clearing Screen")
        self.chip8.display_buffer = [0] * 64 * 32
        self.chip8.should_draw = True

    def _0ZZE(self):
        logging.log(logging.INFO, "Returning from subroutine")
        self.chip8.pc = self.chip8.stack.pop()

    def _1ZZZ(self):
        logging.log(logging.INFO, "Jumping addresses")
        self.chip8.pc = self.chip8.opcode & 0x0fff
