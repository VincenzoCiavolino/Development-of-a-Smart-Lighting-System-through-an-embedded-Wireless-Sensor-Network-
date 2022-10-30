#!/usr/bin/python
#coding=utf-8

import matplotlib.pyplot as plt
import numpy as np
import math
#from statsmodels.nonparametric.smoothers_lowess import lowess

fin = open("daylight2.txt", 'r')
lux_list = []
temp_list = []
hum_list = []
time_list = []
pktlx_list=[]
PWM_bin_val=[]
medialive=[]
win = []
media=[]


b=[]
binwin=[]
alfa,alpha = 1, 0.6
filtwin=[]
my_ewma2 = []
pesi = [1.2**-x for x in range(200)]


for line in fin:
     if line.startswith("Luminosità"):
         values = line.split()
         lux_list.append(float(values[1]))
         temp_list.append(float(values[4]))
         hum_list.append(float(values[7]))
         time_list.append(values[10])
         medialive.append(float(values[13]))
         PWM_bin_val.append(int(values[16]))
     if line.startswith("Pacchetto"):
         vals = line.split()
         z = (int(vals[13]) << 8) + int(vals[14])
    #funzione elimina picchi
         if len(pktlx_list)>2:
             a = z-pktlx_list[-1] 
             b = pktlx_list[-1]-pktlx_list[-2]
             c = pktlx_list[-2]-pktlx_list[-3]
             sa,sb,sc = np.sign(a), np.sign(b), np.sign(c)
             if abs(a) and abs(b) > 50 and sa!=sb:
                 pktlx_list[-1]=z
                 pktlx_list.append(z)
             elif abs(a) and abs(c) > 50 and sa!=sc:
                 pktlx_list[-1]=z
                 pktlx_list[-2]=z
                 pktlx_list.append(z)
             else:
                 pktlx_list.append(z)
         else:
             pktlx_list.append(z)
         
fin.close()


for i in range(len(pktlx_list)):
    win.append(pktlx_list[i-8 : i])



for n in range(10,len(win)):
    a = max(win[n-2])-min(win[n-2])         
    if a==0:
       a=1                                   
    if (win[n][-1]-win[n][-2])/(a) and (win[n][-2]-win[n][-3])/(a) > 10 and np.sign(win[n][-1]-win[n][-2])!=np.sign(win[n][-2]-win[n][-3]):
        media[-1]=media[-2]
        media.append(media[-1])
    else:
        media.append(sum(win[n])/8)


def steady_state(out):
 if len(out) < 20:
  return False
 temp = out[-20:]
 variance = np.var(temp, dtype=np.float64)
 if variance < 0.001:
  return True


def PWMchoose (medialive):
    h,_ = np.histogram(medialive[-37:-26], bins=list(range(0,13,3))) # numero di oss dei valori della finestra nei bin
    x = np.argmax(h)
    #print h
    if sum(h)>0 :
        o = max(h)
        e = float(o)/float(sum(h))
        if e > 0.8 and int(x)<5:
            print ('PWM change')
            print ('range #%d'%int(x))
            return int(x)
        elif int(x)>=5:
            print ('PWM OFF')
            return (50)
        else: 
            print ('No change')
            return (200)
    else:
        print ('No change')
        return 200



z=PWMchoose(medialive)
h,_ = np.histogram(medialive[-37:-26], bins=list(range(0,13,3))) # numero di oss dei valori della finestra nei bin
    
a = np.digitize(medialive[169:180],_)                                                        # indice del binquale va prox dato
b = np.digitize(medialive[-26:-15],_)   


plt.figure(1)
ax = plt.subplot(221)
ax.legend(loc="upper right",fontsize = 'x-small')
for t,r,g in zip(range(3,18,3),[0.8,0.6,0.4,0.3,0.2,0],[100,80,60,50,30,0]):
 ax.axhline(t-0.2, linestyle='--', color='g',linewidth=2) # horizontal lines
 ax.fill_between(range(len(medialive[165:195])+1),t-3,t,color='orange',alpha=r)
 ax.annotate('dc %d%%'%(g),(0.5,t-3))
ax.annotate('dc 0%',(0.5,15))
plt.plot(medialive[165:195],'b-o', markersize=3,label='Letture medie')
plt.plot(range((195-191),(195-191)+len(medialive[169:180])),medialive[169:180],'r-o', linewidth=2,markersize=4,label='Ultima finestra di media')
plt.yticks(range(0, 19),(round(x*0.2816,2) for x in range(0, 19)))
ax.yaxis.set_major_locator(plt.MultipleLocator(3))
ax.yaxis.set_minor_locator(plt.MultipleLocator(1))
ax.set_ylabel(u"Luminosità rilevata (lx)")
ax.set_xlabel(u"Numero campioni")
ax.legend(loc="upper right")
#plt.plot(PWM_bin_val,'g-*',markersize=5,linewidth=3)


