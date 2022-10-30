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
  components BlinkToRadioC ;
  components ActiveMessageC;
  //components new AMReceiverC(AM_BLINKTORADIOMSG);
  components new AMSenderC(AM_BLINKTORADIOMSG);
  components new HamamatsuS10871TsrC() as Light;
  components new SensirionSht11C() as Temperature;
  components new SensirionSht11C() as Humidity;

  BlinkToRadioC -> MainC.Boot;
  BlinkToRadioC.Timer0 -> Timer0;
  BlinkToRadioC.Timer1 -> Timer1;
  BlinkToRadioC.AMControl->ActiveMessageC;
  BlinkToRadioC.Leds -> LedsC;
  BlinkToRadioC.Packet-> AMSenderC;
  BlinkToRadioC.AMPacket->AMSenderC;
  BlinkToRadioC.AMSend-> AMSenderC;
  BlinkToRadioC.AMControl-> ActiveMessageC;
  BlinkToRadioC.Light -> Light;
  BlinkToRadioC.Temperature -> Temperature.Temperature;
  BlinkToRadioC.Humidity -> Humidity.Humidity;
 // BlinkToRadioC.Receiver -> AMReceiverC;
}
