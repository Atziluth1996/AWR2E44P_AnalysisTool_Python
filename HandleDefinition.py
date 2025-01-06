# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 01:01:12 2025

@author: Atziluth
"""

chirpCfg = {
    "numRx"          : 4,
    "numTx"          : 4,
    "numADCSamples"  : 512,
    "numRangebins"   : 256,
    "numDopplerbins" : 768,
    "numChirps"      : 768}

CompressionCfg = {
    "CompressionRatio" : 0.5,
    "RangebinPerBlock" : 8,
    "K_Array"          : [3, 4, 5, 7, 9, 11, 13, 15],
    "SrcBitW"          : 16,
    "SamplesPerBlock"  : 64,
    "numChirpsPerloop" : 128}

MainHandle = {
    "UI_MainFigure"    : None,
    "UI_DircPathBtn"   : None,
    "UI_RunSimulate"   : None,
    "UI_DircPathEdit"  : None,
    "UI_FileListbox"   : None,
    "UI_FileListScroll": None,
    "DircPathTrace"    : None,
    "FilePath"         : None,
    "Data"             : None}