ax1 = plt.subplot(222)
ax1.axhline(9, linestyle='--', color='g') # horizontal lines

ax1.annotate('Soglia di\nattivazione',(0.1,8.4))
for t,r in zip(range(6),[0.9,0.7,0.5,0.4,0.3,0]):
 ax1.fill_betweenx(range(12),t,t+1,color='orange',alpha=r)
plt.hist(a, bins=range(0,7))
plt.yticks(range(0, 12))
plt.xticks(range(1,6),[100,80,60,50,30,0])
ax1.set_ylabel('Numero di osservazioni')
ax1.set_xlabel(u'Intervalli di luminosità (% duty cycle)')


a = np.digitize(medialive[175:186],_)                                                        # indice del binquale va prox dato
b = np.digitize(medialive[-32:-21],_) 
ax2 = plt.subplot(223)
ax2.legend(loc="upper right",fontsize = 'x-small')
for t,r,g in zip(range(3,18,3),[0.8,0.6,0.4,0.3,0.2,0],[100,80,60,50,30,0]):
 ax2.axhline(t-0.2, linestyle='--', color='g',linewidth=2) # horizontal lines
 ax2.fill_between(range(len(medialive[165:195])+1),t-3,t,color='orange',alpha=r)
 ax2.annotate('dc %d%%'%(g),(0.5,t-3))
ax2.annotate('dc 0%',(0.5,15))
plt.plot(medialive[165:195],'b-o', markersize=3,label='Letture medie')
plt.plot(range((195-185),(195-185)+len(medialive[175:186])),medialive[175:186],'r-o', linewidth=2,markersize=4,label='Ultima finestra di media')
plt.yticks(range(0, 19),(round(x*0.2816,2) for x in range(0, 19)))
ax2.yaxis.set_major_locator(plt.MultipleLocator(3))
ax2.yaxis.set_minor_locator(plt.MultipleLocator(1))
ax2.set_ylabel(u"Luminosità rilevata (lx)")
ax2.set_xlabel(u"Numero campioni")
ax2.legend(loc="upper right")
#plt.plot(PWM_bin_val,'g-*',markersize=5,linewidth=3)


ax3 = plt.subplot(224)
ax3.axhline(9, linestyle='--', color='g') # horizontal lines

ax3.annotate('Soglia\nattivazione',(0.1,8.4))
for t,r in zip(range(6),[0.8,0.7,0.5,0.4,0.3,0]):
 ax3.fill_betweenx(range(12),t,t+1,color='orange',alpha=r)
plt.hist(a, bins=range(0,7))
plt.yticks(range(0, 12))
plt.xticks(range(1,7),[100,80,60,50,30,0])
ax3.set_ylabel('Numero di osservazioni')
ax3.set_xlabel(u'Intervalli di luminosità (% duty cycle)')


#for x,y,z in zip(range(0,len(pktlx_list)),pktlx_list,lux_list):
 #    ax.annotate('(%s)'%(y),xy=(x,y), fontsize='xx-small')

plt.subplots_adjust(left=0.05, right=0.97, top=0.97,bottom=0.06,wspace=0.3,hspace=0.3)


plt.figure(2)
ax = plt.subplot(221)
ax.legend(loc="upper right",fontsize = 'x-small')
for t,r,g in zip(range(3,18,3),[0.8,0.6,0.4,0.3,0.2,0],[100,80,60,50,30,0]):
 ax.axhline(t-0.2, linestyle='--',color='g',lw=2) # horizontal lines
 ax.fill_between(range(len(medialive[-45:-15])+1),t-3,t,color='orange',alpha=r)
 ax.annotate('dc %d%%'%(g),(0.5,t-3))
ax.annotate('dc 0%',(0.5,15))
ax.plot(medialive[-35:-5],'b-o', markersize=3,label='Letture medie')
ax.plot(range((35-32),(35-32)+len(medialive[-32:-21])),medialive[-32:-21],'r-o', linewidth=2,markersize=4,label='Ultima finestra di media')
plt.yticks(range(0, 19),(round(x*0.2816,2) for x in range(0, 19)))
ax.yaxis.set_major_locator(plt.MultipleLocator(3))
ax.yaxis.set_minor_locator(plt.MultipleLocator(1))
ax.set_ylabel(u"Luminosità rilevata (lx)")
ax.set_xlabel(u"Numero campioni")
ax.legend(loc="upper right")
#plt.plot(PWM_bin_val,'g-*',markersize=5,linewidth=3)


ax1 = plt.subplot(222)
ax1.axhline(9, linestyle='--', color='g') # horizontal lines

ax1.annotate('Soglia\nattivazione',(0.1,8.4))
for t,r in zip(range(6),[0.9,0.7,0.5,0.4,0.3,0]):
 ax1.fill_betweenx(range(12),t,t+1,color='orange',alpha=r)
