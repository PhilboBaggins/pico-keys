#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

#include "bsp/board.h"
#include "tusb.h"

#include "pico/stdlib.h"
#include "hardware/uart.h"

#include "usb_descriptors.h"
#include "buttons.h"

//--------------------------------------------------------------------+
// MACRO CONSTANT TYPEDEF PROTYPES
//--------------------------------------------------------------------+

/* Blink pattern
 * - 250 ms  : device not mounted
 * - 1000 ms : device mounted
 * - 2500 ms : device is suspended
 */
enum  {
  BLINK_NOT_MOUNTED = 250,
  BLINK_MOUNTED = 1000,
  BLINK_SUSPENDED = 2500,
};

static uint32_t blink_interval_ms = BLINK_NOT_MOUNTED;

// Map buttons to key codes - These will be send when the button is pressed
uint8_t BUTTON_KEY_MAP[NUM_BUTTONS] = {
    HID_KEY_A, HID_KEY_B, HID_KEY_C,
    HID_KEY_D, HID_KEY_E, HID_KEY_F,
    HID_KEY_G, HID_KEY_H, HID_KEY_I,
    HID_KEY_J, HID_KEY_K, HID_KEY_L,
#if BOAD_MAJOR_VERSION == 1
    HID_KEY_M, HID_KEY_N, HID_KEY_O,
#endif
};

void led_blinking_task(void);
void hid_task(void);
void cdc_task(void);

//--------------------------------------------------------------------+
// Main
//--------------------------------------------------------------------+
int main(void)
{
    board_init();
    tusb_init();
    buttons_init();

    while (true)
    {
        sleep_ms(1000);

        tud_task(); // tinyusb device task
        led_blinking_task();
        hid_task();
    }

    return 0;
}

//--------------------------------------------------------------------+
// Device callbacks
//--------------------------------------------------------------------+

// Invoked when device is mounted
void tud_mount_cb(void)
{
  blink_interval_ms = BLINK_MOUNTED;
}

// Invoked when device is unmounted
void tud_umount_cb(void)
{
  blink_interval_ms = BLINK_NOT_MOUNTED;
}

// Invoked when usb bus is suspended
// remote_wakeup_en : if host allow us  to perform remote wakeup
// Within 7ms, device must draw an average of current less than 2.5 mA from bus
void tud_suspend_cb(bool remote_wakeup_en)
{
  (void) remote_wakeup_en;
  blink_interval_ms = BLINK_SUSPENDED;
}

// Invoked when usb bus is resumed
void tud_resume_cb(void)
{
  blink_interval_ms = BLINK_MOUNTED;
}

//--------------------------------------------------------------------+
// USB HID
//--------------------------------------------------------------------+

#define NUM_SIMULTANEOUS_USB_KEY_CODES 6

bool addKey(uint8_t existingKeycodes[NUM_SIMULTANEOUS_USB_KEY_CODES], uint8_t newKeyCode)
{
    // USB HID allows for 6 keys pressed at one time. So effectively there are 6 slots we could put out key code into
    // Go through each slot, check if it's empty and if so, put our key code in
    for (int idx = 0; idx < NUM_SIMULTANEOUS_USB_KEY_CODES; idx++)
    {
        if (existingKeycodes[idx] == 0)
        {
            existingKeycodes[idx] = newKeyCode;
            return true;
        }
    }

    // All slots full so could not add this new keycode
    return false;
}

// Every 10ms, we will sent 1 report for each HID profile (keyboard, mouse etc ..)
// tud_hid_report_complete_cb() is used to send the next report after previous one is complete
void hid_task(void)
{
    // Poll every 10ms
    const uint32_t interval_ms = 10;
    static uint32_t start_ms = 0;

    if ( board_millis() - start_ms < interval_ms)
        return; // not enough time
    start_ms += interval_ms;

    static uint8_t prevSentKeycodes[6] = { 0 };
    uint8_t keycodes[6] = { 0 };

    // Check each button
    for (int buttonIdx = 0; buttonIdx < NUM_BUTTONS; buttonIdx++)
    {
        enum BUTTON_STATE state = buttonRead(buttonIdx);

        switch (state)
        {
            case BUTTON_NOT_PRESSED:
                break;
            case BUTTON_PRESSED:
                addKey(keycodes, BUTTON_KEY_MAP[buttonIdx]);
                break;
            case BUTTON_HELD_PRESSED:
                addKey(keycodes, BUTTON_KEY_MAP[buttonIdx]);
                break;
            case BUTTON_RELEASED:
                break;
            default:
                break;
        }
    }

    // Check if any new key codes need to be send
    bool newKeysToSend = false;
    for (int idx = 0; idx < NUM_SIMULTANEOUS_USB_KEY_CODES; idx++)
    {
        if (keycodes[idx] != prevSentKeycodes[idx])
        {
            newKeysToSend = true;
            prevSentKeycodes[idx] = keycodes[idx];
        }
    }

    if (newKeysToSend)
    {
        tud_hid_keyboard_report(REPORT_ID_KEYBOARD, 0, keycodes);
    }
}

// Invoked when sent REPORT successfully to host
// Application can use this to send the next report
// Note: For composite reports, report[0] is report ID
void tud_hid_report_complete_cb(uint8_t instance, uint8_t const* report, uint8_t len)
{
  (void) instance;
  (void) len;
}

// Invoked when received GET_REPORT control request
// Application must fill buffer report's content and return its length.
// Return zero will cause the stack to STALL request
uint16_t tud_hid_get_report_cb(uint8_t instance, uint8_t report_id, hid_report_type_t report_type, uint8_t* buffer, uint16_t reqlen)
{
  // TODO not Implemented
  (void) instance;
  (void) report_id;
  (void) report_type;
  (void) buffer;
  (void) reqlen;

  return 0;
}

// Invoked when received SET_REPORT control request or received data on OUT endpoint ( Report ID = 0, Type = 0 )
void tud_hid_set_report_cb(uint8_t instance, uint8_t report_id, hid_report_type_t report_type, uint8_t const* buffer, uint16_t bufsize)
{
  (void) instance;

  if (report_type == HID_REPORT_TYPE_OUTPUT)
  {
    // Set keyboard LED e.g Capslock, Numlock etc...
    if (report_id == REPORT_ID_KEYBOARD)
    {
      // bufsize should be (at least) 1
      if ( bufsize < 1 ) return;

      uint8_t const kbd_leds = buffer[0];

      if (kbd_leds & KEYBOARD_LED_CAPSLOCK)
      {
        // Capslock On: disable blink, turn led on
        blink_interval_ms = 0;
        board_led_write(true);
      }else
      {
        // Caplocks Off: back to normal blink
        board_led_write(false);
        blink_interval_ms = BLINK_MOUNTED;
      }
    }
  }
}

//--------------------------------------------------------------------+
// BLINKING TASK
//--------------------------------------------------------------------+
void led_blinking_task(void)
{
  static uint32_t start_ms = 0;
  static bool led_state = false;

  // blink is disabled
  if (!blink_interval_ms) return;

  // Blink every interval ms
  if ( board_millis() - start_ms < blink_interval_ms) return; // not enough time
  start_ms += blink_interval_ms;

  board_led_write(led_state);
  led_state = 1 - led_state; // toggle
}
