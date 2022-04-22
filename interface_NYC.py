#!/usr/bin/python3
# coding: utf-8
'''
 @Time    : 4/8/2022 10:10 AM
 @Author  : Shulu Chen
 @FileName: interface_NYC.py
 @Software: PyCharm
'''

import numpy as np
from random import sample
import bluesky as bs
from bluesky.simulation import ScreenIO
from geopy.distance import geodesic
from math import radians, cos, sin, asin, sqrt
import matplotlib.pyplot as plt
from random import expovariate,seed
import itertools
from tqdm import tqdm
import random
#
class ScreenDummy(ScreenIO):
    """
    Dummy class for the screen. Inherits from ScreenIO to make sure all the
    necessary methods are there. This class is there to reimplement the echo
    method so that console messages are printed.
    """
    def echo(self, text='', flags=0):
        """Just print echo messages"""
        print("BlueSky console:", text)

#conpute the distance of two aircraft, meters
def get_distance(location1,location2):
    lat1=location1[0]
    lon1=location1[1]
    alt1=location1[2]
    lat2=location2[0]
    lon2=location2[1]
    alt2=location2[2]
    horizon_dist=geodesic((lat1,lon1), (lat2,lon2)).m
    dist=sqrt(horizon_dist**2+(alt1-alt2)**2)
    return horizon_dist

# Generate the demand based on exponential distribution, lambda-number of flight per second,
# lambda=0.1--flight interval=10s
def generate_interval(interval,number):
    lambda_x = 1/interval
    ac_demand_interval = [int(expovariate(lambda_x)) for i in range(number)]
    depart_time = np.cumsum(ac_demand_interval)
    depart_time_ori = depart_time.copy()
    return depart_time,depart_time_ori

def init_bs():

    # initialize bluesky as non-networked simulation node
    bs.init('sim-detached')

    # bs.stack.stack('CRELOG NYC 1')
    # bs.stack.stack('NYC ADD id,lat, lon, alt, tas, vs ')
    # bs.stack.stack('NYC ON 1  ')
    # bs.stack.stack('ASAS ON')
    bs.stack.stack('TAXI OFF 4')
    # f.write("00:00:00.00>CRELOG NYC_gui 1\n")
    # f.write("00:00:00.00>NYC_gui ADD id,lat, lon, alt, tas, vs\n")
    # f.write("00:00:00.00>NYC_gui ON 1\n")
    f.write("00:00:00.00>TRAILS ON \n")
    f.write("00:00:00.00>TAXI OFF 4\n")
    # f.write("0:00:00.00>ASAS ON \n")
    f.write("0:00:00.00>PAN 40.689582,-73.886988 \n")
    f.write("0:00:00.00>ZOOM 2 \n")
    # f.write("0:00:00.00>FF \n")
    f.write("\n")

    # set simulation time step, and enable fast-time running
    bs.stack.stack('DT 1;FF')
    # bs.traf.cre(acid="I"+str(0), actype="ELE01",aclat=40.749573, aclon=-73.901223)
    bs.traf.cre(acid="A"+str(0), actype="ELE01",aclat=40.5959242, aclon=-74.0465984)
    # bs.traf.cre(acid="G"+str(0), actype="ELE01",aclat=40.6964385, aclon=-74.1231651)
    add_plane(0,"A")


