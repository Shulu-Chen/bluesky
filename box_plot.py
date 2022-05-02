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
import numpy as np

def plot_capacity():
    data = pd.read_csv("exp1_capacity.csv")
    LOS =  data[data['Event Type']=='LOS']
    LOS['Number of Event'] /= 1500
    NMAC = data[data['Event Type']=='NMAC']
    NMAC['Number of Event'] /= 1500
    Ground_Delay = data[data['Event Type']=='Ground Delay']

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
    LOS1 =  data[data['Event Type']=='LOS with high']
    LOS2 =  data[data['Event Type']=='LOS_low']
    LOS3 =  data[data['Event Type']=='LOS_no']
    LOS = pd.concat([LOS1,LOS2,LOS3])

    NMAC1 = data[data['Event Type']=='NMAC_high']
    NMAC2 = data[data['Event Type']=='NMAC_low']
    NMAC3 = data[data['Event Type']=='NMAC_no']
    NMAC = pd.concat([NMAC1,NMAC2,NMAC3])

    Ground_Delay1 = data[data['Event Type']=='Delay_high']
    Ground_Delay2 = data[data['Event Type']=='Delay_low']
    Ground_Delay3 = data[data['Event Type']=='Delay_no']
    Ground_Delay = pd.concat([Ground_Delay1,Ground_Delay2,Ground_Delay3])

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

def plot_heatmap():
    data = pd.read_csv("grid_search.csv")
    LOS =  data[data['Event Type']=='LOS']
    NMAC = data[data['Event Type']=='NMAC']
    Ground_Delay = data[data['Event Type']=='Ground Delay']
    C_list = [1,2,3,4,5,6,7,8,20]
    S_list = [50,100,150,200,250,300,350,400]
    LOS_mean = []
    NMAC_mean = []
    Ground_Delay_mean = []
    C = []
    S = []
    for c in C_list:
        for s in S_list:
            LOS_num = LOS[(LOS['C']==c) & (LOS['S']==s)]
            NMAC_num = NMAC[(NMAC['C']==c) & (NMAC['S']==s)]
            delay_num = Ground_Delay[(Ground_Delay['C']==c) & (Ground_Delay['S']==s)]
            LOS_mean.append(round(np.mean(LOS_num['Number'])*5/3000,2))
            NMAC_mean.append(round(np.mean(NMAC_num['Number'])*5/3000,2))
            Ground_Delay_mean.append(np.mean(delay_num['Number']))
            C.append(c)
            S.append(s)
    table1={"Capacity" : C, "Block Size" : S,"LOS":LOS_mean}
    data=pd.DataFrame(table1)
    data=data.pivot("Block Size","Capacity","LOS")

    sns.set_context({"figure.figsize":(8,8)})
    sns.heatmap(data=data,annot=True,cmap="RdBu_r")
    # sns.set_context("set_context","Test Class",fontsize=19)
    # sns.set_ylabel("Average Ground Delay (seconds)",fontsize=19)
    plt.savefig('image\\heatmap_los.png')
    plt.close()
    table2={"Capacity" : C, "Block Size" : S,"NMAC":NMAC_mean}
    data=pd.DataFrame(table2)
    data=data.pivot("Block Size","Capacity","NMAC")
    sns.set_context({"figure.figsize":(8,8)})
    sns.heatmap(data=data,annot=True,cmap="RdBu_r")
    # sns.set_xlabel("Capacity",fontsize=10)
    # sns.set_ylabel("Block Size",fontsize=10)
    plt.savefig('image\\heatmap_nmac.png')

def plot_exp5():
    data = pd.read_csv("exp5.csv")
    Ground_Delay = data[data['Event Type']=='Ground Delay']
    plt.xticks(fontsize=19)
    plt.yticks(fontsize=19)
    plt.figure(figsize=(10, 8))
    ax = sns.boxplot(x="Test Class", y="Number",
                 data=Ground_Delay,color="mediumseagreen",showfliers = False)
    ax.set_xlabel("Test Class",fontsize=10)
    ax.set_ylabel("Average Ground Delay (seconds)",fontsize=10)
    plt.savefig('image\\exp5_delay.png')
# plot_capacity()
# plot_block()
# plot_interval()
# plot_NYC()
plot_heatmap()
# plot_exp5()