import os
import time
import sys
import json
import numpy as np
sys.path.append("../")
from supports.support_methods import SupportMethods


INTERVALS = [30]
CAPACITIES = [5]   #[2,3,4,5,6,7,8,9,10,11]
TEST_NUM = 1       #30
AC_NUM = 10

for c in CAPACITIES:
    for i in INTERVALS:
        result = {"ground_delay":[],"capacity":c, "interval":i}
        for id in range(TEST_NUM):
            delay = SupportMethods.generate_scenario_file(id, "hybird", capacity=c, interval=i, plot_image=False, ac_num=AC_NUM)
            result['ground_delay'].append(delay)
        result['ground_delay_mean'] = np.mean(result['ground_delay'])
        result['ground_delay_std'] = np.std(result['ground_delay'])
        json_object = json.dumps(result, indent=4)

        if not os.path.exists("..\\result\\ground_delay"):
            os.makedirs("..\\result\\ground_delay")

        with open(f"..\\result\\ground_delay\\delay_{i}_{c}.json", "w") as outfile:
            outfile.write(json_object)

