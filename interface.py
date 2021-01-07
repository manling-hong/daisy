import tkinter as tk  
from PIL import Image,ImageTk 
import matplotlib.pyplot as plt
import numpy as np
import time
import time, random
import math
import serial
from collections import deque
from scipy import signal
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time


              
win = tk.Tk()                          
win.geometry('640x480')                          
win.title('heart rate')  

class PlotData:
    def __init__(self, max_entries=30):
        self.axis_x = deque(maxlen=max_entries) #一個有30個位子的list
        self.axis_y = deque(maxlen=max_entries)
    def add(self, x, y):
        self.axis_x.append(x)
        self.axis_y.append(y)

PData= PlotData(500)

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

#original介面
def original():
    fig,ax=plt.subplots(figsize=(8,8)) 
    line,  = ax.plot(np.random.randn(100))
    plt.show(block = False)
    ax.set_ylim(0,500)
    #顯示
    while True:
    
        for ii in range(10):

            try:
                #.readline():返回一個字串物件
                data = float(ser.readline())
                #.add():給予集合添加元素，如果元素已存在，則不執行操作。
                PData.add(time.time() - start, data)
            except:
                pass

        plt.title("Original")
        ax.set_xlim(PData.axis_x[0], PData.axis_x[0]+5) #PData.axis_x[0]=?
        line.set_xdata(PData.axis_x)
        line.set_ydata(PData.axis_y)
        fig.canvas.draw()
        fig.canvas.flush_events()
        
       
    

#dc介面
def dc():
    fig2, ax2 = plt.subplots(figsize=(8,8))  
    line2, = ax2.plot(np.random.randn(100))
    plt.show(block = False)
    plt.setp(line2,color = 'r')
    ax2.set_ylim(-5,5)
    #顯示
    while True:
    
        for ii in range(10):

            try:
                #.readline():返回一個字串物件
                data = float(ser.readline())
                #.add():給予集合添加元素，如果元素已存在，則不執行操作。
                PData.add(time.time() - start, data)
            except:
                pass
        plt.title("DC filter")
        ax2.set_xlim(PData.axis_x[0], PData.axis_x[0]+5)
        line2.set_xdata(PData.axis_x)
        y_mean=np.array(PData.axis_y)-np.mean(PData.axis_y)
        line2.set_ydata(y_mean)
        fig2.canvas.draw()
        fig2.canvas.flush_events()

#spectrum介面
def spectrum():
    fig3=tk.Toplevel(win)
    fig3.geometry('640x480')                          
    fig3.title('FIR filter')  
    fig3, ax3 = plt.subplots(figsize=(8,8))
    line3, = ax3.plot(np.random.randn(100))
    plt.show(block = False)
    ax3.set_ylim(0,400)
    #顯示
    while True:
    
        for ii in range(10):

            try:
                #.readline():返回一個字串物件
                data = float(ser.readline())
                #.add():給予集合添加元素，如果元素已存在，則不執行操作。
                PData.add(time.time() - start, data)
            except:
                pass
        #即時信號頻譜顯示，橫軸以 (Hz)計算，並能看出心跳頻帶
        # !!!x軸代表什麼，並轉換成頻率 #如果是第一秒跟第二秒...
        #lesson2 實驗10
        plt.title("Spectrum")
        line3.set_xdata(np.arange(len(PData.axis_y)))
        y_fft=abs(np.fft.fft(np.array(PData.axis_y)-np.mean(PData.axis_y)))
        line3.set_ydata(y_fft)
        fig3.canvas.draw()
        fig3.canvas.flush_events()

#fir介面
def fir():
    fig4, ax4 = plt.subplots(figsize=(8,8))
    line4, = ax4.plot(np.random.randn(100))
    plt.show(block = False)
    ax4.set_ylim(0,1.5)
    #顯示
    while True:
    
        for ii in range(10):

            try:
                #.readline():返回一個字串物件
                data = float(ser.readline())
                #.add():給予集合添加元素，如果元素已存在，則不執行操作。
                PData.add(time.time() - start, data)
            except:
                pass
        Fs=np.arange(0, 100, 1)
        line4.set_xdata(Fs)
        x=abs(np.fft.fft(np.array(PData.axis_y)-np.mean(PData.axis_y)))
        y = signal.lfilter([1/5,1/5,1/5,1/5,1/5], 1, (np.array(PData.axis_y)-np.mean(PData.axis_y)))
        y2=[]
        fs=300
        t = np.arange(0, 1, 1/fs) 
        for i in Fs:
            x = np.cos(2*np.pi*i*t)
            y = signal.lfilter([1/5,1/5,1/5,1/5,1/5], 1, x)
            y2.append(max(y))   
        line4.set_ydata(y2)
    
        fig4.canvas.draw()
        fig4.canvas.flush_events()


#z介面
def z():                       
    #顯示
    fig5, ax5 = plt.subplots(figsize=(8,8))
    plt.show(block = False)
    ax5.set_ylim(-2,2)
    ax5.set_ylabel('Imag')
    
    ax5.grid()

    #以z-domain plot畫出你所設計的FIR濾波器之零點極點，注意，零點應調整增益使其位置在單位圓上
    plt.title("Z Domain")
    ax5.set_xlim(-2,2)
    ax5.set_xlabel('Real')
    #畫圓
    angle=np.linspace(-np.pi,np.pi,50)
    cirx=np.sin(angle)
    ciry=np.cos(angle)
    ax5.plot(cirx, ciry,'k-')

    r=np.roots([1/5,1/5,1/5,1/5,1/5])
    ax5.plot(np.real(r),np.imag(r),'rx',markersize=10)

#設定按紐
btn_original = tk.Button(win,command=original,text='Original', bg='orange', fg='Black',font=10)
btn_original.place(rely=0.75, relx=0.1, anchor='center')

btn_dc = tk.Button(win,command=dc, text='DC filter', bg='orange', fg='Black',font=10)
btn_dc.place(rely=0.75, relx=0.3, anchor='center')

btn_spectrum = tk.Button(win,command=spectrum, text='Spectrum', bg='orange', fg='Black',font=10)
btn_spectrum.place(rely=0.75, relx=0.5, anchor='center')

btn_fir = tk.Button(win,command=fir, text='FIR filter', bg='orange', fg='Black',font=10)
btn_fir.place(rely=0.75, relx=0.7, anchor='center')

btn_z = tk.Button(win,command=z, text='Z Domain', bg='orange', fg='Black',font=10)
btn_z.place(rely=0.75, relx=0.9, anchor='center')

#設定標題
title = tk.Label(win, text='Heart Rate',fg='black',font=('Bodoni MT Black',70,'bold'))
title.place(rely=0.4, relx=0.5, anchor='center')



win.mainloop()