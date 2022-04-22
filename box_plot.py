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


def plot_capacity():
    data = pd.read_csv("exp1_capacity.csv")
    LOS =  data[data['Event Type']=='LOS']
    NMAC = data[data['Event Type']=='NMAC']
    Ground_Delay = data[data['Event Type']=='Ground Delay']

    ax = sns.boxplot(x="Capacity of Each DCB Block", y="Number of Event",
                     data=LOS,color="steelblue",showfliers = False)
    plt.title("Capacity VS LOS")
    plt.ylabel("Number of LOS")
    plt.show()
    ax = sns.boxplot(x="Capacity of Each DCB Block", y="Number of Event",
                     data=NMAC,color="tan",showfliers = False)
    plt.title("Capacity VS NMAC")
    plt.ylabel("Number of NMAC")
    plt.show()
    ax = sns.boxplot(x="Capacity of Each DCB Block", y="Number of Event",
                     data=Ground_Delay,color="mediumseagreen",showfliers = False)
    plt.title("Capacity VS Ground Delay")
    plt.ylabel("Average Ground Delay (seconds)")
    plt.show()

def plot_block():
    data = pd.read_csv("exp2_block.csv")
    LOS =  data[data['Event Type']=='LOS']
    NMAC = data[data['Event Type']=='NMAC']
    Ground_Delay = data[data['Event Type']=='Ground Delay']

    ax = sns.boxplot(x="Size of Each DCB Block", y="Number of Event",
                     data=LOS,color="steelblue",showfliers = False)
    plt.title("Block Size VS LOS")
    plt.ylabel("Number of LOS")
    plt.show()
    ax = sns.boxplot(x="Size of Each DCB Block", y="Number of Event",
                     data=NMAC,color="tan",showfliers = False)
    plt.title("Block Size VS NMAC")
    plt.ylabel("Number of NMAC")
    plt.show()
    ax = sns.boxplot(x="Size of Each DCB Block", y="Number of Event",
                     data=Ground_Delay,color="mediumseagreen",showfliers = False)
    plt.title("Block Size VS Ground Delay")
    plt.ylabel("Average Ground Delay (seconds)")
    plt.show()

def plot_interval():
    data = pd.read_csv("exp3_interval.csv")
    LOS =  data[data['Event Type']=='LOS']
    NMAC = data[data['Event Type']=='NMAC']
    Ground_Delay = data[data['Event Type']=='Ground Delay']

    ax = sns.boxplot(x="Interval of Each DCB Block", y="Number of Event",
                     data=LOS,color="steelblue",showfliers = False)
    plt.title("Departure Interval VS LOS")
    plt.ylabel("Number of LOS")
    plt.xlabel("Flight Departure Average Interval (seconds)")
    plt.show()
    ax = sns.boxplot(x="Interval of Each DCB Block", y="Number of Event",
                     data=NMAC,color="tan",showfliers = False)
    plt.title("Departure Interval VS NMAC")
    plt.ylabel("Number of NMAC")
    plt.xlabel("Flight Departure Average Interval (seconds)")
    plt.show()
    ax = sns.boxplot(x="Interval of Each DCB Block", y="Number of Event",
                     data=Ground_Delay,color="mediumseagreen",showfliers = False)
    plt.title("Departure Interval VS Ground Delay")
    plt.ylabel("Average Ground Delay (seconds)")
    plt.xlabel("Flight Departure Average Interval (seconds)")
    plt.show()
plot_capacity()
# plot_block()
# plot_interval()