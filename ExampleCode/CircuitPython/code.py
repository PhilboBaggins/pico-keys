# SPDX-FileCopyrightText: 2021 John Park for Adafruit Industries
# SPDX-License-Identifier: MIT
# RaspberryPi Pico RP2040 Mechanical Keyboard

import time
import board
from digitalio import DigitalInOut, Direction
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from button_checker import ButtonChecker, PRESSED, RELEASED

print("---Pico Pad Keyboard---")

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
led.value = True

kbd = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

# List of pins to use:
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

MEDIA = 1
KEY = 2
FUNC = 3

def loginSequence():
    layout.write('!!!!! USERNAME HERE !!!!!')
    time.sleep(0.1)  # Seconds
    kbd.press(Keycode.TAB)
    time.sleep(0.1)  # Seconds
    layout.write('!!!!! PASSWORD HERE !!!!!')
    time.sleep(0.1)  # Seconds
    kbd.press(Keycode.ENTER)
    # TODO: Do I need the time.sleep calls?

keymap = {
    (0):  (KEY, (Keycode.CONTROL, Keycode.ALT, Keycode.DELETE)),
    (1):  (KEY, (Keycode.CONTROL, Keycode.ALT, Keycode.DELETE)),
    (2):  (MEDIA, ConsumerControlCode.VOLUME_DECREMENT),
    (3):  (MEDIA, ConsumerControlCode.VOLUME_INCREMENT),

    (4):  (FUNC, loginSequence),
    (5):  (KEY, [Keycode.B]),
    (6):  (KEY, [Keycode.C]),
    (7):  (KEY, [Keycode.D]),

    (8):  (KEY, [Keycode.E]),
    (9):  (KEY, [Keycode.F]),
    (10): (KEY, [Keycode.G]),
    (11): (KEY, [Keycode.H]),

    (12): (FUNC, lambda: layout.write('Hello world')),
    (13): (FUNC, lambda: layout.write('Hello world')),
    (14): (FUNC, lambda: layout.write('Hello world')),
    (15): (FUNC, lambda: layout.write('Hello world')),
}

buttonChecker = ButtonChecker(pins)

while True:
    for button, state in buttonChecker.check_all():
        try:
            if state == PRESSED:
                if keymap[button][0] == KEY:
                    kbd.press(*keymap[button][1])
                elif keymap[button][0] == FUNC:
                    keymap[button][1]()
                else:
                    cc.send(keymap[button][1])
            elif state == RELEASED:
                if keymap[button][0] == KEY:
                    kbd.release(*keymap[button][1])
        except ValueError:  # deals with six key limit
            pass

    led.value = not led.value  # TODO: Get LED flashing at a sensible rate... right now it blinks so fast that it just looks constantly on
    time.sleep(0.01)  # debounce
