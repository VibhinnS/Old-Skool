#for a 64x32 display
class Output(self):
"""The Output class is a 64x32 display buffer, which is a list of 2048 elements. Each element is a pixel, which can be 0 or 1. The display buffer is initialized to all 0s."""
    self.display_buffer = [0]*32*64