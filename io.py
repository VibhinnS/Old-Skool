import pyglet
import sys
import logging


class CHIP8(pyglet.window.Window):
    """Pyglet window for CHIP-8 emulator - pyglet does not support threads"""
    def on_key_press(self, symbol, modifiers):
        pass

    def on_key_release(self, symbol, modifiers):
        pass

    memory = [0]*4960 #4096 bytes of memory
    display_buffer = [0]*32*64 #64x32 display buffer
    gpio = [0]*16 #16 8-bit registers
    sound_timer = 0 #sound timer
    delay_timer = 0 #delay timer
    index = 0 #16 bit index register
    pc = 0 #16 bit program counter
    stack = [] #stack pointer

    self.funcmap = {
        0x000: _0ZZZ,
        0x00e0: _0ZZ0,
        0x00ee: _0ZZE,
        0x1000: _1ZZZ,
    }


    def main(self) -> None:
        self.initialize()
        self.load_rom(sys.argv[1])
        self.cycle()
        self.draw()

    def initialize(self) -> None:
        self.clear()
        self.memory = [0]*4096
        self.gpio = [0]*16
        self.display_buffer = [0]*32*64
        self.stack = []
        self.Key_inputs = [0]*16
        self.opcode = 0
        self.index = 0

        self.delay_timer = 0
        self.sound_timer = 0
        self.should_draw = False

        self.pc = 0x200

        i :int = 0
        while i < 80:
            #char-80 fontset for CHIP-8
            self.memory[i] = self.chip8_fontset[i]
            i += 1

    def load_rom(self, ROM_PATH) -> None:
        """Loading ROM in the memory as a binary file"""
        logging.log(logging.INFO, "Loading ROM: %s", rom_path)
        binary = open(ROM_PATH, "rb").read()
        i :int = 0
        while i < len(binary):
            self.memory[i + 512] = binary[i]
            i += 1

    def cycle(self):
        self.opcode = self.memory[self.pc]
        self.pc += 2
        self.vx = (self.opcode & 0x0F00) >> 8
        self.vy = (self.opcode & 0x00F0) >> 4
        self.pc += 2

        extracted_op = self.opcode & 0xf000
        try:
            self.funcmap[extracted_op]()
        except:
            print("Unknown opcode: %s", self.opcode)

        if self.delay_timer > 0:
            self.delay_timer -= 1
        if self.sound_timer > 0:
            self.sound_timer -= 1
            if self.sound_timer == 0:
                print("BEEP")

    #All the OpCodes listed here - 

    def _0ZZZ(self):
        extracted_op = self.opcode & 0xf0ff
        try:
            self.funcmap[extracted_op]()
        except:
            print("Unknown opcode: %s", self.opcode)

    def _0ZZ0(self):
        logging.log("Clearing Screen")
        self.display_buffer = [0]*364*32
        self.should_draw = True

    def _0ZZE(self):
        logging.log("Returning from subroutine")
        self.pc = self.stack.pop()

    def _1ZZZ(self):
        logging.log("Jumping addresses")
        self.pc = self.opcode & 0x0fff

    