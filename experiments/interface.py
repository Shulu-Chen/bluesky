#!/usr/bin/python3
# coding: utf-8
'''
 @Time    : 12/16/2021 12:43 AM
 @Author  : Shulu Chen
 @FileName: interface.py
 @Software: PyCharm
'''
import numpy as np
from random import sample
import bluesky as bs
from bluesky.simulation import ScreenIO
from geopy.distance import geodesic
from math import radians, cos, sin, asin, sqrt

class ScreenDummy(ScreenIO):
    """
    Dummy class for the screen. Inherits from ScreenIO to make sure all the
    necessary methods are there. This class is there to reimplement the echo
    method so that console messages are printed.
    """
    def echo(self, text='', flags=0):
        """Just print echo messages"""
        print("BlueSky console:", text)

# initialize bluesky as non-networked simulation node
bs.init('sim-detached')

# initialize dummy screen
# bs.scr = ScreenDummy()

# generate some trajectories
n = 1

# create n aircraft with random positions, altitudes, speeds

bs.stack.stack('CRELOG INT 1')
bs.stack.stack('INT ADD id,lat, lon, alt, tas, vs ')
bs.stack.stack('INT ON 1  ')
bs.stack.stack('TAXI OFF 6')

# bs.traf.cre(acid=acids, actype=actypes, aclat=aclats, aclon=aclons,
#          achdg=achdgs, acalt=acalts, acspd=acspds)
# alternative: individually initialize each aircraft by passing the initial
# position, heading, altitude, and speed.
# bs.traf.cre(acid=acids, actype=actypes, aclat=aclats, aclon=aclons,
#         achdg=achdgs, acalt=acalts, acspd=acspds)

# iterate over traffic and add the same waypoints
# Note that preferably, all simulation commands are initiated through the stack
# however, if you wish, you can also call the functions directly, such as the
# mcre command in the above cell.
# for acid in bs.traf.id:
#     print(acid)
#     # set the origin (not needed if initialized in flight),
#     # and add some waypoints, here only the altitude (in m) is passed to the
#     # function, but you can additionally pass a speed as well
#     # finally turn on VNAV for each flight
#     bs.stack.stack(f'>ORIG {acid} A_1;'
#                    f'DEST {acid} A_15;'
#                    f'ADDWPT {acid} A_2 400 31;'
#                    f'ADDWPT {acid} A_3 400 31;'
#                    f'ADDWPT {acid} A_4 400 31;'
#                    f'ADDWPT {acid} A_5 400 31;'
#                    f'ADDWPT {acid} A_6 400 31;'
#                    f'ADDWPT {acid} A_7 400 31;'
#                    f'ADDWPT {acid} A_8 200 31;'
#                    f'ADDWPT {acid} A_9 200 31;'
#                    f'ADDWPT {acid} A_10 200 31;'
#                    f'ADDWPT {acid} A_11 200 31;'
#                    f'ADDWPT {acid} A_12 200 31;'
#                    f'ADDWPT {acid} A_13 200 31;'
#                    f'ADDWPT {acid} A_14 200 31;'
#                    f'VNAV {acid} ON;'
#                    f'DUMPRTE {acid}')

    # you can also set the way the waypoint should be flown
    # bs.stack.stack(f'ADDWPT {acid} FLYOVER')

    # you can also set a destination
    # bs.stack.stack(f'DEST {acid} EHAM')

def get_distance(lat1,lon1,lat2,lon2,alt1,alt2):

    horizon_dist=geodesic((lat1,lon1), (lat2,lon2)).m
    dist=sqrt(horizon_dist**2+(alt1-alt2)**2)

    return horizon_dist

