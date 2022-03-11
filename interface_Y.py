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



f=open("scenario/interface_naive.scn","w")

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

def add_plane(id):
    speed_list=[30,31,32,33,34]
    # speed_list=[30]
    acid="A"+str(id)
    bs.stack.stack(f'ORIG {acid} N_1')
    bs.stack.stack(f'DEST {acid} N_4')
    bs.stack.stack(f'SPD {acid} 30')
    bs.stack.stack(f'ALT {acid} 400')
    bs.stack.stack(f'ADDWPT {acid} N_2, 400, 40')
    bs.stack.stack(f'ADDWPT {acid} N_3, 400, 40')
    bs.stack.stack(f'DUMPRTE {acid}')
    bs.stack.stack(f'VNAV {acid} ON')


    f.write(f"00:00:{id}.00>CRE {acid} ELE01 0 0 0 0\n")
    f.write(f"00:00:{id}.00>ORIG {acid} N_1\n")
    f.write(f"00:00:{id}.00>DEST {acid} N_4\n")
    f.write(f"00:00:{id}.00>SPD {acid} 30\n")
    f.write(f"00:00:{id}.00>ALT {acid} 400\n")
    f.write(f"00:00:{id}.00>ADDWPT {acid} N_2, 400, 40\n")
    f.write(f"00:00:{id}.00>ADDWPT {acid} N_3, 400, 40\n")
    f.write(f"00:00:{id}.00>VNAV {acid} ON\n")
    f.write(f"00:00:{id}.00>DUMPRTE {acid}\n")


    f.write("\n")
# set simulation time step, and enable fast-time running
bs.stack.stack('DT 1;FF')


# we'll run the simulation for up to 2000 seconds
t_max = 3000

ntraf = bs.traf.ntraf

n_steps = int(t_max + 1)
t = np.linspace(0, t_max, n_steps)

# Generate the demand based on exponential distribution, lambda-number of flight per second, lambda=0.1--flight interval=10s
ac_number=10
flight_interval=20
lambda_x = 1/flight_interval
ac_demand_interval = [int(expovariate(lambda_x)) for i in range(ac_number)]
ac_depart_time = np.cumsum(ac_demand_interval)
ori_depart_time=ac_depart_time.copy()
departure_safety_bound = 100

# bs.traf.cre(acid="A"+str(0), actype="ELE01",aclat=0,aclon=0.0,acalt=0,acspd=3)
bs.traf.cre(acid="A"+str(0), actype="ELE01",aclat=0.0, aclon=0.0)
add_plane(0)
MAC=0
LOS=0
current_ac=0
for i in range(1,n_steps):
    bs.sim.step()
    ac_list=bs.traf.id
    alt_list=bs.traf.alt
    lat_list=bs.traf.lat
    lon_list=bs.traf.lon
    spd_list=bs.traf.tas

    ac_comb = list(itertools.combinations(ac_list, 2))
    ##Check the nearest comb of the acs

    ## add aircraft based on demand##
    if current_ac<ac_number:
        if i>=ac_depart_time[current_ac]:
            if len(lat_list)>=1:
                dep_dist=get_distance([lat_list[-1],lon_list[-1],alt_list[-1]],[0,0,0])

                if dep_dist>departure_safety_bound:
                    bs.traf.cre(acid="A"+str(i), actype="ELE01",aclat=0,aclon=0.0,acalt=0,acspd=3)
                    add_plane(i)
                    current_ac+=1
                else:
                    ac_depart_time[current_ac:]=list(map(lambda x:x+1,ac_depart_time[current_ac:]))
                    # print(ac_depart_time)

    # ## in-air deconfliction ##
    if i%1==0:
        if len(lat_list)<=1:
            continue
        else:
            bs.stack.stack(f"SPD {ac_list[0]} 40")
            f.write(f"00:00:{i}.00>SPD {ac_list[0]} 40\n")

            for comb in ac_comb:
                ac1=ac_list.index(comb[0])
                ac2=ac_list.index(comb[1])
                loc1=[lat_list[ac1],lon_list[ac1],alt_list[ac1]]
                loc2=[lat_list[ac2],lon_list[ac2],alt_list[ac2]]
                dist=get_distance(loc1,loc2)
                if lon_list[ac1]>=lon_list[ac2]:
                    ac_spd_down=ac2
                    ac_other=ac1
                else:
                    ac_speed_down=ac1
                    ac_other=ac2
                if dist<600:  ## low seperation warning, speed down
                    bs.stack.stack(f"SPD {ac_list[ac_spd_down]} {max(spd_list[ac_spd_down]*2-5,3)}")
                    f.write(f"00:00:{i}.00>SPD {ac_list[ac_spd_down]} {max(spd_list[ac_spd_down]*2-5,3)}\n")
                if dist<100:  ## too low seperation, force hover (nearly)
                    LOS+=1
                    bs.stack.stack(f"SPD {ac_list[ac_spd_down]} 3")
                    f.write(f"00:00:{i}.00>SPD {ac_list[ac_spd_down]} 3\n")
                if dist>800: ## seperation large, speed up
                    bs.stack.stack(f"SPD {ac_list[ac_spd_down]} {min(spd_list[ac_spd_down]*2+5,45)}")
                    f.write(f"00:00:{i}.00>SPD {ac_list[ac_spd_down]} {min(spd_list[ac_spd_down]*2+5,45)}\n")
                if dist<10:  ## near in-air crash
                    MAC+=1
                    bs.stack.stack(f"DEL {ac_list[ac_spd_down]}")
                    bs.stack.stack(f"DEL {ac_list[ac_other]}")
                    f.write(f"00:00:{i}.00>DEL {ac_list[ac_spd_down]}\n")
                    f.write(f"00:00:{i}.00>DEL {ac_list[ac_other]}\n")

print(f"number of LOS:{LOS}")
print(f"number of MAC:{MAC*2}")
print(ac_depart_time)
print(ori_depart_time)
print(ac_depart_time-ori_depart_time)

ground_delay_list=ac_depart_time-ori_depart_time
plt.bar(range(len(ground_delay_list)), ground_delay_list)
plt.title("Ground delay")
plt.xlabel("Flight id")
plt.ylabel("Delay time/s")
plt.show()
