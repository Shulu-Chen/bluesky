import random
import numpy as np
from gurobipy import *

from sequencing.evtol_performance import eVTOL


class ComputeRTA():
    '''
    This functions is used to compute RTA for a set of ac.
    Input:
        - num: number of ac,
        - ETA_list
        - Cruise_Speed_list
        - Max_Speed_list
        - Descent_time: Descent time of each ac
    '''

    def __init__(self, num, ETA_list, cruise_speed_list, max_speed_list, descent_time=60, waiting_time = 3600):
        self.num = num
        self.ac_list = []
        self.descent_time = descent_time
        self.infeasibility = -1
        for i in range(num):
            self.ac_list.append(eVTOL(i, ETA_list[i], cruise_speed_list[i], max_speed_list[i], waiting_time))

    def show_status(self):
        '''
        Output: the initial index, earliest_ETA, ETA and Latest_ETA of each aircraft.
        '''
        print(f"ac_number  earliest_ETA  normal_ETA  Latest_ETA")
        for ac in self.ac_list:
            print(f"{ac.original_sequence_number:9}  {ac.earliest_ETA:6f}  {ac.ETA:6f}  {ac.latest_ETA:6f}")

    def get_RTA(self):
        '''
        Return the list of RTA.
        '''
        (obj, RTA_list) = self._Gurobi_Optimization_Method()
        if (obj == self.infeasibility):
            print("Warning: RTA can not be computed by Gurobi solver!")
        else:
            return RTA_list

    def _Gurobi_Optimization_Method(self):
        # Rotorcraft_Separation = 173 # Time for vertical descent 173 sec
        # Fixedwing_Separation = 151 # Time for vertical descent 151 sec
        # Gurobi Optimization
        urban_air_mobility = self.ac_list
        descent_time = self.descent_time
        k = self.num

        # Create an empty model
        m = Model('Scheduling')
        m.Params.LogToConsole = 0
        # Creating empty list for decision variables i.e. Required Time of Arrival
        x = []

        # Adding decision variables i.e. RTA
        x = m.addVars(k, lb=0, ub=1000000, vtype=GRB.CONTINUOUS, name='RTA')

        # Adding upper bounds as constraints
        # m.addConstrs((x[index] <= urban_air_mobility[index].latest_ETA for index in range(k)), name='c0')

        # Adding lower bounds as constraints
        m.addConstrs((-x[index] <= -urban_air_mobility[index].earliest_ETA for index in range(k)), name='c1')

        # Adding Separation constraints
        for index in range(k - 1):
            m.addConstr(descent_time <= x[index + 1] - x[index], "e2")

        # Objective is to minimize Makespan
        makespan = x[k - 1]

        # Optimization process
        m.setObjective(makespan, GRB.MINIMIZE)

        m.optimize()

        if m.status == GRB.Status.OPTIMAL:
            solution = m.getAttr('x')
            return (m.objVal, [round(m.x[i]) for i in range(k)])
        else:
            return (self.infeasibility, [])

