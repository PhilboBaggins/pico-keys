
from digitalio import DigitalInOut, Direction, Pull

NO_CHANGE = 0
PRESSED = 1
RELEASED = 2

class ButtonChecker():
    def __init__(self, pins) -> None:
        self.numButtons = len(pins)
        self.button = [0] * self.numButtons
        self.prevState = [0] * self.numButtons
        for i in range(self.numButtons):
            self.button[i] = DigitalInOut(pins[i])
            self.button[i].direction = Direction.INPUT
            self.button[i].pull = Pull.UP


    def check(self, idx):
        if self.prevState[idx] == 0 and not self.button[idx].value:
            self.prevState[idx] = 1
            return PRESSED
        elif self.prevState[idx] == 1 and self.button[idx].value:
            self.prevState[idx] = 0
            return RELEASED
        else:
            return NO_CHANGE


    def check_all(self):
        for idx in range(self.numButtons):
            state = self.check(idx)
            if state != NO_CHANGE:
                yield idx, state
