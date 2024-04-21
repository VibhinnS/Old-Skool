class Memory(self):
    """CHIP-8 has 4096 bytes of memory, alongwith 16 8-bit registers. The memory is initialized to all 0s.
    The registers are specified as Vx - where x is a hexadecimal digit (0-F)."""
    self.memory = [0]*4096
    self.gpio = [0]*16

    #Two timer registers - delay and sound. Cause delays by decrementing to 0 for each operation.
    self.sound_timer = 0
    self.delay_timer = 0

    #16 bit index register
    self.index = 0

    #16 bit program counter
    self.pc = 0

    #Stack pointer - stack holds 16 elements at any time
    self.stack = []

    