def add_plane(acid):
    speed_list=[30,31,32,33,34]
    # speed_list=[30]
    bs.stack.stack(f'ORIG {acid} A_1;'
                   f'DEST {acid} A_15;'
                   f'ADDWPT {acid} A_2 400 {sample(speed_list,1)[0]};'
                   f'ADDWPT {acid} A_3 400 {sample(speed_list,1)[0]};'
                   f'ADDWPT {acid} A_4 400 {sample(speed_list,1)[0]};'
                   f'ADDWPT {acid} A_5 400 {sample(speed_list,1)[0]};'
                   f'ADDWPT {acid} A_6 400 {sample(speed_list,1)[0]};'
                   f'ADDWPT {acid} A_7 400 {sample(speed_list,1)[0]};'
                   f'ADDWPT {acid} A_8 400 {sample(speed_list,1)[0]};'
                   f'ADDWPT {acid} A_9 400 {sample(speed_list,1)[0]};'
                   f'ADDWPT {acid} A_10 400 {sample(speed_list,1)[0]};'
                   f'ADDWPT {acid} A_11 400 {sample(speed_list,1)[0]};'
                   f'ADDWPT {acid} A_12 400 {sample(speed_list,1)[0]};'
                   f'ADDWPT {acid} A_13 400 {sample(speed_list,1)[0]};'
                   f'ADDWPT {acid} A_14 400 {sample(speed_list,1)[0]};'
                   f'VNAV {acid} ON;'
                   f'DUMPRTE {acid}')

# set simulation time step, and enable fast-time running
bs.stack.stack('DT 1;FF')

# we'll run the simulation for up to 2000 seconds
t_max = 2000

ntraf = bs.traf.ntraf

n_steps = int(t_max + 1)
t = np.linspace(0, t_max, n_steps)

# allocate some empty arrays for the results
# res = np.zeros((n_steps, 4, ntraf))
res1=np.zeros((n_steps, 4, 1))
res2=np.zeros((n_steps, 4, 1))
# iteratively simulate the traffic
ind=0
ind2=0
dist_list=np.zeros(n_steps)
dis=10000
interval=100
for i in range(n_steps):
    # Perform one step of the simulation
    if i==0:
        bs.traf.cre(acid='A1', actype="ELE01",aclat=40.701863,aclon=-74.015915,acalt=0,acspd=3)
        add_plane("A1")
    bs.sim.step()
    if i == interval:
        bs.traf.cre(acid="A2", actype="ELE01",aclat=40.701863,aclon=-74.015915,acalt=0,acspd=3)
        add_plane("A2")

    if i == 500:
         bs.stack.stack('SPD A2 45')
    if dis<=100 and ind==1:
        bs.stack.stack('SPD A2 20')
        ind2=1
    if dis>500 and ind2==1:
        bs.stack.stack('SPD A2 30')
    if len(bs.traf.lat)==1 and ind==0:
        res1[i]=[[bs.traf.lat[0]], [bs.traf.lon[0]], [bs.traf.alt[0]], [bs.traf.tas[0]]]
    if len(bs.traf.lat)==2:
        ind=1
        res1[i]=[[bs.traf.lat[0]], [bs.traf.lon[0]], [bs.traf.alt[0]], [bs.traf.tas[0]]]
        res2[i]=[[bs.traf.lat[1]], [bs.traf.lon[1]], [bs.traf.alt[1]], [bs.traf.tas[1]]]
        end1=i
        dis=get_distance(bs.traf.lat[0],bs.traf.lon[0],bs.traf.lat[1],bs.traf.lon[1],bs.traf.alt[0],bs.traf.alt[1])
        dist_list[i]=dis

    if len(bs.traf.lat)==1 and ind==1:
        end2=i
        res2[i]=[[bs.traf.lat[0]], [bs.traf.lon[0]], [bs.traf.alt[0]], [bs.traf.tas[0]]]

# plot
import matplotlib.pyplot as plt


fig = plt.figure(figsize=(10, 20))
ax1 = plt.subplot2grid((5, 1), (0, 0), rowspan=2)
ax2 = plt.subplot2grid((5, 1), (2, 0))
ax3 = plt.subplot2grid((5, 1), (3, 0))
ax4 = plt.subplot2grid((5, 1), (4, 0))
#
ax1.plot(res1[0:end1, 1], res1[0:end1, 0])
ax1.plot(res2[interval:end2, 1], res2[interval:end2, 0])
#
print(res2[:, 3])
ax2.plot(res1[:, 2],label="A1")
ax2.plot(res2[:, 2],label="A2")
ax2.set_xlabel('t [s]')
ax2.set_ylabel('alt [m]')

ax3.plot(res1[:, 3],label="A1")
ax3.plot(res2[:, 3],label="A2")
ax3.set_xlabel('t [s]')
ax3.set_ylabel('TAS [m/s]')

ax4.plot(dist_list)
ax4.set_xlabel('t [s]')
ax4.set_ylabel('dist [m]')
# fig.suptitle(f'Trajectory {acid}')
ax2.legend()
ax3.legend()
plt.show()