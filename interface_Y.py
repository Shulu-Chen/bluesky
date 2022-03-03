#!/usr/bin/python3
# coding: utf-8
'''
 @Time    : 2/25/2022 3:06 AM
 @Author  : Shulu Chen
 @FileName: interface_Y.py
 @Software: PyCharm
'''
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



f=open("scenario/interface_naive_Y.scn","w")

# initialize bluesky as non-networked simulation node
bs.init('sim-detached')

bs.stack.stack('CRELOG NAIVE_Y 1')
bs.stack.stack('NAIVE_Y ADD id,lat, lon, alt, tas, vs ')
bs.stack.stack('NAIVE_Y ON 1  ')
# bs.stack.stack('ASAS ON')
bs.stack.stack('TAXI OFF 4')
f.write("00:00:00.00>CRELOG NAIVE_Y_gui 1\n")
f.write("00:00:00.00>NAIVE_Y_gui ADD id,lat, lon, alt, tas, vs\n")
f.write("00:00:00.00>NAIVE_Y_gui ON 1\n")
f.write("00:00:00.00>TRAILS ON \n")
f.write("00:00:00.00>TAXI OFF 4\n")
# f.write("0:00:00.00>ASAS ON \n")
f.write("0:00:00.00>PAN 0,0.2 \n")
f.write("0:00:00.00>ZOOM 2 \n")
# f.write("0:00:00.00>FF \n")

f.write("\n")

def add_plane(id,orign):
    speed_list=[30,31,32,33,34]
    # speed_list=[30]
    acid="A"+str(id)
    if orign==1:
        bs.stack.stack(f'ORIG {acid} N_6')
        bs.stack.stack(f'DEST {acid} N_5')
        bs.stack.stack(f'SPD {acid} 30')
        bs.stack.stack(f'ALT {acid} 400')
        bs.stack.stack(f'ADDWPT {acid} N_7, 400, 40')
        bs.stack.stack(f'ADDWPT {acid} N_1, 400, 40')
        bs.stack.stack(f'ADDWPT {acid} N_2, 400, 40')
        bs.stack.stack(f'ADDWPT {acid} N_3, 400, 40')
        bs.stack.stack(f'ADDWPT {acid} N_4, 400, 40')
        bs.stack.stack(f'DUMPRTE {acid}')
        bs.stack.stack(f'VNAV {acid} ON')


        f.write(f"00:00:{id}.00>CRE {acid} ELE01 N_6 0 0\n")
        f.write(f"00:00:{id}.00>ORIG {acid} N_6\n")
        f.write(f"00:00:{id}.00>DEST {acid} N_5\n")
        f.write(f"00:00:{id}.00>SPD {acid} 30\n")
        f.write(f"00:00:{id}.00>ALT {acid} 400\n")
        f.write(f"00:00:{id}.00>ADDWPT {acid} N_7, 400, 40\n")
        f.write(f"00:00:{id}.00>ADDWPT {acid} N_1, 400, 40\n")
        f.write(f"00:00:{id}.00>ADDWPT {acid} N_2, 400, 40\n")
        f.write(f"00:00:{id}.00>ADDWPT {acid} N_3, 400, 40\n")
        f.write(f"00:00:{id}.00>ADDWPT {acid} N_4, 400, 40\n")
        f.write(f"00:00:{id}.00>VNAV {acid} ON\n")
        f.write(f"00:00:{id}.00>DUMPRTE {acid}\n")
    else:
        bs.stack.stack(f'ORIG {acid} N_8')
        bs.stack.stack(f'DEST {acid} N_5')
        bs.stack.stack(f'SPD {acid} 30')
        bs.stack.stack(f'ALT {acid} 400')
        bs.stack.stack(f'ADDWPT {acid} N_9, 400, 40')
        bs.stack.stack(f'ADDWPT {acid} N_1, 400, 40')
        bs.stack.stack(f'ADDWPT {acid} N_2, 400, 40')
        bs.stack.stack(f'ADDWPT {acid} N_3, 400, 40')
        bs.stack.stack(f'ADDWPT {acid} N_4, 400, 40')
        bs.stack.stack(f'DUMPRTE {acid}')
        bs.stack.stack(f'VNAV {acid} ON')


        f.write(f"00:00:{id}.00>CRE {acid} ELE01 N_8 0 0\n")
        f.write(f"00:00:{id}.00>ORIG {acid} N_8\n")
        f.write(f"00:00:{id}.00>DEST {acid} N_5\n")
        f.write(f"00:00:{id}.00>SPD {acid} 30\n")
        f.write(f"00:00:{id}.00>ALT {acid} 400\n")
        f.write(f"00:00:{id}.00>ADDWPT {acid} N_9, 400, 40\n")
        f.write(f"00:00:{id}.00>ADDWPT {acid} N_1, 400, 40\n")
        f.write(f"00:00:{id}.00>ADDWPT {acid} N_2, 400, 40\n")
        f.write(f"00:00:{id}.00>ADDWPT {acid} N_3, 400, 40\n")
        f.write(f"00:00:{id}.00>ADDWPT {acid} N_4, 400, 40\n")
        f.write(f"00:00:{id}.00>VNAV {acid} ON\n")
        f.write(f"00:00:{id}.00>DUMPRTE {acid}\n")

    f.write("\n")