plt.hist(b, bins=range(0,7))
plt.yticks(range(0, 12))
plt.xticks(range(1,7),[100,80,60,50,30,0])
ax1.set_ylabel('Numero di osservazioni')
ax1.set_xlabel(u'Intervalli di luminosità (% duty cycle)')

a = np.digitize(medialive[169:180],_)                                                        # indice del binquale va prox dato
b = np.digitize(medialive[-26:-15],_)     
ax2 = plt.subplot(223)
ax2.legend(loc="upper right",fontsize = 'x-small')
for t,r,g in zip(range(3,18,3),[0.8,0.6,0.4,0.3,0.2,0],[100,80,60,50,30,0]):
 ax2.axhline(t-0.2, linestyle='--',color='g',lw=2) # horizontal lines
 ax2.fill_between(range(len(medialive[-45:-15])+1),t-3,t,color='orange',alpha=r)
 ax2.annotate('dc %d%%'%(g),(0.5,t-3))
ax2.annotate('dc 0%',(0.5,15))
ax2.plot(medialive[-35:-5],'b-o', markersize=3,label='Letture medie')
ax2.plot(range((35-26),(35-26)+len(medialive[-26:-15])),medialive[-26:-15],'r-o', linewidth=2,markersize=4,label='Ultima finestra di media')
plt.yticks(range(0, 19),(round(x*0.2816,2) for x in range(0, 19)))
ax2.yaxis.set_major_locator(plt.MultipleLocator(3))
ax2.yaxis.set_minor_locator(plt.MultipleLocator(1))
ax2.set_ylabel(u"Luminosità rilevata (lx)")
ax2.set_xlabel(u"Numero campioni")
ax2.legend(loc="upper right")
#plt.plot(PWM_bin_val,'g-*',markersize=5,linewidth=3)


ax3 = plt.subplot(224)
ax3.axhline(9, linestyle='--', color='g') # horizontal lines

ax3.annotate('Soglia di\nattivazione',(0.1,8.4))
for t,r in zip(range(6),[0.9,0.7,0.5,0.4,0.3,0]):
 ax3.fill_betweenx(range(12),t,t+1,color='orange',alpha=r)
plt.hist(b, bins=range(0,7))
plt.yticks(range(0, 12))
plt.xticks(range(1,7),[100,80,60,50,30,0])
ax3.set_ylabel('Numero di osservazioni')
ax3.set_xlabel(u'Intervalli di luminosità')
ax3.set_xlabel(u'Intervalli di luminosità (% duty cycle)')





#plt.plot(hum_list)





plt.subplots_adjust(left=0.05, right=0.97, top=0.97,bottom=0.06,wspace=0.3,hspace=0.3)
plt.show()






"""
for slwi in win:
    for j in range(1,len(slwi)):
        n = abs(slwi[j]-slwi[j-1])
        if n == 0 or n == 1:
            beta.append(1
        else:
            x = int((math.log(n,2.5))//1)
            beta.append(pesi[x])

  #  my_ewma2.append(sum(slwi[g]*beta[g-1]/sum(beta) for g in range(len(slwi)-1,-1,-1)))
    my_ewma2.append(sum(slwi[g]*pesi[g]*beta[g-1]/sum([pesi[x] * beta[x] for x in range(8)]) for g in range(len(slwi)-1,0,-1)))
    del beta[:]

"""

                                                                                                                                                                                                                                                                                                       
"""



filtered = lowess(pktlx_list,range(0,len(pktlx_list)),frac=0.009,return_sorted=False)
filtered2 = lowess(pktlx_list,range(0,len(pktlx_list)),frac=0.009,it=2,return_sorted=False)



my_ewma1 = [pktlx_list[0]]

for n in range(1,len(pktlx_list)-1):
    b.append(pktlx_list[n])
    b = b[-20:]
    h,_ = np.histogram(win[n],bins=range(0,3000,3))                                        # numero di oss dei valori della finestra nei bin
    a = np.digitize(win[n],_)                                                        # indice del binquale va prox dato
    q = abs(pktlx_list[n]-pktlx_list[n-1])
  #  print b[0 : 50]
  #  print a, h[a-1]
  #  print sorted(h[h!=0], reverse=True)
    if h[a-1]==sorted(h[h!=0], reverse=True)[0]:
        alfa=1
    elif max(h)>10:
        alfa = float(h[a-1])/20
    else:
        alfa = float(h[a-1])/max(h)
  #  print alfa
    if q == 0 or q == 1:
        my_ewma1.append(my_ewma1[n-1]+alpha*(pktlx_list[n]-my_ewma1[n-1]))
    else:
        x = int((math.log(n,2.5))//1)
        beta = pesi[x]
        my_ewma1.append(my_ewma1[n-1]+alpha*beta*(pktlx_list[n]-my_ewma1[n-1])/q)


"""


