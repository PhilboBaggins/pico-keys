# PicoKeys example using RPi Pico C SDK

TODO: Add description .... what is this for... where will it be used

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
    #cmake -DCMAKE_BUILD_TYPE=Debug -G "NMake Makefiles" ..
    cmake -G "NMake Makefiles" ..
    nmake
