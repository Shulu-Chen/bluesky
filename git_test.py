import matplotlib.pyplot as plt
from random import expovariate
l=[]

ac_number=10
lambda_x = 0.1
ac_demand_interval = [int(expovariate(lambda_x)) for i in range(ac_number)]
print(ac_demand_interval)