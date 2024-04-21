class Memory(self):
    """CHIP-8 has 4096 bytes of memory, alongwith 16 8-bit registers. The memory is initialized to all 0s.
    The registers are specified as Vx - where x is a hexadecimal digit (0-F)."""
    self.memory = [0]*4096