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
import scipy.stats as st


def plot_capacity():
    data = pd.read_csv("result\\exp1_capacity.csv")
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
    data = pd.read_csv("result\\exp2_block.csv")
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
    data = pd.read_csv("result\\exp3_interval.csv")
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
    data = pd.read_csv("result\\exp4_NYC.csv")
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

def plot_heatmap(demand,cross):
    if not cross:
        path = f"result\\grid_search_{demand}.txt"
        running_time = 2500
        los_max = 25
        nmac_max = 5
    else:
        path = f"result\\GridSearch_cross_{demand}.txt"
        running_time = 2000
        los_max = 10
        nmac_max = 1

    if demand == 30:
        colabel = True
        wide = 11
    else:
        colabel = False
        wide = 9

    data = pd.read_table(path,sep=',',header=None)
    data.columns=['Number','C','S','Event Type']
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
            LOS_mean.append(round(np.mean(LOS_num['Number'])*5/running_time,1))
            NMAC_mean.append(round(np.mean(NMAC_num['Number'])*5/running_time,1))
            Ground_Delay_mean.append(round(np.mean(delay_num['Number'])/60,1))
            C.append(c)
            S.append(s)

    table1={"Capacity" : C, "Block Size" : S,"LOS":LOS_mean}
    data=pd.DataFrame(table1)
    data=data.pivot("Block Size","Capacity","LOS")
    sns.set(font_scale=1.4)
    sns.set_context({"figure.figsize":(wide,8)})
    # cbar_kws = { 'ticks' : [0, 30] }
    sns.heatmap(data=data,annot=True,cmap="RdBu_r", vmin=0, vmax=los_max,cbar=colabel,
                cbar_kws={'label': 'LOS Duration (%)'})

    plt.ylim(0,8)
    # sns.set_context("set_context","Test Class",fontsize=19)
    plt.ylabel('DCB Window Size (seconds)', fontsize = 19)
    if not cross:
        plt.savefig(f'image\\heatmap_merge_los_{demand}.pdf')
    else:
        plt.savefig(f'image\\heatmap_cross_los_{demand}.pdf')
    plt.show()
    plt.close()


    table2={"Capacity" : C, "Block Size" : S,"NMAC":NMAC_mean}
    data=pd.DataFrame(table2)
    data=data.pivot("Block Size","Capacity","NMAC")
    sns.set_context({"figure.figsize":(wide,8)})
    sns.heatmap(data=data,annot=True,cmap="RdBu_r",vmin=0, vmax=nmac_max,cbar=colabel,
                cbar_kws={'label': 'NMAC Duration (%)'})
    plt.ylim(0,8)
    # sns.set_xlabel("Capacity",fontsize=10)
    plt.ylabel('DCB Window Size (seconds)', fontsize = 19)
    if not cross:
        plt.savefig(f'image\\heatmap_merge_nmac_{demand}.pdf')
    else:
        plt.savefig(f'image\\heatmap_cross_nmac_{demand}.pdf')
    plt.show()
    plt.close()

    table3={"Capacity" : C, "Block Size" : S,"Delay":Ground_Delay_mean}
    data=pd.DataFrame(table3)
    data=data.pivot("Block Size","Capacity","Delay")
    sns.set_context({"figure.figsize":(wide,8)})
    sns.heatmap(data=data,annot=True,cmap="OrRd",vmin=0, vmax=15,cbar=colabel,
                cbar_kws={'label': 'Average Ground Delay (minute)'})
    plt.ylim(0,8)
    # sns.set_xlabel("Capacity",fontsize=10)
    plt.ylabel('DCB Window Size (seconds)', fontsize = 19)
    if not cross:
        plt.savefig(f'image\\heatmap_merge_delay_{demand}.pdf')
    else:
        plt.savefig(f'image\\heatmap_cross_delay_{demand}.pdf')
    plt.show()

def plot_exp5():
    data = pd.read_csv("result\\exp5.csv")
    Ground_Delay = data[data['Event Type']=='Ground Delay']
    plt.xticks(fontsize=19)
    plt.yticks(fontsize=19)
    plt.figure(figsize=(10, 8))
    ax = sns.boxplot(x="Test Class", y="Number",
                 data=Ground_Delay,color="mediumseagreen",showfliers = True)
    ax.set_xlabel("Test Class",fontsize=10)
    ax.set_ylabel("Average Ground Delay (seconds)",fontsize=10)
    plt.savefig('image\\exp5_delay.png')

