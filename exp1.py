#!/usr/bin/python3
# coding: utf-8
'''
 @Time    : 4/28/2022 6:47 PM
 @Author  : Shulu Chen
 @FileName: exp1.py
 @Software: PyCharm
'''
import numpy as np
import random
import bluesky as bs
from bluesky.simulation import ScreenIO
from geopy.distance import geodesic
from math import radians, cos, sin, asin, sqrt
import matplotlib.pyplot as plt
from random import expovariate,seed
import itertools
from tqdm import tqdm
import sys

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
    # seed(100)
    lambda_x = 1/interval
    ac_demand_interval = [int(expovariate(lambda_x)) for i in range(number)]
    depart_time = np.cumsum(ac_demand_interval)
    depart_time_ori = depart_time.copy()
    return depart_time,depart_time_ori

def init_bs():

    bs.stack.stack('TAXI OFF 4')

    # set simulation time step, and enable fast-time running

    bs.stack.stack('DT 1;FF')
    bs.traf.cre(acid="U"+str(0), actype="ELE01",aclat=0.1, aclon=-0.1)
    add_plane(0,"U")


def add_plane(id,type):
    speed_list=[30,31,32,33,34]

    if type=="U":

        acid="U"+str(id)

        bs.stack.stack(f'ORIG {acid} N_7')
        bs.stack.stack(f'DEST {acid} N_4')

        v = random.choice(speed_list)
        bs.stack.stack(f'SPD {acid} {v}')
        bs.stack.stack(f'ALT {acid} 400')

        v = random.choice(speed_list)
        bs.stack.stack(f'ADDWPT {acid} N_1, 400, {v}')

        v = random.choice(speed_list)
        bs.stack.stack(f'ADDWPT {acid} N_2, 400, {v}')

        v = random.choice(speed_list)
        bs.stack.stack(f'ADDWPT {acid} N_3, 400, {v}')
        bs.stack.stack(f'VNAV {acid} ON')

    if type=="D":

        acid="D"+str(id)

        bs.stack.stack(f'ORIG {acid} N_9')
        bs.stack.stack(f'DEST {acid} N_4')

        v = random.choice(speed_list)
        bs.stack.stack(f'SPD {acid} {v}')

        bs.stack.stack(f'ALT {acid} 400')

        v = random.choice(speed_list)
        bs.stack.stack(f'ADDWPT {acid} N_1, 400, {v}')

        v = random.choice(speed_list)
        bs.stack.stack(f'ADDWPT {acid} N_2, 400, {v}')

        v = random.choice(speed_list)
        bs.stack.stack(f'ADDWPT {acid} N_3, 400, {v}')


        bs.stack.stack(f'VNAV {acid} ON')



t_max = 3000                   #second
n_steps = int(t_max + 1)
# inv = int(sys.argv[1])
inv = 60
AC_nums = [10,10]
# AC_intervals = [60,60]         #second
AC_intervals =[inv,inv]
departure_safety_bound = 150   #second
max_speed = 40                 #kts
min_speed = 3                  #kts
delta_v = 5                    #kts
check_inv = 1                  #second
control_inv = 10               #second
NMAC_dist = 10                 #meter
LOS_dist = 100                 #meter
Warning_dist = 600             #meter
SpeedUp_dist = 800
merge_capacity = int(sys.argv[1])
merge_time = 1015              #second
check_block_size =  100        #second


bs.init('sim-detached')

