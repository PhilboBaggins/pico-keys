# PicoKeys example using RPi Pico C SDK

Example code for use on a PicoKeys board using the Raspberry Pi Pico's C/C++ SDK.

The Pico becomes at USB HID device that sends keyboard key presses when PicoKeys buttons are pressed.

## Building

### Building on Linux

    PICO_SDK_PATH="path/to/pico-sdk"
    mkdir build
    cd build
    #cmake -DCMAKE_BUILD_TYPE=Debug ..
    cmake ..
    make

### Building on Windows with NMake

    set PICO_SDK_PATH="C:/path/to/pico-sdk"
    mkdir build
    cd build
    #cmake -G "NMake Makefiles" -DCMAKE_BUILD_TYPE=Debug  ..
    cmake -G "NMake Makefiles" ..
    nmake
