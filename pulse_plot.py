from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
import time
import time, random
import math
import serial
from collections import deque
from scipy.signal import butter, lfilter, freqz

#Display loading 
#deque:一個類似 list 的容器，可以快速的在頭尾加入元素與取出元素。
#執行一次PlotData就會更新30個數據
class PlotData:
    def __init__(self, max_entries=30):
        self.axis_x = deque(maxlen=max_entries) #一個有30個位子的list
        self.axis_y = deque(maxlen=max_entries)
    def add(self, x, y):
        self.axis_x.append(x)
        self.axis_y.append(y)


#initial
#輸出總畫布"視窗"的
fig, (ax,ax2,ax3,ax4) = plt.subplots(4,1) #畫出2*1的子圖 #ax:設定圖表的子圖位置
#np.random.randn:根據給定維度生成[0,1)之間的資料
line,  = ax.plot(np.random.randn(100))
line2, = ax2.plot(np.random.randn(100))
line3, = ax3.plot(np.random.randn(100))
line4, = ax4.plot(np.random.randn(100))
#line5, = ax5.plot(np.random.randn(100))

plt.show(block = False)
plt.setp(line2,color = 'r')
plt.setp(line3,color = 'b')



PData= PlotData(500)
#設定軸的限制 (始值,終值)
ax.set_ylim(0,500)
ax2.set_ylim(-5,5)
ax3.set_ylim(0,100)
ax4.set_ylim(0,1.5)




# plot parameters
print ('plotting data...')
# open serial port
#要跟著arduino的連結改定com數
strPort='com5'
#選擇裝置
ser = serial.Serial(strPort, 115200)
#用來刷新緩衝區的，即將緩衝區中的數據立刻寫入文件，
#同時清空緩衝區，不需要是被動的等待輸出緩衝區寫入。
ser.flush()

#返回當前時間的時間戳
start = time.time()
#try-except:例外錯誤處理，將錯誤置於try區塊，
#在except區塊定義有錯誤發生時，需進行的反應。
while True:
    
    for ii in range(10):

        try:
            #.readline():返回一個字串物件
            data = float(ser.readline())
            #.add():給予集合添加元素，如果元素已存在，則不執行操作。
            PData.add(time.time() - start, data)
        except:
            pass

    plt.title("未處理訊號")
    ax.set_xlim(PData.axis_x[0], PData.axis_x[0]+5) #PData.axis_x[0]=?
    plt.title("過濾直流訊號之訊號")
    ax2.set_xlim(PData.axis_x[0], PData.axis_x[0]+5)
    #ax3.set_xlim(PData.axis_x[0], PData.axis_x[0]+5)
    
    
    line.set_xdata(PData.axis_x)
    line.set_ydata(PData.axis_y)
    #更新繪圖。
   
    line2.set_xdata(PData.axis_x)
    line2.set_ydata(np.array(PData.axis_y)-np.mean(PData.axis_y))
   
    #plt.plot(PData.axis_x*fs,abs(np.fft.fft(PData.axis_y-np.mean(PData.axis_y))))
    #更新繪圖。
   

    #即時信號頻譜顯示，橫軸以 (Hz)計算，並能看出心跳頻帶
    # !!!x軸代表什麼，並轉換成頻率 #如果是第一秒跟第二秒...
    #lesson2 實驗10
    fs=300
    line3.set_xdata(np.arange(len(PData.axis_y)))
    
    #print(len(PData.axis_x*fs))
    line3.set_ydata(abs(np.fft.fft(np.array(PData.axis_y)-np.mean(PData.axis_y))))
    
    #plt.plot(abs(np.fft.fft(np.array(PData.axis_y)-np.mean(PData.axis_y))))
 
    #print(abs(np.fft.fft(PData.axis_y-np.mean(PData.axis_y))).shape)
    Fs=np.arange(0, 100, 1)
    line4.set_xdata(Fs)
    #x=abs(np.fft.fft(np.array(PData.axis_y)-np.mean(PData.axis_y)))
    
   # y=signal.lfilter([1/3, 1/3, 1/3], 1,x)
   # y = signal.lfilter([1/5,1/5,1/5,1/5,1/5], 1, (np.array(PData.axis_y)-np.mean(PData.axis_y)))
    y2=[]
    t = np.arange(0, 1, 1/fs) 
    for i in Fs:
        x = np.cos(2*np.pi*i*t)
        y = signal.lfilter([1/5,1/5,1/5,1/5,1/5], 1, x)
        y2.append(max(y))   
    line4.set_ydata(y2)
  
    fig.canvas.draw()
    fig.canvas.flush_events()