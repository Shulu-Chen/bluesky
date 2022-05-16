#!/usr/bin/python3
# coding: utf-8
'''
 @Time    : 4/28/2022 6:37 PM
 @Author  : Shulu Chen
 @FileName: sim_run.py
 @Software: PyCharm
'''
import os
import sys
import numpy as np
# C =  int(sys.argv[1])
# S = int(sys.argv[2])
C_list = [1,2,3,4,5,6,7,8,20]
S_list = [50,100,150,200,250,300,350,400]
exp = 4
if exp ==1:
    print("Experiment 1")
    for c in C_list:
        for s in S_list:
            os.system(f"python exp1.py {c} {s}")
elif exp ==2:
    print("Experiment 2")
    for i in range(20):
        os.system(f"python exp2.py {para}")
elif exp ==3:
    print("Experiment 3")
    for para in np.arange(10,360,10):
        os.system(f"python exp3.py {para}")
elif exp ==4:
    print("Experiment 4")
    for para in np.arange(10,360,10):
        os.system(f"python exp4.py {para}")
elif exp ==6:
    print("Cross heatmap")
    for c in C_list:
        for s in S_list:
            os.system(f"python exp6_cross.py {c} {s}")
elif exp ==7:
    print("Experiment 7")
    for para in np.arange(10,360,10):
        os.system(f"python exp6_cross.py {para}")