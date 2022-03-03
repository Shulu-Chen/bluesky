#!/usr/bin/python3
# coding: utf-8
'''
 @Time    : 12/1/2021 11:05 PM
 @Author  : Shulu Chen
 @FileName: trj_analysis.py
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

trj_dir1 = "output/NAIVE__20220303_12-30-48.log"

route_dir1 = "scenario/NYC_case1.scn"

f=open("scenario/interface_naive.scn","w")

def route_type_get(route_dir):
    route = open(route_dir)
    route_type = []

    line_id = 0
    read_line_id = -1

    start_count=False
    for line in route:
        line_id += 1
        if line == "####\n":
            start_count = True
        if start_count:
            if line == "\n":
                read_line_id = line_id+1
            if read_line_id == line_id:
                line_sp = line.split()
                x = [char for char in line_sp[1]]
                route_type.append(x[0])
    return route_type


def get_distance(loc):
    horizon_dist=geodesic((loc[0][0],loc[0][1]), (loc[1][0],loc[1][1])).m
    dist=sqrt(horizon_dist**2+(loc[0][2]-loc[1][2])**2)
    return dist

def run_time_get(dir):
    df = pd.read_csv(dir, sep=",", header=None, names=["simt", "id", "lat", "lon", "alt", "tas", "vs"])
    df = df.drop([0, 1])
    df_id = df.groupby("id")
    id_list = list(df['id'].unique())
    running_time_list = []
    for i in id_list:
        U_id = df_id.get_group(i)
        t_st = float(U_id['simt'].iloc[0])
        t_end = float(U_id['simt'].iloc[-1])
        running_time = t_end-t_st
        running_time_list.append(running_time)
    return running_time_list

def LOS_get(dir):
    df = pd.read_csv(dir, sep=",", header=None, names=["simt", "id", "lat", "lon", "alt", "tas", "vs"])
    df = df.drop([0, 1])
    df_simt = df.groupby("simt")
    simt_list = list(df['simt'].unique())
    LOS=0
    LOS_location=[]
    for t in simt_list[1::5]:
        # print(t)
        df_= df_simt.get_group(t)
        if len(df_)==1:
            continue
        A=df_[['lat','lon',"alt"]].astype(float)
        A=A.to_numpy()
        # result = list(product(A, repeat=2))
        result = list(itertools.combinations(A, 2))
        dist_list = list(map(get_distance, result))
        dist_idx = list(zip(range(len(dist_list)),dist_list))
        LOS_id = list(filter(lambda x:x[1] < 100 ,dist_idx))
        if len(LOS_id)>0:
            for LOS_ in LOS_id:
                LOS_location.append(result[LOS_[0]])
    print(len(LOS_location))
    return LOS_location

def conf_to_csv(in_dir, out_dir):
    t1=time.time()
    LOS_loc = LOS_get(in_dir)
    LOS_x=[]
    LOS_y=[]
    for LOS_ in LOS_loc:
        LOS_x.append(LOS_[0][0])
        LOS_y.append(LOS_[0][1])
    df_LOS=pd.DataFrame({"lat":LOS_x,"lon":LOS_y})
    df_LOS.to_csv(out_dir,index=False)
# x1 = route_type_get(route_dir1)
# x2 = route_type_get(route_dir2)
# y1 = run_time_get(trj_dir1)
# y2 = run_time_get(trj_dir2)

conf_to_csv(trj_dir1,"df_naive.csv")
# conf_to_csv(trj_dir2,"df_dec.csv")

# print("running time",time.time()-t1)
# A_norm=np.sum(np.abs(A)**2,axis=1)
# B=np.tile(A_norm, (len(A_norm), 1))
# dist_mat=B+B.transpose()-2*np.matmul(A, A.transpose())
#
#
# #
# plt.scatter(x=x1,y=y1, label="Naive case")
# plt.scatter(x=x2,y=y2, label="Deconflication")
# plt.legend()
# plt.title("Running time for different route")
# plt.show()