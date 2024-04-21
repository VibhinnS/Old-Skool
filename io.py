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

    def load_rom(self, rom_path) -> None:
        """Loading ROM in the memory as a binary file"""
        logging.log(logging.INFO, "Loading ROM: %s", rom_path)
        binary = open(rom_path, "rb").read()
        i :int = 0
        while i < len(binary):
            self.memory[i + 512] = binary[i]
            i += 1

    def cycle(self):
        self.opcode = self.memory[self.pc]
        self.pc += 2

        if self.delay_timer > 0:
            self.delay_timer -= 1
        if self.sound_timer > 0:
            self.sound_timer -= 1
            if self.sound_timer == 0:
                print("BEEP")
            self.sound_timer -= 1