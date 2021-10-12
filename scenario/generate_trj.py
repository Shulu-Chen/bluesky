#!/usr/bin/python3
# coding: utf-8
'''
 @Time    : 9/28/2021 2:31 PM
 @Author  : Shulu Chen
 @FileName: generate_trj.py
 @Software: PyCharm
'''
from random import sample
from numpy import random


f=open("NYC_test.scn","w")

f.write("00:00:00.00>TRAILS ON \n")
f.write("\n")
f.write("00:00:00.00>CIRCLE a, 40.689582,-73.886988 0.2 \n")
f.write("00:00:00.00>CIRCLE b, 40.701863,-74.015915 0.2 \n")
f.write("00:00:00.00>CIRCLE c, 40.678505,-74.029101 0.2 \n")
f.write("00:00:00.00>CIRCLE d, 40.712367,-73.976248 0.2 \n")
f.write("00:00:00.00>CIRCLE e, 40.743822,-73.970742 0.2 \n")
f.write("00:00:00.00>CIRCLE f, 40.7779659,-73.8926095 0.2 \n")
f.write("00:00:00.00>CIRCLE g, 40.6668873,-73.8055968 0.2 \n")
f.write("00:00:00.00>CIRCLE h, 40.775976,-73.94206 0.2 \n")
f.write("00:00:00.00>CIRCLE i, 40.78281,-73.935198 0.2 \n")
f.write("0:00:00.00>PAN 40.689582,-73.886988 \n")
f.write("0:00:00.00>ZOOM 2 \n")
f.write("0:00:00.00>ASAS ON \n")
f.write("0:00:00.00>ZONER 0.05 \n")        #Buffer radius/nm  0.05nm=100m
f.write("0:00:00.00>DTNOLOOK 0.1 \n")
f.write("0:00:00.00>FF \n")
f.write("0:00:00.00>TAXI OFF 10 \n")
f.write("0:00:00.00>CRELOG NYCLOG 1 \n")
f.write("0:00:00.00>NYCLOG ADD id,lat, lon, alt, tas, vs \n")
f.write("0:00:00.00>NYCLOG ON 1 \n")


f.write("\n")

n=100        #number of total flights
dep_inte=10     #departure interval for each resource/second

ORIG_list=["A_","B_","C_","D_","E2_",'F_','G_','H_',"I_","J_","L_"]
ROUTE={"A_":15,"B_":26,"C_":8,"D_":8,"E2_":6,'F_':6,'G_':10,'H_':8,"I_":7,"J_":9,"L_":9}

route_id_old=""
id_dict={}

for i in range(n):

    x = random.poisson(lam=1, size=1)
    if x[0] > 11:
       x[0] = 11
    route_ids = sample(ORIG_list,x[0])


    for route_id in route_ids:

        plane = "U_"+str(route_id)+str(i)

        if route_id != route_id_old:
            id_dict[plane] = route_id
            route_length = ROUTE[route_id]
            current_time = i*dep_inte
            time = "00:00:"+str(current_time)+".00"

            f.write(time+">CRE "+plane+",Mavic,"+route_id+"1,0,0"+"\n")
            f.write(time+">LISTRTE "+plane+"\n")
            f.write(time+">ORIG "+plane+" "+route_id+"1\n")
            f.write(time+">DEST "+plane+" "+route_id+str(route_length)+"\n")
            f.write(time+">SPD "+plane+" 30"+"\n")
            f.write(time+">ALT "+plane+" 400"+"\n")


            for j in range(route_length-2):
                wpt=route_id+str(j+2)
                f.write(time+">ADDWPT "+plane+" "+wpt+" 400 40"+"\n")
            f.write(time+">"+plane+" VNAV on \n")


            f.write("\n")
        route_id_old=route_id


f.close()