def add_plane(id,type):
    speed_list=[30,31,32,33,34]

    if type=="A":
        acid="A"+str(id)
        bs.stack.stack(f'ORIG {acid} L_6')
        bs.stack.stack(f'DEST {acid} A_9')
        bs.stack.stack(f'SPD {acid} 32')
        bs.stack.stack(f'ALT {acid} 400')

        f.write(f"00:00:{id}.00>CRE {acid} ELE01 L_6 0 0\n")
        f.write(f"00:00:{id}.00>ORIG {acid} L_6\n")
        f.write(f"00:00:{id}.00>DEST {acid} A_9\n")
        f.write(f"00:00:{id}.00>SPD {acid} 30\n")
        f.write(f"00:00:{id}.00>ALT {acid} 400\n")


        v = random.choice(speed_list)
        bs.stack.stack(f'ADDWPT {acid} L_5, 400, {v}')
        f.write(f"00:00:{id}.00>ADDWPT {acid} L_5, 400, {v}\n")

        v = random.choice(speed_list)
        bs.stack.stack(f'ADDWPT {acid} L_4, 400, {v}')
        f.write(f"00:00:{id}.00>ADDWPT {acid} L_4, 400, {v}\n")

        v = random.choice(speed_list)
        bs.stack.stack(f'ADDWPT {acid} L_3, 400, {v}')
        f.write(f"00:00:{id}.00>ADDWPT {acid} L_3, 400, {v}\n")

        v = random.choice(speed_list)
        bs.stack.stack(f'ADDWPT {acid} L_2, 400, {v}')
        f.write(f"00:00:{id}.00>ADDWPT {acid} L_2, 400, {v}\n")

        v = random.choice(speed_list)
        bs.stack.stack(f'ADDWPT {acid} L_1, 400, {v}')
        f.write(f"00:00:{id}.00>ADDWPT {acid} L_1, 400, {v}\n")

        v = random.choice(speed_list)
        bs.stack.stack(f'ADDWPT {acid} A_2, 400, {v}')
        f.write(f"00:00:{id}.00>ADDWPT {acid} A_2, 400, {v}\n")

        v = random.choice(speed_list)
        bs.stack.stack(f'ADDWPT {acid} A_3, 400, {v}')
        f.write(f"00:00:{id}.00>ADDWPT {acid} A_3, 400, {v}\n")

        v = random.choice(speed_list)
        bs.stack.stack(f'ADDWPT {acid} A_4, 400, {v}')
        f.write(f"00:00:{id}.00>ADDWPT {acid} A_4, 400, {v}\n")

        v = random.choice(speed_list)
        bs.stack.stack(f'ADDWPT {acid} A_5, 400, {v}')
        f.write(f"00:00:{id}.00>ADDWPT {acid} A_5, 400, {v}\n")

        v = random.choice(speed_list)
        bs.stack.stack(f'ADDWPT {acid} A_6, 400, {v}')
        f.write(f"00:00:{id}.00>ADDWPT {acid} A_6, 400, {v}\n")

        v = random.choice(speed_list)
        bs.stack.stack(f'ADDWPT {acid} A_7, 400, {v}')
        f.write(f"00:00:{id}.00>ADDWPT {acid} A_7, 400, {v}\n")

        v = random.choice(speed_list)
        bs.stack.stack(f'ADDWPT {acid} A_8, 400, {v}')
        f.write(f"00:00:{id}.00>ADDWPT {acid} A_8, 400, {v}\n")


        bs.stack.stack(f'DUMPRTE {acid}')
        bs.stack.stack(f'VNAV {acid} ON')

        f.write(f"00:00:{id}.00>VNAV {acid} ON\n")
        f.write(f"00:00:{id}.00>DUMPRTE {acid}\n")

    if type=="G":
        acid="G"+str(id)
        bs.stack.stack(f'ORIG {acid} G_7')
        bs.stack.stack(f'DEST {acid} H_8')
        bs.stack.stack(f'SPD {acid} 32')
        bs.stack.stack(f'ALT {acid} 400')
        v = random.choice(speed_list)
        bs.stack.stack(f'ADDWPT {acid} G_6, 400, {v}')
        bs.stack.stack(f'ADDWPT {acid} G_5, 400, {v}')
        bs.stack.stack(f'ADDWPT {acid} G_4, 400, {v}')
        bs.stack.stack(f'ADDWPT {acid} G_3, 400, {v}')
        bs.stack.stack(f'ADDWPT {acid} G_2, 400, {v}')
        bs.stack.stack(f'ADDWPT {acid} G_1, 400, {v}')
        bs.stack.stack(f'ADDWPT {acid} H_2, 400, {v}')
        bs.stack.stack(f'ADDWPT {acid} H_4, 400, {v}')
        bs.stack.stack(f'ADDWPT {acid} H_7, 400, {v}')
        bs.stack.stack(f'DUMPRTE {acid}')
        bs.stack.stack(f'VNAV {acid} ON')


        f.write(f"00:00:{id}.00>CRE {acid} ELE01 G_7 0 0\n")
        f.write(f"00:00:{id}.00>ORIG {acid} G_7\n")
        f.write(f"00:00:{id}.00>DEST {acid} H_8\n")
        f.write(f"00:00:{id}.00>SPD {acid} 30\n")
        f.write(f"00:00:{id}.00>ALT {acid} 400\n")
        f.write(f"00:00:{id}.00>ADDWPT {acid} G_6, 400, {v}\n")
        f.write(f"00:00:{id}.00>ADDWPT {acid} G_5, 400, {v}\n")
        f.write(f"00:00:{id}.00>ADDWPT {acid} G_4, 400, {v}\n")
        f.write(f"00:00:{id}.00>ADDWPT {acid} G_3, 400, {v}\n")
        f.write(f"00:00:{id}.00>ADDWPT {acid} G_2, 400, {v}\n")
        f.write(f"00:00:{id}.00>ADDWPT {acid} G_1, 400, {v}\n")
        f.write(f"00:00:{id}.00>ADDWPT {acid} H_2, 400, {v}\n")
        f.write(f"00:00:{id}.00>ADDWPT {acid} H_4, 400, {v}\n")
        f.write(f"00:00:{id}.00>ADDWPT {acid} H_7, 400, {v}\n")
        f.write(f"00:00:{id}.00>VNAV {acid} ON\n")
        f.write(f"00:00:{id}.00>DUMPRTE {acid}\n")

    if type=="I":
        acid="I"+str(id)
        bs.stack.stack(f'ORIG {acid} I_6')
        bs.stack.stack(f'DEST {acid} H_8')
        bs.stack.stack(f'SPD {acid} 32')
        bs.stack.stack(f'ALT {acid} 400')
        v = random.choice(speed_list)
        bs.stack.stack(f'ADDWPT {acid} I_5, 400, {v}')
        bs.stack.stack(f'ADDWPT {acid} I_4, 400, {v}')
        bs.stack.stack(f'ADDWPT {acid} I_3, 400, {v}')
        bs.stack.stack(f'ADDWPT {acid} I_2, 400, {v}')
        bs.stack.stack(f'ADDWPT {acid} I_1, 400, {v}')
        bs.stack.stack(f'ADDWPT {acid} H_2, 400, {v}')
        bs.stack.stack(f'ADDWPT {acid} H_4, 400, {v}')
        bs.stack.stack(f'ADDWPT {acid} H_7, 400, {v}')
        bs.stack.stack(f'DUMPRTE {acid}')
        bs.stack.stack(f'VNAV {acid} ON')


        f.write(f"00:00:{id}.00>CRE {acid} ELE01 I_6 0 0\n")
        f.write(f"00:00:{id}.00>ORIG {acid} I_6\n")
        f.write(f"00:00:{id}.00>DEST {acid} H_8\n")
        f.write(f"00:00:{id}.00>SPD {acid} 30\n")
        f.write(f"00:00:{id}.00>ALT {acid} 400\n")
        f.write(f"00:00:{id}.00>ADDWPT {acid} I_5, 400, {v}\n")
        f.write(f"00:00:{id}.00>ADDWPT {acid} I_4, 400, {v}\n")
        f.write(f"00:00:{id}.00>ADDWPT {acid} I_3, 400, {v}\n")
        f.write(f"00:00:{id}.00>ADDWPT {acid} I_2, 400, {v}\n")
        f.write(f"00:00:{id}.00>ADDWPT {acid} I_1, 400, {v}\n")
        f.write(f"00:00:{id}.00>ADDWPT {acid} H_2, 400, {v}\n")
        f.write(f"00:00:{id}.00>ADDWPT {acid} H_4, 400, {v}\n")
        f.write(f"00:00:{id}.00>ADDWPT {acid} H_7, 400, {v}\n")
        f.write(f"00:00:{id}.00>VNAV {acid} ON\n")
        f.write(f"00:00:{id}.00>DUMPRTE {acid}\n")


    f.write("\n")

