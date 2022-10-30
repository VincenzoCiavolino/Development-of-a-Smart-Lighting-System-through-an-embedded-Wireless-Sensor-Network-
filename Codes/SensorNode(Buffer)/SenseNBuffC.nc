// $Id: BlinkC.nc,v 1.6 2010-06-29 22:07:16 scipio Exp $

#include <Timer.h>
#include "printf.h"
#include "BlinkToRadio.h"

module SenseNBuffC 
{
  uses interface Timer<TMilli> as Timer0;
  uses interface Timer<TMilli> as Timer1;
  uses interface Timer<TMilli> as Timer2;
  uses interface Leds;
  uses interface Boot;
  uses interface Packet;
  uses interface AMPacket;
  uses interface AMSend;
  uses interface SplitControl as AMControl;
  uses interface Read<uint16_t> as Light;
  uses interface Read<uint16_t> as Temperature;
  uses interface Read<uint16_t> as Humidity;
  uses interface CircularBuffer as BufferLight;
  uses interface CircularBuffer as BufferTemperature;
  uses interface CircularBuffer as BufferHumidity;
  uses interface ProcessingF as MeanLight;
  uses interface ProcessingF as MeanTemp;
  uses interface ProcessingF as MeanHum;

}

implementation
{

  bool busy = FALSE;
  message_t pkt;
 
 

  event void Boot.booted()
  {
   call AMControl.start();  
  }

  event void Timer0.fired()
  {   	
	call Light.read();
	call Temperature.read();
	call Humidity.read();
}

event void Light.readDone(error_t result, uint16_t data){
		if(result!=SUCCESS)
			data = 0xffff;			
		else {
			call BufferLight.putElem((int16_t)data);
			}	
	}

event void Temperature.readDone(error_t result, uint16_t data) {
 		if (result != SUCCESS) 
			data = 0xffff;			
		else {
			call BufferTemperature.putElem((int16_t)data);
		}		
  	}

	event void Humidity.readDone(error_t result, uint16_t data) {	
		if (result != SUCCESS) 
			data = 0xffff;
		else {
			call BufferHumidity.putElem((int16_t) data);
		}
	}




 event void Timer2.fired()
  {   
        int16_t *bufferLight = (int16_t *)call BufferLight.getWindow();
        int16_t *bufferTemperature = (int16_t *)call BufferTemperature.getWindow();
	int16_t *bufferHumidity = (int16_t *)call BufferHumidity.getWindow();
	int16_t meanLight = (int16_t)call MeanLight.execute(bufferLight, call BufferLight.size());
	int16_t meanTemp = (int16_t)call MeanTemp.execute(bufferTemperature, call BufferTemperature.size());
	int16_t meanHum = (int16_t)call MeanHum.execute(bufferHumidity, call BufferHumidity.size());
	
	if(!busy){
	BlinkToRadioMsg* btrpkt = (BlinkToRadioMsg*)(call Packet.getPayload(&pkt, sizeof (BlinkToRadioMsg)));
	btrpkt -> nodeid = TOS_NODE_ID;
	btrpkt -> Lum = meanLight;
	btrpkt -> Temp = meanTemp;
	btrpkt -> Hum = meanHum;
	if ( call AMSend.send(AM_BROADCAST_ADDR, &pkt, sizeof(BlinkToRadioMsg)) == SUCCESS){
		busy=TRUE;		
		}	
	}
  } 

event void AMSend.sendDone(message_t* msg, error_t error){
	if (&pkt==msg) busy = FALSE;
}

event void Timer1.fired()
  {
   	call AMControl.start();
	
  }

  event void AMControl.startDone(error_t err){



		if(err==SUCCESS){
				call Leds.led0On();
				call Timer0.startPeriodic(TIMER_PERIOD_MILLI);		
				call Timer2.startPeriodic(WINDOW_SIZE_MILLIS);		
			}else{ call AMControl.start();}

	}
		event void AMControl.stopDone(error_t err){
			if(err==SUCCESS){
				 call Leds.led0Off();
				call Timer1.startOneShot(100);		
			}else{ call AMControl.stop();}
	}
}
