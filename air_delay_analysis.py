#!/usr/bin/python3
# coding: utf-8
'''
 @Time    : 3/4/2022 12:56 AM
 @Author  : Shulu Chen
 @FileName: air_delay_analysis.py
 @Software: PyCharm
'''
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import radians, cos, sin, asin, sqrt
from scipy.spatial import distance
# from itertools import product
from geopy.distance import geodesic
import time
import itertools

trj_dir1 = "output/NAIVE__20220304_10-35-05.log"

# def delay_get(dir):
dir=trj_dir1
df = pd.read_csv(dir, sep=",", header=None, names=["simt", "id", "lat", "lon", "alt", "tas", "vs"])
df = df.drop([0, 1])
df_simt = df.groupby("id")
id_list = list(df['id'].unique())
landing_time=[]
depart_time=[]
for id in id_list:
    # print(t)
    df_= df_simt.get_group(id)
    df_.iloc[-1]['simt']
    landing_time.append(float(df_.iloc[-1]['simt']))
    depart_time.append(float(df_.iloc[0]['simt']))
expected_time=[x+landing_time[0] for x in depart_time]
in_air_delay=np.array(landing_time)-np.array(expected_time)
plt.bar(range(len(in_air_delay)), in_air_delay)
plt.title("In_air delay")
plt.xlabel("Flight id")
plt.ylabel("Delay time/s")
plt.show()
print(in_air_delay)
print(landing_time)