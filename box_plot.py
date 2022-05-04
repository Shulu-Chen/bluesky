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

def plot_heatmap(demand):
    data = pd.read_csv(f"result\\grid_search_{demand}.csv")
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
            LOS_mean.append(round(np.mean(LOS_num['Number'])*5/3000,1))
            NMAC_mean.append(round(np.mean(NMAC_num['Number'])*5/3000,1))
            Ground_Delay_mean.append(np.mean(delay_num['Number']))
            C.append(c)
            S.append(s)
    table1={"Capacity" : C, "Block Size" : S,"LOS":LOS_mean}
    data=pd.DataFrame(table1)
    data=data.pivot("Block Size","Capacity","LOS")
    sns.set(font_scale=1.4)
    sns.set_context({"figure.figsize":(9,8)})
    # cbar_kws = { 'ticks' : [0, 30] }
    sns.heatmap(data=data,annot=True,cmap="RdBu_r", vmin=0, vmax=25)

    plt.ylim(0,8)
    # sns.set_context("set_context","Test Class",fontsize=19)
    # sns.set_ylabel("Average Ground Delay (seconds)",fontsize=19)
    plt.savefig(f'image\\heatmap_los_{demand}.png')
    plt.close()

    table2={"Capacity" : C, "Block Size" : S,"NMAC":NMAC_mean}
    data=pd.DataFrame(table2)
    data=data.pivot("Block Size","Capacity","NMAC")
    sns.set_context({"figure.figsize":(9,8)})
    sns.heatmap(data=data,annot=True,cmap="RdBu_r",vmin=0, vmax=5)
    plt.ylim(0,8)
    # sns.set_xlabel("Capacity",fontsize=10)
    # sns.set_ylabel("Block Size",fontsize=10)
    plt.savefig(f'image\\heatmap_nmac_{demand}.png')

def plot_exp5():
    data = pd.read_csv("result\\exp5.csv")
    Ground_Delay = data[data['Event Type']=='Ground Delay']
    plt.xticks(fontsize=19)
    plt.yticks(fontsize=19)
    plt.figure(figsize=(10, 8))
    ax = sns.boxplot(x="Test Class", y="Number",
                 data=Ground_Delay,color="mediumseagreen",showfliers = False)
    ax.set_xlabel("Test Class",fontsize=10)
    ax.set_ylabel("Average Ground Delay (seconds)",fontsize=10)
    plt.savefig('image\\exp5_delay.png')

def compute_interval(path):
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
    Ground_Delay_mean = []

    for d in np.arange(10,125,5):
        LOS_num = LOS[LOS['D']==d]
        NMAC_num = NMAC[NMAC['D']==d]
        delay_num = Ground_Delay[Ground_Delay['D']==d]
        LOS_mean.append(np.mean(LOS_num['N']*5/3000))
        LOS_sem.append(st.sem(LOS_num['N']*5/3000))
        # LOS_std.append(round(np.std(LOS_num['N'])*5/3000,1))
        # conf_intveral = stats.norm.interval(0.9, loc=mean, scale=std)
        NMAC_mean.append(round(np.mean(NMAC_num['N']*5/3000),1))
        Ground_Delay_mean.append(np.mean(delay_num['N']))

    data_points = len(LOS_mean)


    # predicted expect and calculate confidence interval
    predicted_expect = np.mean(data, 0)
    low_CI_bound, high_CI_bound = st.t.interval(0.9, len(LOS_mean) - 1,
                                                loc=LOS_mean,scale=LOS_sem)
    # plot confidence interval
    x = np.linspace(10, 125, num=data_points)

    return LOS_mean,x,low_CI_bound,high_CI_bound



def plot_exp6():
    LOS_mean1,X1,low_CI1,high_CI1=compute_interval("result\\interval_none.txt")
    LOS_mean2,X2,low_CI2,high_CI2=compute_interval("result\\interval_T1.txt")
    LOS_mean3,X3,low_CI3,high_CI3=compute_interval("result\\interval_T10_2.txt")
    LOS_mean4,X4,low_CI4,high_CI4=compute_interval("result\\interval_C1S50.txt")
    LOS_mean5,X5,low_CI5,high_CI5=compute_interval("result\\interval_C1S100.txt")
    LOS_mean6,X6,low_CI6,high_CI6=compute_interval("result\\interval_C3S150.txt")
    LOS_mean7,X7,low_CI7,high_CI7=compute_interval("result\\interval_C3S200.txt")
    LOS_mean8,X8,low_CI8,high_CI8=compute_interval("result\\interval_T5.txt")

    plt.figure(figsize=(16, 12))
    plt.xticks(fontsize=22)
    plt.yticks(fontsize=22)
    plt.plot(X1,LOS_mean1, linewidth=3., label='No DCB/Tactical')
    plt.fill_between(X1, low_CI1, high_CI1, alpha=0.5)

    # plt.plot(X2,LOS_mean2, linewidth=3., label='Tactical, control frequency = 1s')
    # plt.fill_between(X2, low_CI2, high_CI2, alpha=0.5)

    # plt.plot(X8,LOS_mean8, linewidth=3., label='Tactical, control frequency = 5s')
    # plt.fill_between(X8, low_CI8, high_CI8, alpha=0.5)

    plt.plot(X3,LOS_mean3, linewidth=3., label='Tactical mitigation')
    plt.fill_between(X3, low_CI3, high_CI3, alpha=0.5)

    plt.plot(X7,LOS_mean7, linewidth=3., label='DCB+Tactical,C=3,S=200')
    plt.fill_between(X7, low_CI7, high_CI7, alpha=0.5)

    plt.ylabel('LOS Duration (%)', fontdict={'size': 22})
    plt.xlabel('Average Departure Interval', fontdict={'size': 22})
    plt.ylim(0,35)
    plt.legend(fontsize=22)
    # plt.grid()
    plt.savefig('image\\exp6_LOS.png')
    plt.show()
    plt.close()

    plt.figure(figsize=(16, 12))
    plt.xticks(fontsize=22)
    plt.yticks(fontsize=22)

    plt.plot(X1,LOS_mean1, linewidth=3., label='No DCB/Tactical')

    plt.plot(X2,LOS_mean2, linewidth=3., label='Tactical, control frequency: 1s')

    plt.plot(X8,LOS_mean8, linewidth=3., label='Tactical, control frequency: 5s')

    plt.plot(X3,LOS_mean3, linewidth=3., label='Tactical, control frequency: 10s')

    plt.plot(X4,LOS_mean4, linewidth=3., label='DCB+Tactical,C=1,S=50')

    plt.plot(X5,LOS_mean5, linewidth=3., label='DCB+Tactical,C=1,S=100')

    plt.plot(X6,LOS_mean6, linewidth=3., label='DCB+Tactical,C=3,S=150')

    plt.plot(X7,LOS_mean7, linewidth=3., label='DCB+Tactical,C=3,S=200')

    plt.ylabel('LOS Duration (%)', fontdict={'size': 22})
    plt.xlabel('Average Departure Interval', fontdict={'size': 22})
    plt.ylim(0,35)
    plt.legend(fontsize=22)
    # plt.grid()
    plt.savefig('image\\exp6_multiple.png')
    plt.show()
    plt.close()


# plot_capacity()
# plot_block()
# plot_interval()
# plot_NYC()
# plot_heatmap(30)
# plot_exp5()
plot_exp6()





























