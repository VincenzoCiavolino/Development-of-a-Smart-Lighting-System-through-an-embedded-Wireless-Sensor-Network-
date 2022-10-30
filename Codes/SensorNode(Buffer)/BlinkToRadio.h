#ifndef BlinkToRAdio_H
#define BlinkToRAdio_H

enum {
  TIMER_PERIOD_MILLI = 500,
  WINDOW_SIZE_MILLIS=5000,
  AM_BLINKTORADIOMSG=6  
};

typedef nx_struct BlinkToRadioMsg {
  nx_uint16_t nodeid;
  nx_uint16_t Lum;
  nx_uint16_t Temp;
  nx_uint16_t Hum;
} BlinkToRadioMsg;
#endif