def compute_interval(path,plt_type,scn):
    if scn == "cross":
        running_time = 400
    if scn == "merge":
        running_time = 500
    if scn == "NYC":
        running_time = 357
    data = pd.read_table(path,sep=',',header=None)
    data.columns=['N','D','Type']
    LOS =  data[data['Type']=='LOS']
    NMAC = data[data['Type']=='NMAC']
    Ground_Delay = data[data['Type']=='Ground Delay']
    # C_list = [1,2,3,4,5,6,7,8,20]
    # S_list = [50,100,150,200,250,300,350,400]
    LOS_mean = []
    LOS_sem = []
    NMAC_mean = []
    NMAC_sem = []
    Ground_Delay_mean = []
    Ground_Delay_sem = []
    for d in np.arange(10,360,10):
        LOS_num = LOS[LOS['D']==d]
        NMAC_num = NMAC[NMAC['D']==d]
        delay_num = Ground_Delay[Ground_Delay['D']==d]
        LOS_mean.append(np.mean(LOS_num['N']/running_time))
        LOS_sem.append(st.sem(LOS_num['N']/running_time))
        Ground_Delay_mean.append(np.mean(delay_num['N']))
        Ground_Delay_sem.append(st.sem(delay_num['N']))
        NMAC_mean.append(np.mean(NMAC_num['N']/running_time))
        NMAC_sem.append(st.sem(NMAC_num['N']/running_time))

    data_points = len(Ground_Delay_mean)

    # print(Ground_Delay_mean)
    # predicted expect and calculate confidence interval
    if plt_type == "LOS":
        low_CI_bound, high_CI_bound = st.t.interval(0.95, len(LOS_mean) - 1,
                                                    loc=LOS_mean,scale=LOS_sem)
        mean_num = LOS_mean
    if plt_type == "delay":
        low_CI_bound, high_CI_bound = st.t.interval(0.95, len(Ground_Delay_mean) - 1,
                                                    loc=Ground_Delay_mean,scale=Ground_Delay_sem)
        mean_num = Ground_Delay_mean
    if plt_type == "NMAC":
        low_CI_bound, high_CI_bound = st.t.interval(0.95, len(NMAC_mean) - 1,
                                                    loc=NMAC_mean,scale=NMAC_sem)
        mean_num = NMAC_mean
    # plot confidence interval
    # x = np.linspace(10, 125, num=data_points)
    # d = [3600/i for i in x ]
    x = np.linspace(10, 360, num=data_points)
    # print(d)
    return mean_num,x,low_CI_bound,high_CI_bound



def plot_exp6(plt_type,scn):

    if scn =="merge":
        LOS_mean1,X1,low_CI1,high_CI1=compute_interval("result\\demand_merge_none.txt",plt_type,scn)
        LOS_mean2,X2,low_CI2,high_CI2=compute_interval("result\\demand_merge_tactical.txt",plt_type,scn)
        LOS_mean3,X3,low_CI3,high_CI3=compute_interval("result\\demand_merge_dcb.txt",plt_type,scn)
        label_name = "$C=3,S=200$"
    if scn =="cross":
        LOS_mean1,X1,low_CI1,high_CI1=compute_interval("result\\demand_cross_none.txt",plt_type,scn)
        LOS_mean2,X2,low_CI2,high_CI2=compute_interval("result\\demand_cross_tactical.txt",plt_type,scn)
        LOS_mean3,X3,low_CI3,high_CI3=compute_interval("result\\demand_cross_C7S200.txt",plt_type,scn)
        label_name = "$C=7,S=200$"
    if scn == "NYC":
        LOS_mean1,X1,low_CI1,high_CI1=compute_interval("result/NYC_data_none.txt",plt_type,scn)
        LOS_mean2,X2,low_CI2,high_CI2=compute_interval("result/NYC_data_tac.txt",plt_type,scn)
        LOS_mean3,X3,low_CI3,high_CI3=compute_interval("result/NYC_data_DCB_C3C7.txt",plt_type,scn)
        label_name = "$C_c=3,C_m=7,S=200$"
    plt.figure(figsize=(16, 12))
    plt.xticks(fontsize=22)
    plt.yticks(fontsize=22)

    plt.plot(X1,LOS_mean1, linewidth=3., label='No DCB/tactical deconfliction')
    plt.fill_between(X1, low_CI1, high_CI1, alpha=0.5)

    plt.plot(X2,LOS_mean2, linewidth=3., label='Tactical deconfliction')
    plt.fill_between(X2, low_CI2, high_CI2, alpha=0.5)

    plt.plot(X3,LOS_mean3, linewidth=3., label=f'DCB+Tactical,{label_name}')
    plt.fill_between(X3, low_CI3, high_CI3, alpha=0.5)

    if plt_type == "LOS":
        plt.ylabel('LOS Duration (%)', fontdict={'size': 22})

    if plt_type == "delay":
        plt.ylabel('Average Ground Delay (seconds)', fontdict={'size': 22})

    if plt_type == "NMAC":
        plt.ylabel('NMAC Duration (%)', fontdict={'size': 22})

    plt.xlabel('Demand (ops/hr)', fontdict={'size': 22})

    # plt.ylim(0,100)
    plt.xlim(30,360)
    plt.legend(loc = "upper left",fontsize=22)

    plt.savefig(f'image\\exp6_{plt_type}_{scn}.pdf')
    plt.show()
    plt.close()



# plot_capacity()
# plot_block()
# plot_interval()
# plot_NYC()
# plot_heatmap(30,False) #True: Cross, False: merge
# plot_exp5()
plot_exp6("LOS","NYC")






# LOS_mean1,X1,low_CI1,high_CI1=compute_interval("result\\interval_none.txt")






















