# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 00:56:06 2025

@author: Atziluth
"""
import struct
import os
import numpy as np
import ctypes


import tkinter as tk
from tkinter import ttk

import time 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.widgets import RectangleSelector
from tkinter import ttk


lib = ctypes.CDLL('./EGE_Decompression_Lib/EGE_Decompression.dll')
lib.EGE_Decompression_16bit.argtypes = (ctypes.POINTER(ctypes.c_uint16), # Input array
                                        ctypes.c_uint32,                 # Input array size
                                        ctypes.POINTER(ctypes.c_int16),  # Output array
                                        ctypes.POINTER(ctypes.c_uint8),  # K array
                                        ctypes.c_uint8,
                                        ctypes.POINTER(ctypes.c_uint16))                  # number of samples per-block
lib.EGE_Decompression_16bit.restype = None  # 该函数不返回值

def Simulate_PreProcess(FilePath, chirpCfg, CompressionCfg):
    # Initial progress

    DataSize = os.path.getsize(FilePath)
    RawData = open(FilePath, "rb")
    data = RawData.read()
    RawData.close()
    # 读取 2 字节并按 'H' 格式（无符号短整数）解析
          # 假设文件包含 2 字节
    if data:
        data = struct.unpack('<' + 'H' * (len(data) // 2), data)
        TotalBlock = chirpCfg["numRangebins"] // CompressionCfg["RangebinPerBlock"] * chirpCfg["numDopplerbins"] * 32
        # DecompData = [0] * chirpCfg["numRangebins"] * chirpCfg["numDopplerbins"] * chirpCfg["numRx"]
        DecompData = np.zeros((chirpCfg["numRx"], chirpCfg["numRangebins"], chirpCfg["numDopplerbins"]), dtype=complex)
        # DecompData = np.reshape(DecompData,
        #                         (chirpCfg["numRx"],
        #                          chirpCfg["numRangebins"],
        #                          chirpCfg["numChirps"]), order='F')
        dim2_idx = 0
        dim3_idx = 0
        for i in range(0, TotalBlock, 32):
            data_slice = data[i:i+32]
            data_array = (ctypes.c_uint16 * 32)(*data_slice)
            # data_array = (ctypes.c_uint16 * len(data))(*data)
            output = (ctypes.c_int16 * 64)(*[0] * 64);
            bit = (ctypes.c_uint16 * 64)(*[0] * 64);
            Karr = [3, 4, 5, 7, 9, 11, 13, 15];
            Karray = (ctypes.c_uint8 * 8)(*Karr);
            lib.EGE_Decompression_16bit(
                data_array,
                32,
                output,
                Karray,
                64,
                bit
            )
            output = np.array(output)
            Output = np.reshape(output[1::2] + 1j*output[0::2], (4,8), order='F')
            DecompData[0:4,dim2_idx:dim2_idx+8, dim3_idx] = Output
            dim3_idx = dim3_idx + 1
            if dim3_idx > chirpCfg["numDopplerbins"]-1:
                dim2_idx = dim2_idx + CompressionCfg["RangebinPerBlock"]
                dim3_idx = 0
        # Simulation
        A_fft = 20*np.log10(np.abs(np.fft.fft(DecompData, axis=2)))
        
        root = tk.Tk()
        root.title("Tkinter with Imagesc")
        
        
        # 使用 Matplotlib 创建图像
        fig, ax = plt.subplots(2, 2, figsize=(10, 5))  # 创建一个 5x5 的图形
        def onselect(eclick, erelease, ax):
            # 获取选区坐标
            x1, y1 = int(eclick.xdata), int(eclick.ydata)
            x2, y2 = int(erelease.xdata), int(erelease.ydata)
            if (x2-x1)< 5:
                ax.set_xlim([0, 255])
                ax.set_xlim([0, 767])
            else:
            # 设置显示区域
                ax.set_xlim([x1, x2])
                ax.set_ylim([y2, y1])  # 注意 y 轴是倒置的
            plt.draw()
        def on_mouse_move(event):
            # 如果鼠标点击在图像区域内
            axis = event.inaxes
            if event.inaxes:
                # 获取鼠标在图像上的位置
                x, y = int(event.xdata), int(event.ydata)
                
                # 确保坐标在图像范围内
                if 0 <= x < A_fft.shape[2] and 0 <= y < A_fft.shape[1]:
                    for i in range(0,2):
                        for j in range(0,2):
                            if axis == ax[i,j]:
                                # 获取该位置的数值
                                value = A_fft[i*2+j,y, x]
                                # 更新标题显示鼠标所在点的值
                                ax[i,j].set_title(f"Value at ({x}, {y}): {value:.2f}")
                    fig.canvas.draw_idle()  # 更新图像
        
        
        for i in range(0, 2):
            for j in range(0, 2):
                cax = ax[i,j].imshow(A_fft[i*2+j,:,:], cmap='viridis')  # 使用 'viridis' 配色
                ax[i,j].set_position([0.05+0.5*j, 0.05+0.5*i, 0.7, 0.4])
                fig.colorbar(cax, ax=ax[i, j], orientation='vertical')
                rect_selector = RectangleSelector(ax[i,j],
                                                  lambda eclick, erelease: onselect(eclick, erelease, ax[i,j]), 
                                                  useblit=True,
                                                  button=[1],  # 使用左键
                                                  minspanx=5, minspany=5, spancoords='pixels')
        
        # 将 Matplotlib 图像嵌入到 Tkinter 窗口中
        canvas = FigureCanvasTkAgg(fig, master=root)  # 将图形绑定到 Tkinter 窗口
        canvas.draw()
        
        # 在 Tkinter 窗口中放置画布
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        

        fig.canvas.mpl_connect('motion_notify_event', on_mouse_move)

        
        # 启动 Tkinter 主事件循环
        root.mainloop()