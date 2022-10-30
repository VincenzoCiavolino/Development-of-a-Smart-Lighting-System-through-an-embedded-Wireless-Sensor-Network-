#include "BlinkToRadio.h"
#include "printf.h"
configuration BlinkToRadioAppC
{
}
implementation
{
  
  components MainC, LedsC,PrintfC,SerialStartC;
  components new TimerMilliC() as Timer0;
  components new TimerMilliC() as Timer1;
  components new TimerMilliC() as Timer2;
  components SenseNBuffC ;
  components ActiveMessageC;
  //components new AMReceiverC(AM_BLINKTORADIOMSG);
  components new AMSenderC(AM_BLINKTORADIOMSG);
  components new HamamatsuS10871TsrC() as Light;
  components new SensirionSht11C() as Temperature;
  components new SensirionSht11C() as Humidity;
  components new CircularBufferC(WINDOW_SIZE_MILLIS/TIMER_PERIOD_MILLI) as BufferLight;
  components new CircularBufferC(WINDOW_SIZE_MILLIS/TIMER_PERIOD_MILLI) as BufferTemperature;
  components new CircularBufferC(WINDOW_SIZE_MILLIS/TIMER_PERIOD_MILLI) as BufferHumidity;
  components MeanC as MeanL;
  components MeanC as MeanT;
  components MeanC as MeanH;

  SenseNBuffC.MeanLight -> MeanL;
  SenseNBuffC.MeanTemp -> MeanT;
  SenseNBuffC.MeanHum -> MeanH;
  SenseNBuffC.BufferLight -> BufferLight;
  SenseNBuffC.BufferTemperature -> BufferTemperature;
  SenseNBuffC.BufferHumidity -> BufferHumidity;
  SenseNBuffC -> MainC.Boot;
  SenseNBuffC.Timer0 -> Timer0;
  SenseNBuffC.Timer1 -> Timer1;
  SenseNBuffC.Timer2 -> Timer2;
  SenseNBuffC.AMControl->ActiveMessageC;
  SenseNBuffC.Leds -> LedsC;
  SenseNBuffC.Packet-> AMSenderC;
  SenseNBuffC.AMPacket->AMSenderC;
  SenseNBuffC.AMSend-> AMSenderC;
  SenseNBuffC.AMControl-> ActiveMessageC;
  SenseNBuffC.Light -> Light;
  SenseNBuffC.Temperature -> Temperature.Temperature;
  SenseNBuffC.Humidity -> Humidity.Humidity;


 // SenseNBuffC.Receiver -> AMReceiverC;
}
