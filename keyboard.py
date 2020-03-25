import sys
import threading

try:
    from getkey import getkey
except ImportError:
    getkey = None


KEYBOARD_ENABLED = getkey is not None


class BaseKeyboard:
    def read_character(self):
        return ord(sys.stdin.read(1))


class Keyboard(BaseKeyboard, threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.buffer = []
        self.daemon = True

    def read_character(self):
        if self.buffer:
            return self.buffer.pop(0)
        return 0

    def run(self):
        while True:
            char = getkey()

            try:
                self.buffer.append(ord(char))
            except TypeError:
                pass
