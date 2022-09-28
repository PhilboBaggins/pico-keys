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
from pin_map import pins

print("---Pico Keys---")

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
led.value = True
LED_BLINK_INTERVAL = 0.5
ledBlinkTime = time.monotonic() + LED_BLINK_INTERVAL

kbd = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

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

    # Mot available on v2.x boards (keymap below will be ignored)
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

    now = time.monotonic()
    if now > ledBlinkTime:
        ledBlinkTime = now + LED_BLINK_INTERVAL
        led.value = not led.value

    time.sleep(0.01)  # debounce
