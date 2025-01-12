# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import matplotlib.pyplot as plt
import numpy as np
import struct
from pathlib import Path
from scipy.fft import fft, fftfreq, ifft
import tkinter as tk
from tkinter import messagebox
import os
import time
from tkinter import filedialog
import HandleDefinition as h
import RunSimulate

def UpdateDataList(name, index, mode):
    uint16_size = struct.calcsize('H')
    try:
        path = Path(h.MainHandle["UI_DircPathEdit"].get())
        h.MainHandle["UI_FileListbox"].delete(0, tk.END)
        # 遍历目录中的所有文件和文件夹
        for file in path.iterdir():
            if file.suffix.lower() == ".bin":# 如果是文件
                # 获取文件的大小
                file_size = file.stat().st_size
                # print(h.chirpCfg["numRx"] * h.chirpCfg["numRangebins"] * h.chirpCfg["numDopplerbins"] * uint16_size * 2 * h.CompressionCfg["CompressionRatio"])
                if file_size == h.chirpCfg["numRx"] * h.chirpCfg["numRangebins"] * h.chirpCfg["numDopplerbins"] * uint16_size * 2 * h.CompressionCfg["CompressionRatio"]:
                    h.MainHandle["UI_FileListbox"].insert(tk.END, file.name)
    
    except FileNotFoundError:
        print(f'The directory {h.MainHandle["UI_DircPathEdit"].get()} does not exist.')
    except PermissionError:
        print(f'Permission denied to access {h.MainHandle["UI_DircPathEdit"].get()}.')

def SelectPath_CallbackFcn():
    """
    顯示檔案選擇對話框，讓使用者選擇檔案。
    :return: 選擇的檔案路徑（若取消選擇則返回 None）
    """
    # 初始化 tkinter 主視窗（隱藏主視窗）
    root = tk.Tk()
    root.withdraw()

    # 顯示檔案選擇對話框
    h.MainHandle["FilePath"] = filedialog.askdirectory(
        title="選擇路徑")
    if h.MainHandle["UI_DircPathEdit"] is not None:
        h.MainHandle["UI_DircPathEdit"].delete(0, tk.END)
        h.MainHandle["UI_DircPathEdit"].insert(0, h.MainHandle["FilePath"])
    else:
        print("Error: h.MainHandle['FilePathEdit'] is None")
    # MainHandle["FilePathEdit"].insert(0, )

def RunSimulateCallback():
    selected_index = h.MainHandle["UI_FileListbox"].curselection()
    if not selected_index:
        messagebox.showwarning("Warning", "No file select.")

    else:
        for idx in selected_index:
            FilePath = h.MainHandle["UI_DircPathEdit"].get() + "/" + h.MainHandle["UI_FileListbox"].get(idx)
            RunSimulate.Simulate_PreProcess(FilePath, h.chirpCfg, h.CompressionCfg)
            print(FilePath)
            
# generate main figure
h.MainHandle["UI_MainFigure"]=tk.Tk()
h.MainHandle["UI_MainFigure"].geometry('500x500')
h.MainHandle["UI_DircPathBtn"] = tk.Button(h.MainHandle["UI_MainFigure"], text="DircPath", command=SelectPath_CallbackFcn)
h.MainHandle["UI_DircPathBtn"].place(x=5, y=5, width=80, height=20)

h.MainHandle["UI_RunSimulate"] = tk.Button(h.MainHandle["UI_MainFigure"], text="Load Data", command=RunSimulateCallback)
h.MainHandle["UI_RunSimulate"].place(x=25, y=110, width=80, height=30)

h.MainHandle["UI_FileListScroll"] = tk.Scrollbar(h.MainHandle["UI_MainFigure"], orient=tk.VERTICAL)
h.MainHandle["UI_FileListScroll"].place(x=280, y=50, width=20, height=300)  # 设置滚动条的位置和大小

h.MainHandle["UI_FileListbox"] = tk.Listbox(h.MainHandle["UI_MainFigure"], selectmode=tk.MULTIPLE)  # selectmode 可选 SINGLE, BROWSE, MULTIPLE, EXTENDED
h.MainHandle["UI_FileListbox"].place(x=150, y=50, width=150, height=300)
h.MainHandle["UI_FileListbox"].config(yscrollcommand=h.MainHandle["UI_FileListScroll"].set)

h.MainHandle["DircPathTrace"] = tk.StringVar()
h.MainHandle["DircPathTrace"].trace_add("write", UpdateDataList)

h.MainHandle["UI_DircPathEdit"] = tk.Entry(h.MainHandle["UI_MainFigure"], textvariable = h.MainHandle["DircPathTrace"])
h.MainHandle["UI_DircPathEdit"].place(x=100, y=5, width=300, height=20)


h.MainHandle["UI_MainFigure"].mainloop()



