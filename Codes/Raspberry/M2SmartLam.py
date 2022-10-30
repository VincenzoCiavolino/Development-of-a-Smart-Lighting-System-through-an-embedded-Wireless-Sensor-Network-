#!/usr/bin/python
#coding=utf-8

import os
import serial
import struct
import time
import re
import urllib
import RPi.GPIO as GPIO
import smtplib
import numpy as np


dc = None
ran = 7
auto = False
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(12, GPIO.OUT)  # Set GPIO pin 12 to output mode.
pwm = GPIO.PWM(12, 100)  # Initialize PWM on pwmPin 100Hz frequency
pwm.start(0)  

url = "http://dimmer.altervista.org/get_data.php"
readlist =[[],[],[]]
media = [[1],[1],[1]]
win=[[],[],[]]

#GMail Credentials
gmail_sender = ' ciavolino.vincenzo@gmail.com '#mittente
gmail_passwd = ' lescusva '

TO = ' ciavolino.vincenzo@gmail.com ' #destinatario
SUBJECT = 'Allarme'#oggetto email
TEXT = 'Incendio rilevato'#messaggio

#Create connection to gmail service
server = smtplib.SMTP('smtp.gmail.com',587)
server.ehlo()
server.starttls()
server.ehlo
server.login(gmail_sender, gmail_passwd)

#Definizione struttura messaggio
BODY = '\r\n'.join([
       'To: %s' % TO,
       'From: %s ' % gmail_sender,
       'Subject: %s' % SUBJECT,
       '',
       TEXT ])



def filtered (data,i):
        if len(readlist[i])>3:
             win[i].append(readlist[i][-5 : -1])
             media[i].append(round(float(sum(win[i][-1])/4),2))
             a = data-readlist[i][-1] 
             b = readlist[i][-1]-readlist[i][-2]
             c = readlist[i][-2]-readlist[i][-3]
             sa,sb,sc = np.sign(a), np.sign(b), np.sign(c)
             if len(media[i])>2:
                 h = max(media[i][-5:-2])-min(media[i][-5:-2])
                 if h==0:
                     h=1 
                 if abs(a)/h and abs(b)/h > 10 and sa!=sb:
                     readlist[i][-1]=round(media[i][-1],2)
                     readlist[i].append(data)
                 elif abs(a)/h and abs(c)/h > 10 and sa!=sc:
                     readlist[i][-1]=round(media[i][-1],2)
                     readlist[i][-2]=round(media[i][-1],2)
                     readlist[i].append(data)
                 else:
                     readlist[i].append(data)
             else:
                 readlist[i].append(data)
        else:
            readlist[i].append(data)


def PWMchoose (medialive):
    a = list(range(0,13,3)+[26,3000])
    # numero di oss dei valori della finestra nei bin
    h,_ = np.histogram(medialive[-12:-1], bins=a)   
    x = np.argmax(h)
    if sum(h)>0 :
        o = max(h)
        e = float(o)/float(sum(h))
        if e > 0.8 and int(x)<5:
            print 'PWM change'
            return int(x)
        elif int(x)>=5:
            print 'PWM OFF'
            return 50
        else: 
            return 200
    else:
        return 200



def history(dictionary,lista):
    for i, (key, val) in enumerate(dictionary.iteritems()):
        if len(lista[i])<10: 
            lista[i].append(val)
            print "\nUltime %d letture di %s: " %(len(lista[i]),key)
            print (lista[i]) 
        else :
            lista[i].append(val)
            del lista[i][0]
            print "\nUltime 10 letture di %s:" %(key)
            print (lista[i])

def autoreg(n,rg):
    s = 1
    if n ==0 and rg!=100:
        for i in range(rg,100):
            pwm.ChangeDutyCycle(i)
        print("Duty cycle impostato a: 100%%")
        return 100
    elif n ==1 and rg!=80:
        if rg > 80:
            s=-1
        for i in range(rg,80,s):
            pwm.ChangeDutyCycle(i)
        print("Duty cycle impostato a: 80%%")
        return 80
    elif n ==2 and rg!=60:
        if rg > 60:
            s=-1
        for i in range(rg,60,s):
            pwm.ChangeDutyCycle(i)
        print("Duty cycle impostato a: 60%%")
        return 60
    elif n ==3 and rg!=50:
        if rg > 50:
            s=-1
        for i in range(rg,50,s):
            pwm.ChangeDutyCycle(i)
        print("Duty cycle impostato a: 50%%")
        return 50
    elif n ==4 and rg!=30:
        if rg > 30:
            s=-1
        for i in range(rg,30,s):
            pwm.ChangeDutyCycle(i)
        print("Duty cycle impostato a: 30%%")
        return 30
    elif n ==5 and rg!=0:
        for i in range(rg,0,-1):
            pwm.ChangeDutyCycle(i)
        print ("Lamp OFF")
        return 0
  
    

while True:
    req = urllib.urlopen(url) 
    val=(req.read().decode('utf-8'))
    dc_url = int(re.search(r'\d+', val).group())
    if (dc_url != dc):
        dc = dc_url
        if dc != 0:
            auto = False
            pwm.ChangeDutyCycle(dc)
            print "Duty Cycle impostato a: %d%%" %(dc)
        else:
            auto = True
            print "Modalità automatica: START"
    ser = serial.Serial("/dev/ttyUSB0",115200,8,"N",2,timeout=2)
    rawdata = ser.read(18)
    ser.close()
    data = struct.unpack("B"*len(rawdata),rawdata)
    if len(data)==18:
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
        light= 0.281616211*light_data
        temperature_data=(num14 << 8) + num15
	temperature=-39+0.01*temperature_data
	humidity_data=(num16 << 8) + num17
	humidity=-2+0.04*humidity_data+0.000002*humidity_data*humidity_data
        tim= time.strftime("%H:%M:%S")

        filtered(light_data,0)
        filtered(temperature,1)
        filtered(humidity,2)

        PWM_bin_val = PWMchoose(media[0])
        if auto == True:
            if  PWM_bin_val != 200:
                ran=autoreg(PWM_bin_val,ran)
            if ran != None:
                last = ran

        print "\n\nPacchetto: [%d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d %d]" % (num0,num1,num2,num3,num4,num5,num6,num7,num8,num9,num10,num11,num12,num13,num14,num15,num16,num17)
        print "Luminosità media: %.2f lx\nTemperatura media: %.2f °C\nUmidità media: %.2f RH\nOrario corrente: %s\n" % (media[0][-1]*0.281616211,media[1][-1],media[2][-1],tim)

        lastreads = {
            "luminosità":light,
            "temperatura":round(temperature,2),
            "umidità":round(humidity,2)
        }
        history(lastreads,readlist)

        if ran == None:
            ran = last

        if auto == True:
            print ("\n\nMODALITA': Automatica")
            print "Duty Cycle corrente: %d%%" %(ran)
        else:
            print ("\n\nMODALITA': Manuale")
            print "Duty Cycle corrente: %d%%"%(dc)

        if (media[2] <60) and (media[1] > 35):
            print 'Allarme incendio: invio email'
            #Comando per inviare e-mail
            try:
                server.sendmail(gmail_sender,[TO], BODY)
                print 'Email inviata con successo'
            except:
                print 'Errore invio email'

        

        os.system('clear')
