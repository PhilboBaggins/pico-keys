
#ifndef _BUTTONS_H_
#define _BUTTONS_H_

#include <stdint.h>

// Select your board version (only define one and comment the others out)
//#define BOAD_MAJOR_VERSION 1
#define BOAD_MAJOR_VERSION 2

#if BOAD_MAJOR_VERSION == 1
    #define NUM_BUTTONS 16
#elif BOAD_MAJOR_VERSION == 2
    #define NUM_BUTTONS 12
#else
    #error Invalid board version selected
#endif

extern const int BUTTON_PINS[NUM_BUTTONS];

enum BUTTON_STATE
{
    BUTTON_NOT_PRESSED = 0,
    BUTTON_PRESSED,
    BUTTON_HELD_PRESSED,
    BUTTON_RELEASED,
};

// Function prototypes
void buttons_init();
enum BUTTON_STATE buttonRead(int buttonIdx);

#endif // _BUTTONS_H_
