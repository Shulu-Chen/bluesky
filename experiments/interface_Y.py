import random
import copy
from tqdm import tqdm

from supports.support_methods import SupportMethods
from supports.operation_generator import OperationGenerator
from sequencing.compute_RTA import ComputeRTA


T_MAX = 3000  # second
INTERVAL = 10
AC_NUM = [5, 5]
CHECK_INV = 100  # second
CONTROL_INV = 100  # second
MERGE_CAPACITY = 1
BLOCK_SIZE = 100  # second

def generate_departure_table():
    AC_INV = [INTERVAL, INTERVAL]
    U_flight_interval = AC_INV[0]
    D_flight_interval = AC_INV[1]
    U_depart_time = SupportMethods.generate_interval(U_flight_interval, AC_NUM[0])
    D_depart_time = SupportMethods.generate_interval(D_flight_interval, AC_NUM[1])
    depart_table = {"U": U_depart_time, "D": D_depart_time}
    return depart_table


def sim_run(block_size, merge_capacity, departure_table):
    ori_departure_table = departure_table.copy()
    n_steps = int(T_MAX + 1)
    U_current_ac = 0
    D_current_ac = 0
    U_number = AC_NUM[0]
    D_number = AC_NUM[1]
    OG = OperationGenerator(block_size, merge_capacity, departure_table)
    OG.init_bs()
    for t in tqdm(range(1, n_steps)):
        OG.update()
        U_first = random.choice([True, False])
        if U_first:
            if U_current_ac < U_number:
                if t >= departure_table['U'][U_current_ac]:
                    U_current_ac = OG.add_U_aircraft(t)

            if D_current_ac < D_number:
                if t >= departure_table['D'][D_current_ac]:
                    D_current_ac = OG.add_D_aircraft(t)

        else:
            if D_current_ac < D_number:
                if t >= departure_table['D'][D_current_ac]:
                    D_current_ac = OG.add_D_aircraft(t)

            if U_current_ac < U_number:
                if t >= departure_table['U'][U_current_ac]:
                    U_current_ac = OG.add_U_aircraft(t)

        if t % CHECK_INV == 0:
            OG.in_air_deconfliction(t)

    return OG.stop_bs(ori_departure_table['U'], ori_departure_table['D'])


g=open("../result/Interval data.txt","a")
for i in [1, 10, 20]:
    depart_table = generate_departure_table()
    safety, efficiency = sim_run(BLOCK_SIZE, i, depart_table)
    g.write(f"{safety[0]},{INTERVAL},LOS\n")
    g.write(f"{safety[1]},{INTERVAL},NMAC\n")
    g.write(f"{round(efficiency)},{INTERVAL},Ground Delay\n")

print("*******************************")
print(f"number of LOS:{safety[0]}")
print(f"number of NMAC:{safety[1]}")
print(f"average delay:{round(efficiency)} s")
print("Flight interval=", INTERVAL)
print("*******************************")



