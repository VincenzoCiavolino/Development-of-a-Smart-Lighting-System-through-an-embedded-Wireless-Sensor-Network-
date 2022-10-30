// $Id: BlinkC.nc,v 1.6 2010-06-29 22:07:16 scipio Exp $

#include "Timer.h"
#include "printf.h"

module BlinkToRadioC 
{
  uses interface Timer<TMilli> as Timer0;
  uses interface Timer<TMilli> as Timer1;
  uses interface Leds;
  uses interface Boot;
  uses interface Packet;
  uses interface AMPacket;
  uses interface AMSend;
//  uses interface Receiver;
  uses interface SplitControl as AMControl;
 uses interface Read<uint16_t> as Light;
 uses interface Read<uint16_t> as Temperature;
 uses interface Read<uint16_t> as Humidity;
}

implementation
{

  bool busy = FALSE;
  message_t pkt;
  uint16_t counter0 ;
  uint16_t counter1 ;
  uint16_t counter2 ; 

  event void Boot.booted()
  {
   call AMControl.start();  
  }
event void Light.readDone(error_t result, uint16_t data){
		if(result!=SUCCESS){
			printf("LightSensorP - NESSUNA OPERAZIONE DI LETTURA\n");
			printfflush();		
		}
		else {
			counter0=data;
			//printf("Check Luminosity: %d \n", data);
			}	
	}

event void Temperature.readDone(error_t result, uint16_t data){
		if(result!=SUCCESS){
			printf("TempSensorP - NESSUNA OPERAZIONE DI LETTURA\n");
			printfflush();		
		}
		else {
			counter1=data;
			//printf("Check Temperature: %d \n", data);
			}	
	}

event void Humidity.readDone(error_t result, uint16_t data){
		if(result!=SUCCESS){
			printf("HumSensorP - NESSUNA OPERAZIONE DI LETTURA\n");
			printfflush();		
		}
		else {
			counter2=data;
			//printf("Check Humidity: %d \n", data);
			}	
	}

  event void Timer0.fired()
  {   	
	call Light.read();
	call Temperature.read();
	call Humidity.read();
	//call AMControl.stop();
	
	if(!busy){
	BlinkToRadioMsg* btrpkt = (BlinkToRadioMsg*)(call Packet.getPayload(&pkt, sizeof (BlinkToRadioMsg)));
	btrpkt -> nodeid = TOS_NODE_ID;
	btrpkt -> counter0 = counter0;
	btrpkt -> counter1 = counter1;
	btrpkt -> counter2 = counter2;
	if ( call AMSend.send(AM_BROADCAST_ADDR, &pkt, sizeof(BlinkToRadioMsg)) == SUCCESS){
		busy=TRUE;		
		}	
	}
  } //timer0.fired

event void AMSend.sendDone(message_t* msg, error_t error){
	if (&pkt==msg) busy = FALSE;
}// AMSend.sendDone

event void Timer1.fired()
  {
   	call AMControl.start();
	
  }

  event void AMControl.startDone(error_t err){

		if(err==SUCCESS){
				call Leds.led0On();
				call Timer0.startPeriodic(100);		
			}else{ call AMControl.start();}

	}
		event void AMControl.stopDone(error_t err){
			if(err==SUCCESS){
				 call Leds.led0Off();
				call Timer1.startOneShot(100);		
			}else{ call AMControl.stop();}
	}
}
