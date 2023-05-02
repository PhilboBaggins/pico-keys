PicoKeys CircuitPython example program
======================================

Example program for using the PicoKeys board with [CircuitPython](https://circuitpython.org/) 7.x, based on the code from Adafruit's [DIY Pico Mechanical Keyboard with Fritzing and CircuitPython](https://learn.adafruit.com/diy-pico-mechanical-keyboard-with-fritzing-circuitpython/code-the-pico-keyboard) project.

Installation instructions
-------------------------

1. Install CiruitPython version 7.x:
    1. Download CiruitPython for the Raspberry Pi Pico from circuitpython.org](https://circuitpython.org/board/raspberry_pi_pico/)
    2. Start with your Pico unplugged from USB. Hold down the BOOTSEL button, and while continuing to hold it (don't let go!), plug the Pico into USB. Continue to hold the BOOTSEL button until the RPI-RP2 drive appears!
    3. If the drive does not appear, unplug your Pico and go through the above process again.
    4. A lot of people end up using charge-only USB cables and it is very frustrating! So make sure you have a USB cable you know is good for data sync.
    5. Once you see a new disk drive appear called RPI-RP2, drag the adafruit_circuitpython_etc.uf2 file to RPI-RP2.
    6. The RPI-RP2 drive will disappear and a new disk drive called CIRCUITPY will appear.
2. Copy the code.py and lib folder to your CIRCUITPY drive:
    * NOTE: This will replace the current code.py, as well as the lib folder and its contents. Back up any desired code before copying these files!
3. Unplug the RPi Pico from your computer and then plug it back in
   * The CIRCUITPY drive will show up again but you can just close and ignore it now

Copyright and licence info
--------------------------

Copyright © 2021, 2022 Phil Baldwin and John Park for Adafruit Industries

Code licensed under the MIT license (see [LICENSE.txt](LICENSE.txt) or <http://opensource.org/licenses/MIT>).

Code and installation instructions based on [Adafruit example program](https://learn.adafruit.com/diy-pico-mechanical-keyboard-with-fritzing-circuitpython/code-the-pico-keyboard) by John Park.