def run_sim(check_point_capacity,block_size,number_list=AC_nums,interval_list=AC_intervals):
    init_bs()
    check_block = np.zeros(round(t_max*2/block_size))
    check_block[int(merge_time/block_size)]+=1

    NMAC = 0
    LOS = 0
    U_current_ac=0
    D_current_ac=0
    U_number = number_list[0]
    D_number = number_list[1]
    U_flight_interval = interval_list[0]
    D_flight_interval = interval_list[1]
    U_depart_time, U_depart_time_ori = generate_interval(U_flight_interval,U_number)
    D_depart_time, D_depart_time_ori = generate_interval(D_flight_interval,D_number)
    operate_dic = {}

    for i in tqdm(range(1,n_steps)):
        bs.sim.step()
        ac_list=bs.traf.id
        alt_list=bs.traf.alt
        lat_list=bs.traf.lat
        lon_list=bs.traf.lon
        spd_list=bs.traf.tas

        ## add aircraft based on demand##
        U_first = random.choice([True,False])
        if U_first:
            if U_current_ac<U_number:
                if i>=U_depart_time[U_current_ac]:
                    if len(lat_list)>=1:
                        try:
                            U_ind = ac_list.index(U_id)
                        except:
                            U_ind = -1
                        dep_dist=get_distance([lat_list[U_ind],lon_list[U_ind],alt_list[U_ind]],[0.1,-0.1,0])

                        if dep_dist>departure_safety_bound and \
                                check_block[int((merge_time+U_depart_time[U_current_ac])/block_size)]<check_point_capacity:
                            bs.traf.cre(acid="U"+str(i), actype="ELE01",aclat=0.1,aclon=-0.1,acalt=0,acspd=3)
                            add_plane(i,"U")
                            U_id = "U"+str(i)
                            check_block[int((merge_time+U_depart_time[U_current_ac])/block_size)]+=1
                            U_current_ac+=1
                        else:
                            U_depart_time[U_current_ac:]=list(map(lambda x:x+1,U_depart_time[U_current_ac:]))

            if D_current_ac<D_number:
                if i>=D_depart_time[D_current_ac]:
                    if len(lat_list)>=1:
                        try:
                            D_ind = ac_list.index(D_id)
                        except:
                            D_ind = -1
                        dep_dist=get_distance([lat_list[D_ind],lon_list[D_ind],alt_list[D_ind]],[-0.1,-0.1,0])
                        if dep_dist>departure_safety_bound and \
                                check_block[int((merge_time+D_depart_time[D_current_ac])/block_size)]<check_point_capacity:
                            bs.traf.cre(acid="D"+str(i), actype="ELE01",aclat=-0.1,aclon=-0.1,acalt=0,acspd=3)
                            add_plane(i,"D")
                            D_id = "D"+str(i)
                            check_block[int((merge_time+D_depart_time[D_current_ac])/block_size)]+=1
                            D_current_ac+=1
                        else:
                            D_depart_time[D_current_ac:]=list(map(lambda x:x+1,D_depart_time[D_current_ac:]))
        else:
            if D_current_ac<D_number:
                if i>=D_depart_time[D_current_ac]:
                    if len(lat_list)>=1:
                        try:
                            D_ind = ac_list.index(D_id)
                        except:
                            D_ind = -1
                        dep_dist=get_distance([lat_list[D_ind],lon_list[D_ind],alt_list[D_ind]],[-0.1,-0.1,0])
                        if dep_dist>departure_safety_bound and \
                                check_block[int((merge_time+D_depart_time[D_current_ac])/block_size)]<check_point_capacity:
                            bs.traf.cre(acid="D"+str(i), actype="ELE01",aclat=-0.1,aclon=-0.1,acalt=0,acspd=3)
                            add_plane(i,"D")
                            D_id = "D"+str(i)
                            check_block[int((merge_time+D_depart_time[D_current_ac])/block_size)]+=1
                            D_current_ac+=1
                        else:
                            D_depart_time[D_current_ac:]=list(map(lambda x:x+1,D_depart_time[D_current_ac:]))

            if U_current_ac<U_number:
                if i>=U_depart_time[U_current_ac]:
                    if len(lat_list)>=1:
                        try:
                            U_ind = ac_list.index(U_id)
                        except:
                            U_ind = -1
                        dep_dist=get_distance([lat_list[U_ind],lon_list[U_ind],alt_list[U_ind]],[0.1,-0.1,0])

                        if dep_dist>departure_safety_bound and \
                                check_block[int((merge_time+U_depart_time[U_current_ac])/block_size)]<check_point_capacity:
                            bs.traf.cre(acid="U"+str(i), actype="ELE01",aclat=0.1,aclon=-0.1,acalt=0,acspd=3)
                            add_plane(i,"U")
                            U_id = "U"+str(i)
                            check_block[int((merge_time+U_depart_time[U_current_ac])/block_size)]+=1
                            U_current_ac+=1
                        else:
                            U_depart_time[U_current_ac:]=list(map(lambda x:x+1,U_depart_time[U_current_ac:]))

        # ## in-air deconfliction ##
        if i%control_inv==0:
            if len(lat_list)<=1 or len(lat_list)<len(ac_list):
                continue
            else:

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


                        if dist<LOS_dist:  ## too low seperation, force hover (nearly)
                            # LOS+=1
                            bs.stack.stack(f"SPD {ac_list[operate_ac]} {min_speed}")


        if i%check_inv==0:
            if len(lat_list)<=1 or len(lat_list)<len(ac_list):
                continue
            else:

                dist_list=[]
                ac_comb = list(itertools.combinations(ac_list, 2))

                for acs in ac_comb:
                    ac1 = ac_list.index(acs[0])
                    ac2 = ac_list.index(acs[1])
                    loc1=[lat_list[ac1],lon_list[ac1],alt_list[ac1]]
                    loc2=[lat_list[ac2],lon_list[ac2],alt_list[ac2]]
                    dist_list.append(get_distance(loc1,loc2))

                dist_list = np.array(dist_list)
                LOS_temp = np.sum(dist_list < LOS_dist)
                NMAC_temp = np.sum(dist_list < NMAC_dist)
                LOS += (LOS_temp-NMAC_temp)
                NMAC += NMAC_temp

    return [LOS,NMAC],(np.mean(U_depart_time-U_depart_time_ori)+np.mean(D_depart_time-D_depart_time_ori))/2


safety,efficiency = run_sim(merge_capacity,check_block_size)
print("*******************************")
print(f"number of LOS:{safety[0]}")
print(f"number of MAC:{safety[1]}")
print(f"average delay:{round(efficiency)} s")
print("Capacity=",merge_capacity)
print("*******************************")
g=open("Capacity_data.txt","a")
g.write(f"{safety[0]},{merge_capacity},LOS\n")
g.write(f"{safety[1]},{merge_capacity},NMAC\n")
g.write(f"{round(efficiency)},{merge_capacity},Ground Delay\n")