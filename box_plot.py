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
    Ground_Delay = data[data['Event Type']=='Ground_Delay']

    plt.figure(figsize=(10, 8))
    ax = sns.boxplot(x="Capacity of Each DCB Block", y="Number of Event",
                     data=LOS,color="steelblue",showfliers = False)
    plt.xticks(fontsize=19)
    plt.yticks(fontsize=19)
    ax.set_xlabel("Capacity of Each DCB Block",fontsize=19)
    ax.set_ylabel("Number of LOS",fontsize=19)
    plt.savefig('image\\exp1_los.png')



    plt.figure(figsize=(10, 8))
    ax = sns.boxplot(x="Capacity of Each DCB Block", y="Number of Event",
                     data=NMAC,color="tan",showfliers = False)
    plt.xticks(fontsize=19)
    plt.yticks(fontsize=19)
    ax.set_xlabel("Capacity of Each DCB Block",fontsize=19)
    ax.set_ylabel("Number of NMAC",fontsize=19)
    plt.savefig('image\\exp1_nmac.png')

    plt.figure(figsize=(10, 8))
    ax = sns.boxplot(x="Capacity of Each DCB Block", y="Number of Event",
                     data=Ground_Delay,color="mediumseagreen",showfliers = False)
    plt.xticks(fontsize=19)
    plt.yticks(fontsize=19)
    ax.set_xlabel("Capacity of Each DCB Block",fontsize=19)
    ax.set_ylabel("Average Ground Delay (seconds)",fontsize=19)
    plt.savefig('image\\exp1_delay.png')

def plot_block():
    data = pd.read_csv("exp2_block.csv")
    LOS =  data[data['Event Type']=='LOS']
    NMAC = data[data['Event Type']=='NMAC']
    Ground_Delay = data[data['Event Type']=='Ground Delay']

    plt.figure(figsize=(10, 8))
    ax = sns.boxplot(x="Size of Each DCB Block", y="Number of Event",
                     data=LOS,color="steelblue",showfliers = False)
    plt.xticks(fontsize=19)
    plt.yticks(fontsize=19)
    ax.set_xlabel("Size of Each DCB Block",fontsize=19)
    ax.set_ylabel("Number of LOS",fontsize=19)
    # ax.legend(fontsize=19)
    plt.savefig('image\\exp2_los.png')

    plt.figure(figsize=(10, 8))
    ax = sns.boxplot(x="Size of Each DCB Block", y="Number of Event",
                     data=NMAC,color="tan",showfliers = False)


    plt.xticks(fontsize=19)
    plt.yticks(fontsize=19)
    ax.set_xlabel("Size of Each DCB Block",fontsize=19)
    ax.set_ylabel("Number of NMAC",fontsize=19)
    plt.savefig('image\\exp2_nmac.png')

    plt.figure(figsize=(10, 8))
    ax = sns.boxplot(x="Size of Each DCB Block", y="Number of Event",
                     data=Ground_Delay,color="mediumseagreen",showfliers = False)
    plt.xticks(fontsize=19)
    plt.yticks(fontsize=19)
    ax.set_xlabel("Size of Each DCB Block",fontsize=19)
    ax.set_ylabel("Average Ground Delay (seconds)",fontsize=19)
    plt.savefig('image\\exp2_delay.png')


def plot_interval():
    data = pd.read_csv("exp3_interval.csv")
    LOS =  data[data['Event Type']=='LOS']
    NMAC = data[data['Event Type']=='NMAC']
    Ground_Delay = data[data['Event Type']=='Ground Delay']

    plt.figure(figsize=(10, 8))
    ax = sns.boxplot(x="Interval of Each DCB Block", y="Number of Event",
                     data=LOS,color="steelblue",showfliers = False)
    plt.xticks(fontsize=19)
    plt.yticks(fontsize=19)
    ax.set_xlabel("Flight Departure Average Interval (seconds)",fontsize=19)
    ax.set_ylabel("Number of LOS",fontsize=19)
    plt.savefig('image\\exp3_los.png')

    plt.figure(figsize=(10, 8))
    ax = sns.boxplot(x="Interval of Each DCB Block", y="Number of Event",
                     data=NMAC,color="tan",showfliers = False)
    plt.xticks(fontsize=19)
    plt.yticks(fontsize=19)
    ax.set_xlabel("Flight Departure Average Interval (seconds)",fontsize=19)
    ax.set_ylabel("Number of NMAC",fontsize=19)
    plt.savefig('image\\exp3_nmac.png')

    plt.figure(figsize=(10, 8))
    ax = sns.boxplot(x="Interval of Each DCB Block", y="Number of Event",
                     data=Ground_Delay,color="mediumseagreen",showfliers = False)
    plt.xticks(fontsize=19)
    plt.yticks(fontsize=19)
    ax.set_xlabel("Flight Departure Average Interval (seconds)",fontsize=19)
    ax.set_ylabel("Average Ground Delay (seconds)",fontsize=19)
    plt.savefig('image\\exp3_delay.png')


def plot_NYC():
    data = pd.read_csv("exp4_NYC.csv")
    LOS1 =  data[data['Event Type']=='LOS with DCB']
    LOS2 =  data[data['Event Type']=='LOS without DCB']
    LOS = pd.concat([LOS1,LOS2])

    NMAC1 = data[data['Event Type']=='NMAC with DCB']
    NMAC2 = data[data['Event Type']=='NMAC without DCB']
    NMAC = pd.concat([NMAC1,NMAC2])

    Ground_Delay1 = data[data['Event Type']=='Ground Delay with DCB']
    Ground_Delay2 = data[data['Event Type']=='Ground Delay without DCB']
    Ground_Delay = pd.concat([Ground_Delay1,Ground_Delay2])

    plt.figure(figsize=(10, 8))
    ax = sns.boxplot(x="GROUP", y="Number of Event",
                     data=LOS,hue='Event Type',color="steelblue",showfliers = False)
    plt.xticks(fontsize=19)
    plt.yticks(fontsize=19)
    ax.set_xlabel("Test Group",fontsize=19)
    ax.set_ylabel("Number of LOS",fontsize=19)
    ax.legend(fontsize=19)
    plt.savefig('image\\exp4_los.png')


    plt.figure(figsize=(10, 8))
    ax = sns.boxplot(x="GROUP", y="Number of Event",
                     data=NMAC,hue='Event Type',color="tan",showfliers = False)
    plt.xticks(fontsize=19)
    plt.yticks(fontsize=19)
    ax.set_xlabel("Test Group",fontsize=19)
    ax.set_ylabel("Number of NMAC",fontsize=19)
    ax.legend(fontsize=19)
    plt.savefig('image\\exp4_nmac.png')


    plt.figure(figsize=(10, 8))
    ax = sns.boxplot(x="GROUP", y="Number of Event",
                     data=Ground_Delay,hue='Event Type',color="mediumseagreen",showfliers = False)
    plt.xticks(fontsize=19)
    plt.yticks(fontsize=19)
    ax.set_xlabel("Test Group",fontsize=19)
    ax.set_ylabel("Average Ground Delay (seconds)",fontsize=19)
    ax.legend(fontsize=19)
    plt.savefig('image\\exp4_dalay.png')

plot_capacity()
plot_block()
plot_interval()
plot_NYC()