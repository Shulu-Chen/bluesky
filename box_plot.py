#!/usr/bin/python3
# coding: utf-8
'''
 @Time    : 4/21/2022 4:17 PM
 @Author  : Shulu Chen
 @FileName: box_plot.py
 @Software: PyCharm
'''
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv("exp1_capacity.csv")
LOS =  data[data['Event Type']=='LOS']
NMAC = data[data['Event Type']=='NMAC']
Ground_Delay = data[data['Event Type']=='Ground_Delay']

ax = sns.boxplot(x="Capacity of Each DCB Block", y="Number of Event", data=LOS,color="steelblue")
plt.title("Capacity VS LOS")
plt.ylabel("Number of LOS")
plt.show()
ax = sns.boxplot(x="Capacity of Each DCB Block", y="Number of Event", data=NMAC,color="tan")
plt.title("Capacity VS NMAC")
plt.ylabel("Number of NMAC")
plt.show()
ax = sns.boxplot(x="Capacity of Each DCB Block", y="Number of Event", data=Ground_Delay,color="mediumseagreen")
plt.title("Capacity VS Ground Delay")
plt.ylabel("Average Ground Delay (seconds)")
plt.show()
