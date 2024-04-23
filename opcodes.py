import logging
from functools import partial
from typing import BinaryIO, Any

class Opcodes:
    def __init__(self, chip8):
        self.chip8 = chip8
        self.funcmap = {
            0x0000: partial(self._0ZZZ, chip8),
            0x00e0: partial(self._0ZZ0, chip8),
            0x00ee: partial(self._0ZZE, chip8),
            0x1000: partial(self._1ZZZ, chip8),
        }

    """Instrxns which take into account the leftmost nibbles of the opcode"""
    def _0ZZZ(self, chip8) -> None:
        extracted_op = chip8.opcode & 0xf0ff
        try:
            self.funcmap[extracted_op]()
        except KeyError:
            print("Unknown opcode: {}".format(hex(chip8.opcode)))


    def _4ZZZ(self, chip8) -> None:
        """For instructions that use VX register when it's not equal to NN"""
        if chip8.register_bank[chip8.vx] != (chip8.opcode & 0x00ff):
            chip8.pc += 2


    def _5ZZZ(self, chip8) -> None:
        """For instrxns when VX == Vy register"""
        if chip8.register_bank[chip8.vx] == chip8.register_bank[chip8.vy]:
            chip8.pc += 2


    def _8ZZ4(self, chip8) -> None:
        if chip8.register_bank[chip8.vx] + chip8.register_bank[chip8.vy] > 0xff:
            chip8.register_bank[0xf] = 1
        else:
            chip8.register_bank[0xf] = 0
        chip8.register_bank[chip8.vx] += chip8.register_bank[chip8.vy]
        chip8.register_bank[chip8.vx] &= 0xff 

    def _8ZZ5(self, chip8):
        if chip8.register_bank[chip8.vy] > chip8.register_bank[chip8.vx]:
            chip8.register_bank[0xf] = 0
        else:
            chip8.register_bank[0xf] = 1

        chip8.register_bank[chip8.vx] -= chip8.register_bank[chip8.vy]
        chip8.register_bank[chip8.vx] &= 0xff


    def _0ZZ0(self, chip8) -> None:
        logging.log(logging.INFO, "Clearing Screen")
        chip8.display_buffer = [0] * 64 * 32
        chip8.should_draw = True


    def _0ZZE(self, chip8) -> None:
        logging.log(logging.INFO, "Returning from subroutine")
        chip8.pc = chip8.stack.pop()


    def _1ZZZ(self, chip8) -> None:
        logging.log(logging.INFO, "Jumping addresses")
        chip8.pc = chip8.opcode & 0x0fff


