import sys
import os
import re
sys.path.append("../")
import time

import numpy as np
import pandas as pd
from geopy.distance import geodesic
from math import sqrt
from random import expovariate
from bluesky.tools import geo

from sequencing.compute_DCB import ComputeDCB
from supports.operation_writer import OperationWriter


class SupportMethods():

    @staticmethod
    def get_distance(location1,location2):
        '''
        conpute the distance of two aircraft, meters
        '''
        lat1=location1[0]
        lon1=location1[1]
        alt1=location1[2]
        lat2=location2[0]
        lon2=location2[1]
        alt2=location2[2]
        horizon_dist=geodesic((lat1,lon1), (lat2,lon2)).m
        dist=sqrt(horizon_dist**2+(alt1-alt2)**2)
        return horizon_dist

    @staticmethod
    def generate_departure_table(landing_num, demand_interval, ROUTES=['U', 'D']):
        '''
        Generate the demand based on exponential distribution, lambda-number of flight per second,
        lambda=0.1--flight interval=10s
        '''
        ETA_tabel = []
        for route_id in ROUTES:
            ETA_list = []
            for _ in range(landing_num):
                ETA_list.append(round(expovariate(1 / demand_interval)))
            ETA_cum = list(np.cumsum(ETA_list))
            for ETA in ETA_cum:
                ETA_tabel.append((ETA, route_id))
        ETA_tabel = sorted(ETA_tabel)
        return ETA_tabel


    @staticmethod
    def generate_beta_appear_table(landing_num, demand_interval, ROUTES=['U', 'D'] , alpha=2, beta=4):
        time_horizon = landing_num * demand_interval
        ETA_tabel = {}
        for route_id in ROUTES:
            ETA_list = sorted(np.random.beta(alpha, beta, size=landing_num) * time_horizon)
            ETA_list = [int(ETA) for ETA in ETA_list]
            ETA_tabel[route_id] = ETA_list
        return ETA_tabel

    @staticmethod
    def generate_unif_appear_table(landing_num, demand_interval, ROUTES=['U', 'D']):
        time_horizon = landing_num * demand_interval
        ETA_tabel = {}
        for route_id in ROUTES:
            ETA_list = np.arange(0, time_horizon, demand_interval).tolist()
            ETA_list = [int(ETA) for ETA in ETA_list]
            ETA_tabel[route_id] = ETA_list
        return ETA_tabel

    @staticmethod
    def list_to_dict(schedule_table):
        schedule_dic = {}
        for item in schedule_table:
            if item[1] in schedule_dic.keys():
                schedule_dic[item[1]].append(item[0])
            else:
                schedule_dic[item[1]] = []
                schedule_dic[item[1]].append(item[0])
        for key in schedule_dic.keys():
            schedule_dic[key] = np.array(schedule_dic[key])
        return schedule_dic

    @staticmethod
    def save_to_csv(schedule_table, csv_path):
        schedule_dic = SupportMethods.list_to_dict(schedule_table)
        df = pd.DataFrame(schedule_dic)
        df.to_csv(csv_path)

    @staticmethod
    def count_close_points(lat, lon, LOS_dist=100, NMAC_dist=10):
        """
        Count the number of points in the given list of coordinates that are closer than the given distance threshold.
        """
        LOS = 0
        NMAC = 0
        for i in range(len(lat)):
            for j in range(i+1, len(lon)):
                distance = geo.latlondist(lat[i], lon[i], lat[j], lon[j])
                if distance < LOS_dist:
                    LOS += 1
                if distance < NMAC_dist:
                    NMAC += 1
        return LOS, NMAC

    @staticmethod
    def generate_scenario_file(file_id, scn_type, plot_image=False, capacity=3, interval=90, ac_num=10):
        '''
        This method is used to generate scenario files.
        Scn_type: cross/ merge_
        '''

        T_MAX = 8000  # second
        BLOCK_SIZE = 200  # second

        directory = f"../scenario/{scn_type}_{interval}_{capacity}_test"
        if not os.path.exists(directory):
            os.makedirs(directory)

        SCN_FILE_DCB = f"{directory}/{file_id}.scn"

        depart_buffer = max(int(BLOCK_SIZE / capacity), 20)
        if scn_type == "hybird":
            departure_table = SupportMethods.generate_beta_appear_table(ac_num, interval, ROUTES=['U', 'D', 'C'])
            fly_time = {"U": [225,300], "D":[225,300], "C":[150]}
            inter_id =  {"U": [0,1], "D":[0,1], "C":[1]}
            check_points =  [0, 1]
        else:
            departure_table = SupportMethods.generate_unif_appear_table(ac_num, interval, ROUTES=['U'])
            fly_time = {"U": [225], "D":[225]}
            inter_id =  {"U": [0], "D":[0]}
            check_points =  [0]
        start = time.time()
        # print(departure_table)
        S = ComputeDCB(departure_table, depart_buffer, T_MAX, capacity, BLOCK_SIZE, fly_time, inter_id, check_points)
        schedule_table = S.get_computed_time()
        schedule_table = sorted(schedule_table)

        # PlotMethods.plot_dcb_hist(point_2, point_2)


        sched_depart_total_time = 0
        for pair in schedule_table:
            sched_depart_total_time += pair[0]
        depart_total_time = sum([sum(departure_table[i]) for i in departure_table.keys()])

        operator_writer = OperationWriter(SCN_FILE_DCB)
        operator_writer.init_scn()


        if scn_type == "cross":
            operator_writer.generate_cross_file(schedule_table)
            print(f"generate file {SCN_FILE_DCB} succesfully")

        elif scn_type == "merge":
            operator_writer.generate_merge_file(schedule_table)
            print(f"generate file {SCN_FILE_DCB} succesfully")

        elif scn_type == "hybird":
            operator_writer.generate_hybird_file(schedule_table)
            print(f"generate file {SCN_FILE_DCB} succesfully")
        operator_writer.end_generator()

        return (sched_depart_total_time - depart_total_time)/30


    @staticmethod
    def merge_scn_file(input_path1, input_path2, output_path):
        '''
        This function is used to merge original scn file and the actions generated from RL model
        '''

        origin_scn = input_path1
        rl_scn = input_path2
        # Read the contents of both text files into separate lists
        with open(origin_scn, 'r') as f:
            lines1 = f.readlines()
        with open(rl_scn, 'r') as f:
            lines2 = f.readlines()

        # Sort the lines in each list by the time variable
        def extract_time(line):
            if line.strip():
                return float(re.split(">|:", line)[2])
            else:
                return 0.0

        lines = lines1 + lines2
        sorted_lines = sorted(lines, key=extract_time)

        # Write the merged list of lines to a new text file
        with open(output_path, 'w') as f:
            f.writelines(sorted_lines)
        f.close()

    @staticmethod
    def count_speed_change_times(input_path):
        '''
        This function is to count number of speed change times
        '''
        with open(input_path) as f:
            text = f.read()
            count = len(re.findall(r'SPD',text))
        return count