# set simulation time step, and enable fast-time running
bs.stack.stack('DT 1;FF')


# we'll run the simulation for up to 2000 seconds
t_max = 2000
interval=40
ntraf = bs.traf.ntraf

n_steps = int(t_max + 1)
t = np.linspace(0, t_max, n_steps)

# bs.traf.cre(acid="A"+str(0), actype="ELE01",aclat=0,aclon=0.0,acalt=0,acspd=3)
bs.traf.cre(acid="A"+str(0), actype="ELE01",aclat=0.2, aclon=-0.2)
add_plane(0,1)

for i in range(1,n_steps):
    bs.sim.step()
    ## add aircraft ##
    if i%interval==0:
        # if sample([True,False],1)[0]:
        orign=sample([-1,1],1)[0]
        bs.traf.cre(acid="A"+str(i), actype="ELE01",aclat=orign*0.2,aclon=-0.2,acalt=0,acspd=3)
        add_plane(i,orign)

    # ## in-air deconfliction ##
    # if i%1==0:
    #     ac_list=bs.traf.id
    #     alt_list=bs.traf.alt
    #
    #     lat_list=bs.traf.lat
    #     lon_list=bs.traf.lon
    #     spd_list=bs.traf.tas
    #     if len(ac_list)<=1:
    #         continue
    #     else:
    #         bs.stack.stack(f"SPD {ac_list[0]} 35")
    #         f.write(f"00:00:{i}.00>SPD {ac_list[0]} 35\n")
    #         for j in range(len(ac_list)-1):
    #             loc1=[lat_list[j],lon_list[j],alt_list[j]]
    #             loc2=[lat_list[j+1],lon_list[j+1],alt_list[j+1]]
    #             dist=get_distance(loc1,loc2)
    #             if dist<600:  ## low seperation warning, speed down
    #                 bs.stack.stack(f"SPD {ac_list[j+1]} {max(spd_list[j+1]*2-5,3)}")
    #                 f.write(f"00:00:{i}.00>SPD {ac_list[j+1]} {max(spd_list[j+1]*2-5,3)}\n")
    #             if dist<100:  ## too low seperation, force hover (nearly)
    #                 bs.stack.stack(f"SPD {ac_list[j+1]} 3")
    #                 f.write(f"00:00:{i}.00>SPD {ac_list[j+1]} 3\n")
    #             if dist>800: ## seperation large, speed up
    #                 bs.stack.stack(f"SPD {ac_list[j+1]} {min(spd_list[j+1]*2+5,50)}")
    #                 f.write(f"00:00:{i}.00>SPD {ac_list[j+1]} {min(spd_list[j+1]*2+5,50)}\n")
