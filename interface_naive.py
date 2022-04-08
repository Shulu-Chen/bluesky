#!/usr/bin/python3
# coding: utf-8
'''
 @Time    : 2/22/2022 10:08 PM
 @Author  : Shulu Chen
 @FileName: interface_naive.py
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

def get_distance(location1,location2):
    #compute the distance of two aircraft, meters
    lat1=location1[0]
    lon1=location1[1]
    alt1=location1[2]
    lat2=location2[0]
    lon2=location2[1]
    alt2=location2[2]
    horizon_dist=geodesic((lat1,lon1), (lat2,lon2)).m
    # dist=sqrt(horizon_dist**2+(alt1-alt2)**2)
    dist=horizon_dist
    return horizon_dist

def generate_demand(flight_inv,ac_num):
    # Generate the demand based on exponential distribution,
    # lambda-number of flight per second, lambda=0.1--flight interval=10s
    # seed(10)
    lambda_x = 1/flight_inv
    ac_demand_interval = [int(expovariate(lambda_x)) for i in range(ac_num)]
    ac_depart_t = np.cumsum(ac_demand_interval)
    ori_depart_t=ac_depart_t.copy()
    return ac_depart_t,ori_depart_t

def init_bs():

    # initialize bluesky as non-networked simulation node
    bs.init('sim-detached')

    bs.stack.stack('CRELOG NAIVE 1')
    bs.stack.stack('NAIVE ADD id,lat, lon, alt, tas, vs ')
    bs.stack.stack('NAIVE ON 1  ')
    # bs.stack.stack('ASAS ON')
    bs.stack.stack('TAXI OFF 4')
    f.write("00:00:00.00>CRELOG NAIVE_gui 1\n")
    f.write("00:00:00.00>NAIVE_gui ADD id,lat, lon, alt, tas, vs\n")
    f.write("00:00:00.00>NAIVE_gui ON 1\n")
    f.write("00:00:00.00>TRAILS ON \n")
    f.write("00:00:00.00>TAXI OFF 4\n")
    # f.write("0:00:00.00>ASAS ON \n")
    f.write("0:00:00.00>PAN 0,0.2 \n")
    f.write("0:00:00.00>ZOOM 2 \n")
    # f.write("0:00:00.00>FF \n")
    f.write("\n")

    # set simulation time step, and enable fast-time running
    bs.stack.stack('DT 1;FF')
    bs.traf.cre(acid="A"+str(0), actype="ELE01",aclat=0.0, aclon=0.0)
    add_plane(0)

def add_plane(id):
    speed_list=[30,32,34,36,38]
    # speed_list=[30]
    acid="A"+str(id)
    bs.stack.stack(f'ORIG {acid} N_1')
    bs.stack.stack(f'DEST {acid} N_4')
    bs.stack.stack(f'SPD {acid} 35')
    bs.stack.stack(f'ALT {acid} 400')

    f.write(f"00:00:{id}.00>CRE {acid} ELE01 0 0.0 0 0\n")
    f.write(f"00:00:{id}.00>ORIG {acid} N_1\n")
    f.write(f"00:00:{id}.00>DEST {acid} N_4\n")
    f.write(f"00:00:{id}.00>SPD {acid} 35\n")
    f.write(f"00:00:{id}.00>ALT {acid} 400\n")

    speed=sample(speed_list,1)[0]
    bs.stack.stack(f'ADDWPT {acid} N_2, 400, {speed}')
    f.write(f"00:00:{id}.00>ADDWPT {acid} N_2, 400, {speed}\n")

    speed=sample(speed_list,1)[0]
    bs.stack.stack(f'ADDWPT {acid} N_3, 400, {speed}')
    f.write(f"00:00:{id}.00>ADDWPT {acid} N_3, 400, {speed}\n")

    bs.stack.stack(f'DUMPRTE {acid}')
    bs.stack.stack(f'VNAV {acid} ON')

    f.write(f"00:00:{id}.00>VNAV {acid} ON\n")
    f.write(f"00:00:{id}.00>DUMPRTE {acid}\n")

    f.write("\n")


t_max = 3000
n_steps = int(t_max + 1)
ac_number = 9
flight_interval = 50
departure_safety_bound = 150
max_speed = 40
min_speed = 3
delta_v = 5
NMAC = 0
LOS = 0
current_ac = 0
check_inv = 5
NMAC_dist = 10
LOS_dist = 100
Warning_dist = 600
SpeedUp_dist = 800
operate_dic = {}

f=open("scenario/interface_naive.scn","w")
init_bs()
ac_depart_time,ori_depart_time = generate_demand(flight_interval,ac_number)


for i in tqdm(range(1,n_steps)):
# for i in range(1,n_steps):
    bs.sim.step()
    ac_list=bs.traf.id
    alt_list=bs.traf.alt
    lat_list=bs.traf.lat
    lon_list=bs.traf.lon
    spd_list=bs.traf.tas

    ## add aircraft based on demand##
    if current_ac<ac_number:
        if i>=ac_depart_time[current_ac]:
            if len(lat_list)>=1:
                dep_dist=get_distance([lat_list[-1],lon_list[-1],alt_list[-1]],[0,0,0])

                if dep_dist>departure_safety_bound:
                    bs.traf.cre(acid="A"+str(i), actype="ELE01",aclat=0.0,aclon=0.0,acalt=0,acspd=3)
                    add_plane(i)
                    current_ac+=1
                else:
                    ac_depart_time[current_ac:]=list(map(lambda x:x+1,ac_depart_time[current_ac:]))



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
                    if abs(ac1_lon) >= abs(ac2_lon):
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

print(f"number of LOS:{LOS}")
print(f"number of MAC:{NMAC}")
print(ac_depart_time)
print(ori_depart_time)
print(ac_depart_time-ori_depart_time)

# ground_delay_list=ac_depart_time-ori_depart_time
# plt.bar(range(len(ground_delay_list)), ground_delay_list)
# plt.title("Ground delay")
# plt.xlabel("Flight id")
# plt.ylabel("Delay time/s")
# plt.show()