#!/usr/bin/python3
# coding: utf-8
'''
 @Time    : 10/7/2022 1:17 AM
 @Author  : Shulu Chen
 @FileName: compute_DCB.py
 @Software: PyCharm
'''
import random
import numpy as np
from gurobipy import *
import sys
import math
sys.path.append("../")


class ComputeDCB():
    '''
    This function is used to compute departure time by using DCB.
    dep_sch: {"U":[...], "D":[...], ...}
    estimated_flying_time: {"U": [300,600], "D":[300,600], "C":[300]}
    inter_id_per_route: {"U": [0,1], "D":[0,1], "C":[1]}
    check_points: [0, 1]
    '''

    def __init__(self,
                 dep_sch,
                 time_buffer,
                 total_time,
                 capacity,
                 block_size,
                 estimated_flying_time,
                 inter_id_per_route,
                 check_points):

        self.dep_sch = dep_sch
        self.capacity = capacity
        self.block_size = block_size
        self.time_buffer = time_buffer
        self.total_time = total_time
        self.infeasibility = -1
        self.t_est = estimated_flying_time
        self.route_id = list(dep_sch.keys())
        self.inter_id_per_route = inter_id_per_route
        self.check_points = check_points


    def get_computed_time(self):
        '''
        Return the list of scheduled departure time.
        '''
        (obj, DCB_list) = self._Gurobi_Optimization_Method()
        if (obj == self.infeasibility):
            print("Warning: DCB can not be sloved by Gurobi solver!")
        else:
            return DCB_list


    def _Gurobi_Optimization_Method(self):
        flight_num = len(self.dep_sch[self.route_id[0]])
        C = self.capacity
        W = self.block_size
        R = len(self.route_id)
        delta_t = self.time_buffer
        S = self.dep_sch
        T = math.ceil(self.total_time / self.block_size)
        I = self.inter_id_per_route
        D = self.t_est
        P = self.check_points
        # Create an empty model
        m = Model('Scheduling')
        m.Params.LogToConsole = 0
        w = {}
        # m.setParam('MIPGap', 0.3)

        # Adding decision variables
        A = m.addVars(flight_num, R, vtype=GRB.CONTINUOUS, name='computed_time')

        for r in self.route_id:
            w[r] = m.addMVar((T, flight_num, len(I[r])), vtype=GRB.BINARY)

        # time buffer between two aircraft
        for f in range(flight_num-1):
            for r in range(R):
                m.addConstr(A[f+1, r] - A[f, r] >= delta_t)

        #actual departure time should be larger than scheduled time
        for f in range(flight_num):
            for r in range(R):
                m.addConstr(A[f, r] - S[self.route_id[r]][f] >= 0)

        #sum of occupied variable should be 1
        for f in range(flight_num):
            for r in self.route_id:
                for i in range(len(I[r])):
                    m.addConstr(sum(w[r][:, f, i]) == 1)

        #defination of occupied variable
        for f in range(flight_num):
            for r in range(R):
                for i in range(len(I[self.route_id[r]])):
                    for t in range(T):
                        m.addConstr((A[f, r] + D[self.route_id[r]][i] - W * (t-1)) >= 1000000 * (w[self.route_id[r]][t, f, i] - 1))
                        m.addConstr((A[f, r] + D[self.route_id[r]][i] - W * (t-1)) <= W + 1000000 * (1-w[self.route_id[r]][t, f, i]))

        #DCB constraint
        for t in range(T):
            for p in P:
                temp = 0
                for r in self.route_id:
                    for i in range(len(I[r])):
                        if I[r][i] == p:
                            temp += sum(w[r][t,:,i])
                m.addConstr( temp <= C)

        # Objective is to minimize delay
        delay_time = 0
        for f in range(flight_num):
            for r in range(R):
                delay_time += (A[f, r]-S[self.route_id[r]][f])
        # print(delay_time)
        # print('before')
        # Optimization process
        m.setObjective(delay_time, GRB.MINIMIZE)
        # print('after')
        # m.write("../result/master1.lp")

        m.optimize()

        if m.status == GRB.Status.OPTIMAL:
            # solution = m.getAttr('x')
            # print(len(solution))
            schedule_table = []
            for r in range(R):
                for i in range(flight_num):
                    schedule_table.append(((round(A[i,r].x), self.route_id[r])))

            return (m.objVal, schedule_table)

        else:
            return (self.infeasibility, [])

