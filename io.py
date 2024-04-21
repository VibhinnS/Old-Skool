import pyglet

class CPU(pyglet.window.Window):
    def on_key_press(self, symbol, modifiers):
        pass

    def on_key_release(self, symbol, modifiers):
        pass

# 16 button keyboard input
class Input:
    def __init__(self):
        self.key_inputs = [0] * 16

# for a 64x32 display
class Output:
    """The Output class is a 64x32 display buffer, which is a list of 2048 elements. Each element is a pixel, which can be 0 or 1. The display buffer is initialized to all 0s."""
    def __init__(self):
        self.display_buffer = [0] * 64 * 32

