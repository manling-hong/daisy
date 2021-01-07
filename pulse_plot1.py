import matplotlib.pyplot as plt
import numpy as np
import time
import time, random
import math
import serial
from collections import deque
from scipy import signal



#Display loading 
class PlotData:
    def __init__(self, max_entries=30):
        self.axis_x = deque(maxlen=max_entries)
        self.axis_y = deque(maxlen=max_entries)
    def add(self, x, y):
        self.axis_x.append(x)
        self.axis_y.append(y)


#initial
fig, (ax,ax2,ax3,ax4) = plt.subplots(4,1)
#fig, (ax,ax2,ax3) = plt.subplots(3,1)
line,  = ax.plot(np.random.randn(100))
line2, = ax2.plot(np.random.randn(100))
line3, = ax3.plot(np.random.randn(100))
line4, = ax4.plot(np.random.randn(100))
plt.show(block = False)
plt.setp(line2,color = 'r')
plt.setp(line3,color = 'b')
plt.setp(line4,color = 'g')

PData= PlotData(500)

ax.set_ylim(0,500)
ax2.set_ylim(-5,5)
ax3.set_ylim(0,500)
ax4.set_ylim(0,500)


# plot parameters
print ('plotting data...')
# open serial port
strPort='com5'
ser = serial.Serial(strPort, 115200)
ser.flush()

start = time.time()
#即時信號頻譜顯示，橫軸以 (Hz)計算，並能看出心跳頻帶
#t = np.arange(0, ax2.size/fs/10, 1/fs/10)
#plt.figure(figsize=(10,5), dpi=200)
#f=t*250
#plt.plot(f, ecg)


while True:
    
    for ii in range(10):

        try:
            data = float(ser.readline())
            PData.add(time.time() - start, data)
        except:
            pass

    ax.set_xlim(PData.axis_x[0], PData.axis_x[0]+5)
    ax2.set_xlim(PData.axis_x[0], PData.axis_x[0]+5)
    ax3.set_xlim(PData.axis_x[0], PData.axis_x[0]+5)
    ax4.set_xlim(PData.axis_x[0], PData.axis_x[0]+5)
    line.set_xdata(PData.axis_x)
    line.set_ydata(PData.axis_y)
    line2.set_xdata(PData.axis_x)
    line2.set_ydata(PData.axis_y-np.mean(PData.axis_y))
    fs=7200
    line3.set_xdata(fs*PData.axis_x)
    line3.set_ydata(abs(np.fft.fft(PData.axis_y-np.mean(PData.axis_y))))
    line4.set_xdata(PData.axis_x)
    line4.set_ydata(PData.axis_y)
    fig.canvas.draw()
    fig.canvas.flush_events()
    
   
r=[0]*126
for i in range(0,126):
    x = np.cos(2*np.pi*i*t)
    y = signal.lfilter([1/4,-2/4, 1/4], 1, x)
    r[i]=np.max(y)/np.max(x)

plt.plot(r,'b-')
