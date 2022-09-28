
# Select your board version (only define one and comment the others out)
#BOAD_VERSION = '1.x'
BOAD_VERSION = '2.x'

import board

if BOAD_VERSION == '1.x':
    # List of pins to use for PCB v1.x
    pins = [
        board.GP0,
        board.GP1,
        board.GP2,
        board.GP3,
        board.GP4,
        board.GP5,
        board.GP6,
        board.GP7,
        board.GP8,
        board.GP9,
        board.GP10,
        board.GP11,
        board.GP12,
        board.GP13,
        board.GP14,
        board.GP15,  # TODO: Perhaps I shouldn't have used this one because the Adaffruit USB keyboard example code said GPIO15 was "funky" on the RPi Pico
    ]
elif BOAD_VERSION == '2.x':
    # List of pins to use for PCB v2.x
    pins = [
        board.GP27,
        board.GP28,
        board.GP5,
        board.GP21,
        board.GP20,
        board.GP11,
        board.GP18,
        board.GP16,
        board.GP13,
        board.GP17,
        board.GP15,  # TODO: Perhaps I shouldn't have used this one because the Adaffruit USB keyboard example code said GPIO15 was "funky" on the RPi Pico
        board.GP14,
    ]
else:
    # TODO: What to do here? Can I warn the user somehow???
    pass
