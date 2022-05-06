#!/usr/bin/python3
# coding: utf-8
'''
 @Time    : 4/28/2022 10:50 PM
 @Author  : Shulu Chen
 @FileName: exp5.py
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

    bs.stack.stack('TAXI OFF 4')

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



        v = random.choice(speed_list)
        bs.stack.stack(f'ADDWPT {acid} L_5, 400, {v}')

        v = random.choice(speed_list)
        bs.stack.stack(f'ADDWPT {acid} L_4, 400, {v}')

        v = random.choice(speed_list)
        bs.stack.stack(f'ADDWPT {acid} G_4, 400, {v}')

        v = random.choice(speed_list)
        bs.stack.stack(f'ADDWPT {acid} L_2, 400, {v}')

        v = random.choice(speed_list)
        bs.stack.stack(f'ADDWPT {acid} A_1, 400, {v}')

        v = random.choice(speed_list)
        bs.stack.stack(f'ADDWPT {acid} A_2, 400, {v}')
        v = random.choice(speed_list)
        bs.stack.stack(f'ADDWPT {acid} A_3, 400, {v}')
        v = random.choice(speed_list)
        bs.stack.stack(f'ADDWPT {acid} A_4, 400, {v}')

        v = random.choice(speed_list)
        bs.stack.stack(f'ADDWPT {acid} A_5, 400, {v}')

        v = random.choice(speed_list)
        bs.stack.stack(f'ADDWPT {acid} A_6, 400, {v}')

        v = random.choice(speed_list)
        bs.stack.stack(f'ADDWPT {acid} A_7, 400, {v}')

        v = random.choice(speed_list)
        bs.stack.stack(f'ADDWPT {acid} A_8, 400, {v}')


        bs.stack.stack(f'DUMPRTE {acid}')
        bs.stack.stack(f'VNAV {acid} ON')


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
        bs.stack.stack(f'ADDWPT {acid} G_1, 400, {v}')
        bs.stack.stack(f'ADDWPT {acid} H_2, 400, {v}')
        bs.stack.stack(f'ADDWPT {acid} H_4, 400, {v}')
        bs.stack.stack(f'ADDWPT {acid} H_7, 400, {v}')
        bs.stack.stack(f'DUMPRTE {acid}')
        bs.stack.stack(f'VNAV {acid} ON')

t_max = 6000                   #seconds
n_steps = int(t_max + 1)
AC_nums = [10,10,30]
AC_intervals = [60,60,60]         #seconds
departure_safety_bound = 150   #seconds
max_speed = 40                 #kts
min_speed = 3                  #kts
delta_v = 5                    #kts
check_inv = 1                #second
control_inv = 10
NMAC_dist = 10                 #meters
LOS_dist = 100                 #meters
Warning_dist = 600             #meters
SpeedUp_dist = 800             #meters


Cross_time_A = 576             #seconds
Cross_time_G = 497             #seconds
Merge_time_G = 1261            #seconds
Merge_time_I = 448
type = int(sys.argv[1])
if type = 0:
    merge_capacity = 1
    check_block_size = 70         #seconds
elif type = 1:
    merge_capacity = 2
    check_block_size = 140         #seconds
elif type = 2:
    merge_capacity = 50
    check_block_size = 140         #seconds
Cross_check_block = np.zeros(round(t_max*2/check_block_size))
Merge_check_block = np.zeros(round(t_max*2/check_block_size))


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
        if i%control_inv==0:
            if len(lat_list)<=1 or len(lat_list)<len(ac_list):
                continue
            else:
                ## For speed, input is kts, api output is m/s, the rate is 1.95

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

    avg_delay = (np.mean(A_depart_time-A_depart_time_ori)+np.mean(G_depart_time-G_depart_time_ori)+
                 np.mean(I_depart_time-I_depart_time_ori))/3
    return [LOS,NMAC],avg_delay

safety,efficiency = run_sim(merge_capacity,check_block_size)

print(f"number of LOS:{safety[0]}")
print(f"number of MAC:{safety[1]}")
print(f"average delay:{round(efficiency)} s")
print(f"Type={type}")
g=open("result\\NYC data.txt","a")
if type = 0:
    g.write(f"{safety[0]},A,LOS_high\n")
    g.write(f"{safety[1]},A,NMAC_high\n")
    g.write(f"{round(efficiency)},A,Delay)_high\n")
if type = 1:
    g.write(f"{safety[0]},A,LOS_low\n")
    g.write(f"{safety[1]},A,NMAC_low\n")
    g.write(f"{round(efficiency)},A,Delay_low\n")
if type = 2:
    g.write(f"{safety[0]},A,LOS_no\n")
    g.write(f"{safety[1]},A,NMAC_no\n")
    g.write(f"{round(efficiency)},A,Delay_no\n")