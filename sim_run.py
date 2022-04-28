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
exp =  int(sys.argv[1])
para = int(sys.argv[2])
if exp ==1:
    print("Experiment 1")
    for i in range(30):
        os.system(f"python exp1.py {para}")
elif exp ==2:
    print("Experiment 2")
    for i in range(30):
        os.system(f"python exp2.py {para}")
elif exp ==3:
    print("Experiment 3")
    for i in range(30):
        os.system(f"python exp3.py {para}")
elif exp ==4:
    print("Experiment 4")
    for i in range(30):
        os.system(f"python exp4.py {para}")
