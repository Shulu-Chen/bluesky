import numpy as np
from geopy.distance import geodesic
from math import sqrt
from random import expovariate

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
    def generate_interval(interval, number):
        '''
        Generate the demand based on exponential distribution, lambda-number of flight per second,
        lambda=0.1--flight interval=10s
        '''
        lambda_x = 1/interval
        ac_demand_interval = [int(expovariate(lambda_x)) for i in range(number)]
        depart_time = np.cumsum(ac_demand_interval)
        return depart_time