t_max = 3000                   #seconds
n_steps = int(t_max + 1)
AC_nums = [10,10,50]
AC_intervals = [50,50,50]         #seconds
departure_safety_bound = 150   #seconds
max_speed = 40                 #kts
min_speed = 3                  #kts
delta_v = 5                    #kts
check_inv = 10                 #second
NMAC_dist = 10                 #meters
LOS_dist = 100                 #meters
Warning_dist = 600             #meters
SpeedUp_dist = 800             #meters
merge_capacity = 1

Cross_time_A = 576             #seconds
Cross_time_G = 497             #seconds
Merge_time_G = 1261            #seconds
Merge_time_I = 448
check_block_size = 60         #seconds
Cross_check_block = np.zeros(round(t_max*2/check_block_size))
Merge_check_block = np.zeros(round(t_max*2/check_block_size))


f=open("scenario/interface_NYC.scn","w")
init_bs()
Cross_check_block[int(Cross_time_A/check_block_size)]+=1

def run_sim(check_point_capacity,block_size,number_list=AC_nums,interval_list=AC_intervals):
    NMAC = 0
    LOS = 0
    A_current_ac=0
    G_current_ac=0
    I_current_ac=0
    A_number = number_list[0]
    G_number = number_list[1]
    I_number = number_list[2]
    A_flight_interval = interval_list[0]
    G_flight_interval = interval_list[1]
    I_flight_interval = interval_list[2]
    A_depart_time, A_depart_time_ori = generate_interval(A_flight_interval,A_number)
    G_depart_time, G_depart_time_ori = generate_interval(G_flight_interval,G_number)
    I_depart_time, I_depart_time_ori = generate_interval(I_flight_interval,I_number)
    operate_dic = {}

    for i in tqdm(range(1,n_steps)):
        bs.sim.step()
        ac_list=bs.traf.id
        alt_list=bs.traf.alt
        lat_list=bs.traf.lat
        lon_list=bs.traf.lon
        spd_list=bs.traf.tas

        ## add aircraft based on demand##
        first = random.choice([0,1,2])
        if first == 0:
            if A_current_ac<A_number:
                if i>=A_depart_time[A_current_ac]:
                    if len(lat_list)>=1:
                        try:
                            A_ind = ac_list.index(A_id)
                        except:
                            A_ind = -1
                        dep_dist=get_distance([lat_list[A_ind],lon_list[A_ind],alt_list[A_ind]],[40.5959242,-74.0465984,0])

                        if dep_dist>departure_safety_bound and \
                                Cross_check_block[int((Cross_time_A+A_depart_time[A_current_ac])/block_size)]<check_point_capacity:
                            bs.traf.cre(acid="A"+str(i), actype="ELE01",aclat=40.5959242,aclon=-74.0465984,acalt=0,acspd=3)
                            add_plane(i,"A")
                            A_id = "A"+str(i)
                            Cross_check_block[int((Cross_time_A+A_depart_time[A_current_ac])/block_size)]+=1
                            A_current_ac+=1
                        else:
                            A_depart_time[A_current_ac:]=list(map(lambda x:x+1,A_depart_time[A_current_ac:]))

            if G_current_ac<G_number:
                if i>=G_depart_time[G_current_ac]:
                    if len(lat_list)>=1:
                        try:
                            G_ind = ac_list.index(G_id)
                        except:
                            G_ind = -1
                        dep_dist=get_distance([lat_list[G_ind],lon_list[G_ind],alt_list[G_ind]],[40.6964385,-74.1231651,0])

                        if dep_dist>departure_safety_bound and \
                                Merge_check_block[int((Merge_time_G+G_depart_time[G_current_ac])/block_size)]<check_point_capacity and \
                                Cross_check_block[int((Cross_time_G+G_depart_time[G_current_ac])/block_size)]<check_point_capacity:
                            bs.traf.cre(acid="G"+str(i), actype="ELE01",aclat=40.6964385,aclon=-74.1231651,acalt=0,acspd=3)
                            add_plane(i,"G")
                            G_id = "G"+str(i)
                            Merge_check_block[int((Merge_time_G+G_depart_time[G_current_ac])/block_size)]+=1
                            Cross_check_block[int((Cross_time_G+G_depart_time[G_current_ac])/block_size)]+=1
                            G_current_ac+=1
                        else:
                            G_depart_time[G_current_ac:]=list(map(lambda x:x+1,G_depart_time[G_current_ac:]))

            if I_current_ac<I_number:
                if i>=I_depart_time[I_current_ac]:
                    if len(lat_list)>=1:
                        try:
                            I_ind = ac_list.index(I_id)
                        except:
                            I_ind = -1
                        dep_dist=get_distance([lat_list[I_ind],lon_list[I_ind],alt_list[I_ind]],[40.749573,-73.901223,0])

                        if dep_dist>departure_safety_bound and \
                                Merge_check_block[int((Merge_time_I+I_depart_time[I_current_ac])/block_size)]<check_point_capacity:
                            bs.traf.cre(acid="I"+str(i), actype="ELE01",aclat=40.749573,aclon=-73.901223,acalt=0,acspd=3)
                            add_plane(i,"I")
                            I_id = "I"+str(i)
                            Merge_check_block[int((Merge_time_I+I_depart_time[I_current_ac])/block_size)]+=1
                        I_current_ac+=1
                    else:
                        I_depart_time[I_current_ac:]=list(map(lambda x:x+1,I_depart_time[I_current_ac:]))

        if first == 1:

            if G_current_ac<G_number:
                if i>=G_depart_time[G_current_ac]:
                    if len(lat_list)>=1:
                        try:
                            G_ind = ac_list.index(G_id)
                        except:
                            G_ind = -1
                        dep_dist=get_distance([lat_list[G_ind],lon_list[G_ind],alt_list[G_ind]],[40.6964385,-74.1231651,0])

                        if dep_dist>departure_safety_bound and \
                                Merge_check_block[int((Merge_time_G+G_depart_time[G_current_ac])/block_size)]<check_point_capacity and \
                                Cross_check_block[int((Cross_time_G+G_depart_time[G_current_ac])/block_size)]<check_point_capacity:
                            bs.traf.cre(acid="G"+str(i), actype="ELE01",aclat=40.6964385,aclon=-74.1231651,acalt=0,acspd=3)
                            add_plane(i,"G")
                            G_id = "G"+str(i)
                            Merge_check_block[int((Merge_time_G+G_depart_time[G_current_ac])/block_size)]+=1
                            Cross_check_block[int((Cross_time_G+G_depart_time[G_current_ac])/block_size)]+=1
                            G_current_ac+=1
                        else:
                            G_depart_time[G_current_ac:]=list(map(lambda x:x+1,G_depart_time[G_current_ac:]))


            if A_current_ac<A_number:
                if i>=A_depart_time[A_current_ac]:
                    if len(lat_list)>=1:
                        try:
                            A_ind = ac_list.index(A_id)
                        except:
                            A_ind = -1
                        dep_dist=get_distance([lat_list[A_ind],lon_list[A_ind],alt_list[A_ind]],[40.5959242,-74.0465984,0])

                        if dep_dist>departure_safety_bound and \
                                Cross_check_block[int((Cross_time_A+A_depart_time[A_current_ac])/block_size)]<check_point_capacity:
                            bs.traf.cre(acid="A"+str(i), actype="ELE01",aclat=40.5959242,aclon=-74.0465984,acalt=0,acspd=3)
                            add_plane(i,"A")
                            A_id = "A"+str(i)
                            Cross_check_block[int((Cross_time_A+A_depart_time[A_current_ac])/block_size)]+=1
                            A_current_ac+=1
                        else:
                            A_depart_time[A_current_ac:]=list(map(lambda x:x+1,A_depart_time[A_current_ac:]))

            if I_current_ac<I_number:
                if i>=I_depart_time[I_current_ac]:
                    if len(lat_list)>=1:
                        try:
                            I_ind = ac_list.index(I_id)
                        except:
                            I_ind = -1
                        dep_dist=get_distance([lat_list[I_ind],lon_list[I_ind],alt_list[I_ind]],[40.749573,-73.901223,0])

                        if dep_dist>departure_safety_bound and \
                                Merge_check_block[int((Merge_time_I+I_depart_time[I_current_ac])/block_size)]<check_point_capacity:
                            bs.traf.cre(acid="I"+str(i), actype="ELE01",aclat=40.749573,aclon=-73.901223,acalt=0,acspd=3)
                            add_plane(i,"I")
                            I_id = "I"+str(i)
                            Merge_check_block[int((Merge_time_I+I_depart_time[I_current_ac])/block_size)]+=1
                        I_current_ac+=1
                    else:
                        I_depart_time[I_current_ac:]=list(map(lambda x:x+1,I_depart_time[I_current_ac:]))

        if first == 2:

            if I_current_ac<I_number:
                if i>=I_depart_time[I_current_ac]:
                    if len(lat_list)>=1:
                        try:
                            I_ind = ac_list.index(I_id)
                        except:
                            I_ind = -1
                        dep_dist=get_distance([lat_list[I_ind],lon_list[I_ind],alt_list[I_ind]],[40.749573,-73.901223,0])

                        if dep_dist>departure_safety_bound and \
                                Merge_check_block[int((Merge_time_I+I_depart_time[I_current_ac])/block_size)]<check_point_capacity:
                            bs.traf.cre(acid="I"+str(i), actype="ELE01",aclat=40.749573,aclon=-73.901223,acalt=0,acspd=3)
                            add_plane(i,"I")
                            I_id = "I"+str(i)
                            Merge_check_block[int((Merge_time_I+I_depart_time[I_current_ac])/block_size)]+=1
                        I_current_ac+=1
                    else:
                        I_depart_time[I_current_ac:]=list(map(lambda x:x+1,I_depart_time[I_current_ac:]))

            if A_current_ac<A_number:
                if i>=A_depart_time[A_current_ac]:
                    if len(lat_list)>=1:
                        try:
                            A_ind = ac_list.index(A_id)
                        except:
                            A_ind = -1
                        dep_dist=get_distance([lat_list[A_ind],lon_list[A_ind],alt_list[A_ind]],[40.5959242,-74.0465984,0])

                        if dep_dist>departure_safety_bound and \
                                Cross_check_block[int((Cross_time_A+A_depart_time[A_current_ac])/block_size)]<check_point_capacity:
                            bs.traf.cre(acid="A"+str(i), actype="ELE01",aclat=40.5959242,aclon=-74.0465984,acalt=0,acspd=3)
                            add_plane(i,"A")
                            A_id = "A"+str(i)
                            Cross_check_block[int((Cross_time_A+A_depart_time[A_current_ac])/block_size)]+=1
                            A_current_ac+=1
                        else:
                            A_depart_time[A_current_ac:]=list(map(lambda x:x+1,A_depart_time[A_current_ac:]))

            if G_current_ac<G_number:
                if i>=G_depart_time[G_current_ac]:
                    if len(lat_list)>=1:
                        try:
                            G_ind = ac_list.index(G_id)
                        except:
                            G_ind = -1
                        dep_dist=get_distance([lat_list[G_ind],lon_list[G_ind],alt_list[G_ind]],[40.6964385,-74.1231651,0])

                        if dep_dist>departure_safety_bound and \
                                Merge_check_block[int((Merge_time_G+G_depart_time[G_current_ac])/block_size)]<check_point_capacity and \
                                Cross_check_block[int((Cross_time_G+G_depart_time[G_current_ac])/block_size)]<check_point_capacity:
                            bs.traf.cre(acid="G"+str(i), actype="ELE01",aclat=40.6964385,aclon=-74.1231651,acalt=0,acspd=3)
                            add_plane(i,"G")
                            G_id = "G"+str(i)
                            Merge_check_block[int((Merge_time_G+G_depart_time[G_current_ac])/block_size)]+=1
                            Cross_check_block[int((Cross_time_G+G_depart_time[G_current_ac])/block_size)]+=1
                            G_current_ac+=1
                        else:
                            G_depart_time[G_current_ac:]=list(map(lambda x:x+1,G_depart_time[G_current_ac:]))


        # ## in-air deconfliction ##
        if i%check_inv==0:
            if len(lat_list)<=1 or len(lat_list)<len(ac_list):
                continue
            else:
                ## For speed, input is kts, api output is m/s, the rate is 1.95
                # bs.stack.stack(f"SPD {ac_list[0]} {min(spd_list[0]*1.93+delta_v,max_speed)}")
                # f.write(f"00:00:{i}.00>SPD {ac_list[0]} {min(spd_list[0]*1.93+delta_v,max_speed)}\n")

                dist_list=[]
                ac_comb = list(itertools.combinations(ac_list, 2))

                for acs in ac_comb:
                    ac1 = ac_list.index(acs[0])
                    ac2 = ac_list.index(acs[1])
                    loc1=[lat_list[ac1],lon_list[ac1],alt_list[ac1]]
                    loc2=[lat_list[ac2],lon_list[ac2],alt_list[ac2]]
                    dist_list.append(get_distance(loc1,loc2))

                dist_list = np.array(dist_list)
                operate_comb_ids = np.where(dist_list < Warning_dist)
                # print(f"t:{i},ac_comb{ac_comb},dist_list{dist_list},operate_comb_ids{operate_comb_ids[0]}")
                ### All clear
                if len(operate_comb_ids[0])==0 and len(operate_dic)==0:
                    continue

                ### Release the operate ac if larger distance
                if len(operate_dic)>0:
                    pop_list = []
                    for operated_comb in operate_dic:
                        try:
                            ac1 = ac_list.index(operated_comb[0])
                            ac2 = ac_list.index(operated_comb[1])
                            loc1=[lat_list[ac1],lon_list[ac1],alt_list[ac1]]
                            loc2=[lat_list[ac2],lon_list[ac2],alt_list[ac2]]
                            operate_dist = get_distance(loc1,loc2)

                            ## seperation large, speed up
                            if operate_dist>SpeedUp_dist:
                                operate_ac = ac_list.index(operate_dic[operated_comb])
                                bs.stack.stack(f"SPD {ac_list[operate_ac]} {min(spd_list[operate_ac]*1.93+delta_v,max_speed)}")
                                f.write(f"00:00:{i}.00>SPD {ac_list[operate_ac]} {min(spd_list[operate_ac]*1.93+delta_v,max_speed)}\n")
                                if spd_list[operate_ac]*1.93+delta_v >= max_speed:
                                    pop_list.append(operated_comb)
                        except:
                            continue
                    for pop_item in pop_list:
                        operate_dic.pop(pop_item)

                ### Speed down the opearate ac
                if len(operate_comb_ids[0])>0:

                    for operate_comb_id in operate_comb_ids[0]:
                        dist = dist_list[operate_comb_id]
                        if dist>Warning_dist:
                            continue
                        operate_acs = ac_comb[operate_comb_id]
                        ## compute who is the following one
                        operate_ac1 = ac_list.index(operate_acs[0])
                        operate_ac2 = ac_list.index(operate_acs[1])
                        ac1_lon = lon_list[operate_ac1]
                        ac2_lon = lon_list[operate_ac2]
                        if ac1_lon >= ac2_lon:
                            operate_ac = operate_ac2
                            keep_ac = operate_ac1
                            operate_dic[operate_acs] = operate_acs[1]
                        else:
                            operate_ac = operate_ac1
                            keep_ac = operate_ac2
                            operate_dic[operate_acs] = operate_acs[0]

                        if dist<Warning_dist:  ## low seperation warning, speed down
                            bs.stack.stack(f"SPD {ac_list[operate_ac]} {min(max(spd_list[operate_ac]*1.93-delta_v,min_speed),max_speed)}")
                            f.write(f"00:00:{i}.00>SPD {ac_list[operate_ac]} {min(max(spd_list[operate_ac]*1.93-delta_v,min_speed),max_speed)}\n")

                        if dist<LOS_dist:  ## too low seperation, force hover (nearly)
                            LOS+=1
                            bs.stack.stack(f"SPD {ac_list[operate_ac]} {min_speed}")
                            f.write(f"00:00:{i}.00>SPD {ac_list[operate_ac]} {min_speed}\n")

                        if dist<NMAC_dist:  ## near in-air crash
                            NMAC+=1
                            # bs.stack.stack(f"DEL {ac_list[operate_ac]}")
                            # bs.stack.stack(f"DEL {ac_list[keep_ac]}")
                            # f.write(f"00:00:{i}.00>DEL {ac_list[operate_ac]}\n")
                            # f.write(f"00:00:{i}.00>DEL {ac_list[keep_ac]}\n")
    avg_delay = (np.mean(A_depart_time-A_depart_time_ori)+np.mean(G_depart_time-G_depart_time_ori)+
                 np.mean(I_depart_time-I_depart_time_ori))/3
    return [LOS,NMAC],avg_delay

safety,efficiency = run_sim(merge_capacity,check_block_size)

print(f"number of LOS:{safety[0]}")
print(f"number of MAC:{safety[1]}")
print(f"average delay:{round(efficiency)} s")

# plt.bar(range(len(ground_delay_list)), ground_delay_list)
# plt.title("Ground delay")
# plt.xlabel("Flight id")
# plt.ylabel("Delay time/s")
# plt.show()