# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 00:56:06 2025

@author: Atziluth
"""
import struct
import os
import numpy as np
def Simulate_PreProcess(FilePath, chirpCfg, CompressionCfg):
    DataSize = os.path.getsize(FilePath)
    RawData = open(FilePath, "rb")
    data = RawData.read()
    RawData.close()
    # 读取 2 字节并按 'H' 格式（无符号短整数）解析
          # 假设文件包含 2 字节
    if data:
        data = struct.unpack('<' + 'H' * (len(data) // 2), data)
        sorted_data = np.reshape(data,
                                 (chirpCfg["numRx"] * CompressionCfg["RangebinPerBlock"],
                                  chirpCfg["numChirps"] // CompressionCfg["numChirpsPerloop"],
                                  CompressionCfg["numChirpsPerloop"],
                                  chirpCfg["numRangebins"] // CompressionCfg["RangebinPerBlock"]))
        # print(f"Parsed value: {value}")
        1