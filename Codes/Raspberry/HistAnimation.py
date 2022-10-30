"""
==================
Animated histogram
==================

This example shows how to use a path patch to draw a bunch of
rectangles for an animated histogram.

"""
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as path
import matplotlib.animation as animation

win =[]
media=[]
pktlx_list=[]
data=[]


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


fin = open("daylight2.txt", 'r')

for line in fin:
     if line.startswith("Pacchetto"):
         vals = line.split()
         z = (int(vals[13]) << 8) + int(vals[14])
         filtered(z)
fin.close()

fig, ax = plt.subplots()

# histogram our data with numpy
for x in range(1,len(media)-13):
    data.append(media[-abs(x-13) : -x] )
a = list(range(0,13,3)+[26,300])

print data , a
n,bins = np.histogram(data, bins=a)
   
# get the corners of the rectangles for the histogram
left = np.array(bins[:-1])
right = np.array(bins[1:])
bottom = np.zeros(len(left))
top = bottom + n
nrects = len(left)

# here comes the tricky part -- we have to set up the vertex and path
# codes arrays using moveto, lineto and closepoly

# for each rect: 1 for the MOVETO, 3 for the LINETO, 1 for the
# CLOSEPOLY; the vert for the closepoly is ignored but we still need
# it to keep the codes aligned with the vertices
nverts = nrects*(1 + 3 + 1)
verts = np.zeros((nverts, 2))
codes = np.ones(nverts, int) * path.Path.LINETO
codes[0::5] = path.Path.MOVETO
codes[4::5] = path.Path.CLOSEPOLY
verts[0::5, 0] = left
verts[0::5, 1] = bottom
verts[1::5, 0] = left
verts[1::5, 1] = top
verts[2::5, 0] = right
verts[2::5, 1] = top
verts[3::5, 0] = right
verts[3::5, 1] = bottom

barpath = path.Path(verts, codes)
patch = patches.PathPatch(
    barpath, facecolor='green', edgecolor='yellow', alpha=0.5)
ax.add_patch(patch)

ax.set_xlim(left[0], right[-1])
ax.set_ylim(bottom.min(), top.max())


def animate(i):
    # simulate new data coming in
    for x in range(1,len(media)-13):
        dat = media[-abs(x-13) : -x] 
    a = list(range(0,13,3)+[26,300])
    n,bins = np.histogram(dat, bins=a)
    top = bottom + n
    verts[1::5, 1] = top
    verts[2::5, 1] = top
    return [patch, ]

ani = animation.FuncAnimation(fig, animate, 100, repeat=True, blit=True)
plt.show()
