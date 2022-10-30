#!/usr/bin/python
#coding=utf-8

import serial
import struct
import time
import numpy as np

"""
        elif 0.5 < float(max(h))/float(sum(h)) <= 0.85:
            return int((h[x]**2-s[y]**2)/(h[x]+s[y]))
"""
pktlx_list=[]
win=[]
media=[1]
f = open("daylight2.txt","w")


def filtered (light_data):

        if len(pktlx_list)>3:
             win.append(pktlx_list[-5 : -1])
             media.append(sum(win[-1])/4)
             a = light_data-pktlx_list[-1] 
             b = pktlx_list[-1]-pktlx_list[-2]
             c = pktlx_list[-2]-pktlx_list[-3]
             sa,sb,sc = np.sign(a), np.sign(b), np.sign(c)
             if len(win)>2:
                 h = max(media[-5:-2])-min(media[-5:-2])
                 if h==0:
                     h=1 
                 if abs(a)/h and abs(b)/h > 10 and sa!=sb:
                     pktlx_list[-1]=media[-1]
                     pktlx_list.append(light_data)
                 elif abs(a)/h and abs(c)/h > 10 and sa!=sc:
                     pktlx_list[-1]=media[-1]
                     pktlx_list[-2]=media[-1]
                     pktlx_list.append(light_data)
                 else:
                     pktlx_list.append(light_data)
             else:
                 pktlx_list.append(light_data)
        else:
            pktlx_list.append(light_data)


def PWMchoose (medialive):
    h,_ = np.histogram(medialive[-12:-1], bins=list(range(0,13,3)+[26,3000])) # numero di oss dei valori della finestra nei bin
    x = np.argmax(h)
    if sum(h)>0 :
        o = max(h)
        e = float(o)/float(sum(h))
        if e > 0.8 and int(x)<5:
            return int(x*3)
        elif int(x)>=5:
            return 50
            print 'PWM change'
        else: 
            return 200
            print 'PWM OFF'
    else:
        return 200



while True:

    ser = serial.Serial("/dev/ttyUSB0",115200,8,"N",2,timeout=2)
    rawdata = ser.read(18)
    ser.close()
    data = struct.unpack("B"*len(rawdata),rawdata)
    if len(data)==18:# and data[0]==0 and data[5]==255 and data[6]==255:
        num0 = (data[0])
        num1 = (data[1])
        num2 = (data[2])
        num3 = (data[3])
        num4 = (data[4])
        num5 = (data[5])
        num6 = (data[6])
        num7 = (data[7])
        num8 = (data[8])
        num9 = (data[9])
        num10 = (data[10])
        num11 = (data[11])
        num12 = (data[12])
        num13 = (data[13])
        num14 = (data[14])
        num15 = (data[15])
        num16 = (data[16])
        num17 = (data[17])
        light_data=(num12 << 8) + num13
        temperature_data=(num14 << 8) + num15
        humidity_data=(num16 << 8) + num17
        
        filtered(light_data)
        PWM_bin_val = PWMchoose(media)

        light= 0.281616211*light_data  
        temperature=-39+0.01*temperature_data
        humidity=-2+0.04*humidity_data+0.000002*humidity_data*humidity_data
        tim= time.strftime("%H:%M:%S")


        print(light_data, media[-1], PWM_bin_val)
        print "\n\nPacchetto: [%d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d]" % (num0,num1,num2,num3,num4,num5,num6,num7,num8,num9,num10,num11,num12,num13,num14,num15,num16,num17)
        print "Luminosità: %.2f lx\tTemperatura: %.2f °C\tUmidità: %.2f RH\tOrario: %s\tMedia lux: %.2f lx\tPWM_bin_val: %d\n" % (light,temperature,humidity, tim, media[-1], PWM_bin_val)
        f.write( "\n\nPacchetto: [%d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d]\n" % (num0,num1,num2,num3,num4,num5,num6,num7,num8,num9,num10,num11,num12,num13,num14,num15,num16,num17))
        f.write( "Luminosità: %.2f lx\tTemperatura: %.2f °C\tUmidità: %.2f RH\tOrario: %s\tMedia lux: %.2f lx\tPWM_bin_val: %d\n" % (light,temperature,humidity,tim,media[-1], PWM_bin_val))
f.close()
       

