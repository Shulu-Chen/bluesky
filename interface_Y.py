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
from random import expovariate
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

    bs.stack.stack('CRELOG Y 1')
    bs.stack.stack('Y ADD id,lat, lon, alt, tas, vs ')
    bs.stack.stack('Y ON 1  ')
    # bs.stack.stack('ASAS ON')
    bs.stack.stack('TAXI OFF 4')
    f.write("00:00:00.00>CRELOG Y_gui 1\n")
    f.write("00:00:00.00>Y_gui ADD id,lat, lon, alt, tas, vs\n")
    f.write("00:00:00.00>Y_gui ON 1\n")
    f.write("00:00:00.00>TRAILS ON \n")
    f.write("00:00:00.00>TAXI OFF 4\n")
    # f.write("0:00:00.00>ASAS ON \n")
    f.write("0:00:00.00>PAN 0,0.2 \n")
    f.write("0:00:00.00>ZOOM 2 \n")
    # f.write("0:00:00.00>FF \n")
    f.write("\n")

    # set simulation time step, and enable fast-time running
    bs.stack.stack('DT 1;FF')
    bs.traf.cre(acid="A"+str(0), actype="ELE01",aclat=0.1, aclon=-0.1)
    add_plane(0,"U")


def add_plane(id,type):
    speed_list=[30,32,34,36,38]
    acid="A"+str(id)
    if type=="U":
        bs.stack.stack(f'ORIG {acid} N_7')
        bs.stack.stack(f'DEST {acid} N_4')

        bs.stack.stack(f'SPD {acid} 30')
        bs.stack.stack(f'ALT {acid} 400')
        bs.stack.stack(f'ADDWPT {acid} N_1, 400, 40')
        bs.stack.stack(f'ADDWPT {acid} N_2, 400, 40')
        bs.stack.stack(f'ADDWPT {acid} N_3, 400, 40')
        bs.stack.stack(f'DUMPRTE {acid}')
        bs.stack.stack(f'VNAV {acid} ON')


        f.write(f"00:00:{id}.00>CRE {acid} ELE01 0.1 -0.1 0 0\n")
        f.write(f"00:00:{id}.00>ORIG {acid} N_7\n")
        f.write(f"00:00:{id}.00>DEST {acid} N_4\n")
        f.write(f"00:00:{id}.00>SPD {acid} 30\n")
        f.write(f"00:00:{id}.00>ALT {acid} 400\n")
        f.write(f"00:00:{id}.00>ADDWPT {acid} N_1, 400, 40\n")
        f.write(f"00:00:{id}.00>ADDWPT {acid} N_2, 400, 40\n")
        f.write(f"00:00:{id}.00>ADDWPT {acid} N_3, 400, 40\n")
        f.write(f"00:00:{id}.00>VNAV {acid} ON\n")
        f.write(f"00:00:{id}.00>DUMPRTE {acid}\n")

    if type=="D":
        bs.stack.stack(f'ORIG {acid} N_9')
        bs.stack.stack(f'DEST {acid} N_4')
        bs.stack.stack(f'SPD {acid} 30')
        bs.stack.stack(f'ALT {acid} 400')
        bs.stack.stack(f'ADDWPT {acid} N_1, 400, 40')
        bs.stack.stack(f'ADDWPT {acid} N_2, 400, 40')
        bs.stack.stack(f'ADDWPT {acid} N_3, 400, 40')
        bs.stack.stack(f'DUMPRTE {acid}')
        bs.stack.stack(f'VNAV {acid} ON')


        f.write(f"00:00:{id}.00>CRE {acid} ELE01 -0.1 -0.1 0 0\n")
        f.write(f"00:00:{id}.00>ORIG {acid} N_9\n")
        f.write(f"00:00:{id}.00>DEST {acid} N_4\n")
        f.write(f"00:00:{id}.00>SPD {acid} 30\n")
        f.write(f"00:00:{id}.00>ALT {acid} 400\n")
        f.write(f"00:00:{id}.00>ADDWPT {acid} N_1, 400, 40\n")
        f.write(f"00:00:{id}.00>ADDWPT {acid} N_2, 400, 40\n")
        f.write(f"00:00:{id}.00>ADDWPT {acid} N_3, 400, 40\n")
        f.write(f"00:00:{id}.00>VNAV {acid} ON\n")
        f.write(f"00:00:{id}.00>DUMPRTE {acid}\n")

    f.write("\n")

# we'll run the simulation for up to 2000 seconds
t_max = 3000
n_steps = int(t_max + 1)
U_number = 10
U_flight_interval = 140
D_number = 10
D_flight_interval = 140
departure_safety_bound = 150
max_speed = 40
min_speed = 3
delta_v = 5
NMAC = 0
LOS = 0
U_current_ac=0
D_current_ac=0
check_inv = 10
NMAC_dist = 10
LOS_dist = 100
Warning_dist = 600
SpeedUp_dist = 800
merge_cap = 3
merge_time = 1015  #seconds
block_size = 20    #seconds
check_block = np.zeros(round(t_max*2/block_size))
safety_bound = 5

operate_dic = {}

f=open("scenario/interface_Y.scn","w")
init_bs()
check_block[int(merge_time/block_size)]+=1
U_depart_time, U_depart_time_ori = generate_interval(U_flight_interval,U_number)
D_depart_time, D_depart_time_ori = generate_interval(D_flight_interval,D_number)

for i in tqdm(range(1,n_steps)):
    bs.sim.step()
    ac_list=bs.traf.id
    alt_list=bs.traf.alt
    lat_list=bs.traf.lat
    lon_list=bs.traf.lon
    spd_list=bs.traf.tas


    ## add aircraft based on demand##
    if U_current_ac<U_number:
        if i>=U_depart_time[U_current_ac]:
            if len(lat_list)>=1:
                try:
                    U_ind = ac_list.index(U_id)
                except:
                    U_ind = -1
                dep_dist=get_distance([lat_list[U_ind],lon_list[U_ind],alt_list[U_ind]],[0.1,-0.1,0])

                if dep_dist>departure_safety_bound and \
                        check_block[int((merge_time+U_depart_time[U_current_ac])/block_size)]<=safety_bound:
                    bs.traf.cre(acid="A"+str(i), actype="ELE01",aclat=0.1,aclon=-0.1,acalt=0,acspd=3)
                    add_plane(i,"U")
                    U_id = "A"+str(i)
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
                        check_block[int((merge_time+D_depart_time[D_current_ac])/block_size)]<=safety_bound:
                    bs.traf.cre(acid="A"+str(i), actype="ELE01",aclat=-0.1,aclon=-0.1,acalt=0,acspd=3)
                    add_plane(i,"D")
                    D_id = "A"+str(i)
                    check_block[int((merge_time+D_depart_time[D_current_ac])/block_size)]+=1
                    D_current_ac+=1
                else:
                    D_depart_time[D_current_ac:]=list(map(lambda x:x+1,D_depart_time[D_current_ac:]))

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

print(f"number of LOS:{LOS}")
print(f"number of MAC:{NMAC}")


# ground_delay_list=ac_depart_time-ori_depart_time
# plt.bar(range(len(ground_delay_list)), ground_delay_list)
# plt.title("Ground delay")
# plt.xlabel("Flight id")
# plt.ylabel("Delay time/s")
# plt.show()