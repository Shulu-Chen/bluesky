import random
from tqdm import tqdm

from supports.support_methods import SupportMethods
from supports.operation_generator import OperationGenerator


T_MAX = 10000  # second
INTERVAL = 10
AC_NUM = [10, 10]
CHECK_INV = 100  # second
CONTROL_INV = 100  # second
MERGE_CAPACITY = 1
BLOCK_SIZE = 100  # second

n_steps = int(T_MAX + 1)
AC_INV = [INTERVAL, INTERVAL]

U_current_ac = 0
D_current_ac = 0
U_number = AC_NUM[0]
D_number = AC_NUM[1]
U_flight_interval = AC_INV[0]
D_flight_interval = AC_INV[1]
U_depart_time, U_depart_time_ori = SupportMethods.generate_interval(U_flight_interval, U_number)
D_depart_time, D_depart_time_ori = SupportMethods.generate_interval(D_flight_interval, D_number)
depart_table = {"U": U_depart_time, "D": D_depart_time}

OG = OperationGenerator(BLOCK_SIZE, MERGE_CAPACITY, depart_table)
OG.init_bs()
for t in tqdm(range(1, n_steps)):
    OG.update()
    U_first = random.choice([True, False])
    if U_first:
        if U_current_ac < U_number:
            if t >= U_depart_time[U_current_ac]:
                U_current_ac = OG.add_U_aircraft(t)

        if D_current_ac < D_number:
            if t >= D_depart_time[D_current_ac]:
                D_current_ac = OG.add_D_aircraft(t)

    else:
        if D_current_ac < D_number:
            if t >= D_depart_time[D_current_ac]:
                D_current_ac = OG.add_D_aircraft(t)

        if U_current_ac < U_number:
            if t >= U_depart_time[U_current_ac]:
                U_current_ac = OG.add_U_aircraft(t)

    if t % CHECK_INV == 0:
        OG.in_air_deconfliction(t)
safety, efficiency = OG.stop_bs(U_depart_time_ori, D_depart_time_ori)

print("*******************************")
print(f"number of LOS:{safety[0]}")
print(f"number of NMAC:{safety[1]}")
print(f"average delay:{round(efficiency)} s")
print("Flight interval=", INTERVAL)
print("*******************************")
# g=open("../result/Interval data.txt","a")
# g.write(f"{safety[0]},{inv},LOS\n")
# g.write(f"{safety[1]},{inv},NMAC\n")
# g.write(f"{round(efficiency)},{inv},Ground Delay\n")

