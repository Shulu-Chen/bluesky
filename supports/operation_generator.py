import random
import itertools
import numpy as np

import bluesky as bs
from supports.support_methods import SupportMethods

SPEED_LIST = [30,31,32,33,34]
SCN_PATH = '../scenario/interface_Y.scn'

class OperationGenerator():

    def __init__(self, block_size, capacity, depart_table,
                 scn_path = SCN_PATH,
                 depart_bound = 10,     #seconds
                 t_max = 10000,         #seconds
                 merge_time = 1015,     #seconds
                 warning_dist = 600,    #meters
                 speed_up_dist = 800,   #meters
                 LOS_dist = 100,        #meters
                 NMAC_dist = 10,        #meters
                 delta_v = 5,           #kts
                 max_speed = 40,        #kts
                 min_speed = 3):        #kts

        bs.init(mode='sim', detached=True)
        self.f = open(scn_path, "w")
        self.ac_list = []
        self.alt_list = []
        self.lat_list = []
        self.lon_list = []
        self.spd_list = []
        self.depart_bound = depart_bound
        self.block_size = block_size
        self.capacity = capacity
        self.merge_time = merge_time
        self.warning_dist = warning_dist
        self.speed_up_dist = speed_up_dist
        self.delta_v = delta_v
        self.max_speed = max_speed
        self.min_speed = min_speed
        self.NMAC_dist = NMAC_dist
        self.LOS_dist = LOS_dist
        self.depart_table = depart_table
        self.check_block = np.zeros(round(t_max * 2 / block_size))
        self.check_block[int(merge_time / block_size)] += 1
        self.U_current_ac = 0
        self.D_current_ac = 0
        self.LOS = 0
        self.NMAC = 0
        self.U_id = ''
        self.D_id = ''
        self.operate_dic = {}


    def init_bs(self, log=False, log_name="TerminalLog"):
        if log:
            bs.stack.stack(f'CRELOG {log_name} 1')
            bs.stack.stack(f'{log_name}  ADD id,lat, lon, alt, tas, vs ')
            bs.stack.stack(f'{log_name}  ON 1  ')
            self.f.write(f"00:00:00.00>CRELOG {log_name}_gui 1\n")
            self.f.write(f"00:00:00.00>{log_name}_gui ADD id,lat, lon, alt, tas, vs\n")
            self.f.write(f"00:00:00.00>{log_name}_gui ON 1\n")

        # bs.stack.stack('ASAS ON')
        bs.stack.stack('TAXI OFF 4')
        self.f.write("00:00:00.00>TRAILS ON \n")
        self.f.write("00:00:00.00>TAXI OFF 4\n")
        # f.write("0:00:00.00>ASAS ON \n")
        self.f.write("0:00:00.00>PAN 0,0.2 \n")
        self.f.write("0:00:00.00>ZOOM 3 \n")
        self.f.write("00:00:00.00>CIRCLE a, 0.0,0.0 0.2\n")
        self.f.write("0:00:00.00>FF \n")
        self.f.write("\n")
        # set simulation time step, and enable fast-time running
        bs.stack.stack('DT 1;FF')
        bs.traf.cre(acid="U" + str(0), actype="ELE01", aclat=0.1, aclon=-0.1)
        self.add_plane(0, "U")

    def add_plane(self, id, type):
        if type=="U":

            acid="U"+str(id)

            bs.stack.stack(f'ORIG {acid} N_7')
            bs.stack.stack(f'DEST {acid} N_4')
            self.f.write(f"00:00:{id}.00>CRE {acid} ELE01 N_7 0 0\n")
            self.f.write(f"00:00:{id}.00>ORIG {acid} N_7\n")
            self.f.write(f"00:00:{id}.00>DEST {acid} N_4\n")

            v = random.choice(SPEED_LIST)
            bs.stack.stack(f'SPD {acid} {v}')
            self.f.write(f"00:00:{id}.00>SPD {acid} {v}\n")

            bs.stack.stack(f'ALT {acid} 400')
            self.f.write(f"00:00:{id}.00>ALT {acid} 400\n")

            v = random.choice(SPEED_LIST)
            bs.stack.stack(f'ADDWPT {acid} N_1, 400, {v}')
            self.f.write(f"00:00:{id}.00>ADDWPT {acid} N_1, 400, {v}\n")

            v = random.choice(SPEED_LIST)
            bs.stack.stack(f'ADDWPT {acid} N_2, 400, {v}')
            self.f.write(f"00:00:{id}.00>ADDWPT {acid} N_2, 400, {v}\n")

            v = random.choice(SPEED_LIST)
            bs.stack.stack(f'ADDWPT {acid} N_3, 400, {v}')
            self.f.write(f"00:00:{id}.00>ADDWPT {acid} N_3, 400, {v}\n")

            bs.stack.stack(f'VNAV {acid} ON')
            self.f.write(f"00:00:{id}.00>VNAV {acid} ON\n")

        if type=="D":

            acid="D"+str(id)

            bs.stack.stack(f'ORIG {acid} N_9')
            bs.stack.stack(f'DEST {acid} N_4')

            self.f.write(f"00:00:{id}.00>CRE {acid} ELE01 N_9 0 0\n")
            self.f.write(f"00:00:{id}.00>ORIG {acid} N_9\n")
            self.f.write(f"00:00:{id}.00>DEST {acid} N_4\n")

            v = random.choice(SPEED_LIST)
            bs.stack.stack(f'SPD {acid} {v}')
            self.f.write(f"00:00:{id}.00>SPD {acid} {v}\n")

            bs.stack.stack(f'ALT {acid} 400')
            self.f.write(f"00:00:{id}.00>ALT {acid} 400\n")

            v = random.choice(SPEED_LIST)
            bs.stack.stack(f'ADDWPT {acid} N_1, 400, {v}')
            self.f.write(f"00:00:{id}.00>ADDWPT {acid} N_1, 400, {v}\n")

            v = random.choice(SPEED_LIST)
            bs.stack.stack(f'ADDWPT {acid} N_2, 400, {v}')
            self.f.write(f"00:00:{id}.00>ADDWPT {acid} N_2, 400, {v}\n")

            v = random.choice(SPEED_LIST)
            bs.stack.stack(f'ADDWPT {acid} N_3, 400, {v}')
            self.f.write(f"00:00:{id}.00>ADDWPT {acid} N_3, 400, {v}\n")

            self.f.write(f"00:00:{id}.00>VNAV {acid} ON\n")
            bs.stack.stack(f'VNAV {acid} ON')

        self.f.write("\n")

    def update(self):
        bs.sim.step()
        self.ac_list = bs.traf.id
        self.alt_list = bs.traf.alt
        self.lat_list = bs.traf.lat
        self.lon_list = bs.traf.lon
        self.spd_list = bs.traf.tas

    def add_U_aircraft(self, time):
        if len(self.lat_list) >= 1:
            try:
                U_ind = self.ac_list.index(self.U_id)
                dep_dist = SupportMethods.get_distance([self.lat_list[U_ind],
                                                        self.lon_list[U_ind],
                                                        self.alt_list[U_ind]],
                                                       [0.1,-0.1,0])
            except:
                dep_dist = 10000
            if dep_dist > self.depart_bound and \
                    self.check_block[int((self.merge_time+
                                          self.depart_table['U'][self.U_current_ac])/
                                         self.block_size)] < self.capacity:
                bs.traf.cre(acid="U"+str(time), actype="ELE01", aclat=0.1, aclon=-0.1, acalt=0, acspd=3)
                self.add_plane(time, "U")
                self.U_id = "U"+str(time)
                self.check_block[int((self.merge_time +
                                      self.depart_table['U'][self.U_current_ac])/self.block_size)] += 1
                self.U_current_ac += 1
            else:
                self.depart_table['U'][self.U_current_ac:]=list(map(lambda x:x+1,
                                                                    self.depart_table['U'][self.U_current_ac:]))
        return self.U_current_ac

    def add_D_aircraft(self, time):
        if len(self.lat_list) >= 1:
            try:
                #check the shortest distance between origin and in-air aircraft
                D_ind = self.ac_list.index(self.D_id)
                dep_dist = SupportMethods.get_distance([self.lat_list[D_ind],
                                                        self.lon_list[D_ind],
                                                        self.alt_list[D_ind]],
                                                       [-0.1,-0.1,0])
            except:
                dep_dist = 10000
            if dep_dist > self.depart_bound and \
                    self.check_block[int((self.merge_time+
                                          self.depart_table['D'][self.D_current_ac])/
                                         self.block_size)] < self.capacity:
                bs.traf.cre(acid="D"+str(time), actype="ELE01", aclat=-0.1, aclon=-0.1, acalt=0, acspd=3)
                self.add_plane(time, "D")
                self.D_id = "D"+str(time)
                self.check_block[int((self.merge_time +
                                      self.depart_table['D'][self.D_current_ac])/self.block_size)] += 1
                self.D_current_ac += 1
            else:
                self.depart_table['D'][self.D_current_ac:]=list(map(lambda x:x+1,
                                                                    self.depart_table['D'][self.D_current_ac:]))

        return self.D_current_ac

    def in_air_deconfliction(self, time):
        '''
        For speed, input is kts, api output is m/s, the rate is 1.95
        '''

        if len(self.lat_list) <= 1 or len(self.lat_list) < len(self.ac_list):
            pass
        else:
            dist_list=[]
            ac_comb = list(itertools.combinations(self.ac_list, 2))

            for acs in ac_comb:
                ac1 = self.ac_list.index(acs[0])
                ac2 = self.ac_list.index(acs[1])
                loc1=[self.lat_list[ac1], self.lon_list[ac1], self.alt_list[ac1]]
                loc2=[self.lat_list[ac2], self.lon_list[ac2], self.alt_list[ac2]]
                dist_list.append(SupportMethods.get_distance(loc1, loc2))

            dist_list = np.array(dist_list)
            operate_comb_ids = np.where(dist_list < self.warning_dist)

            ### All clear
            if len(operate_comb_ids[0]) == 0 and len(self.operate_dic) == 0:
                pass

            ### Release the operate ac if larger distance
            if len(self.operate_dic) > 0:
                pop_list = []
                for operated_comb in self.operate_dic:
                    try:
                        ac1 = self.ac_list.index(operated_comb[0])
                        ac2 = self.ac_list.index(operated_comb[1])
                        loc1 = [self.lat_list[ac1], self.lon_list[ac1], self.alt_list[ac1]]
                        loc2 = [self.lat_list[ac2], self.lon_list[ac2], self.alt_list[ac2]]
                        operate_dist = SupportMethods.get_distance(loc1, loc2)

                        ## seperation large, speed up
                        if operate_dist > self.speed_up_dist:
                            operate_ac = self.ac_list.index(self.operate_dic[operated_comb])
                            speed = min(self.spd_list[operate_ac] * 1.93+ self.delta_v, self.max_speed)
                            bs.stack.stack(f"SPD {self.ac_list[operate_ac]} {speed}")
                            self.f.write(f"00:00:{time}.00>SPD {self.ac_list[operate_ac]} {speed} \n")
                            if self.spd_list[operate_ac] * 1.93 + self.delta_v >= self.max_speed:
                                pop_list.append(operated_comb)
                    except:
                        continue
                for pop_item in pop_list:
                    self.operate_dic.pop(pop_item)

            ### Speed down the opearate ac
            if len(operate_comb_ids[0]) > 0:

                for operate_comb_id in operate_comb_ids[0]:
                    dist = dist_list[operate_comb_id]
                    if dist > self.warning_dist:
                        continue
                    operate_acs = ac_comb[operate_comb_id]
                    ## compute who is the following one
                    operate_ac1 = self.ac_list.index(operate_acs[0])
                    operate_ac2 = self.ac_list.index(operate_acs[1])
                    ac1_lon = self.lon_list[operate_ac1]
                    ac2_lon = self.lon_list[operate_ac2]
                    if ac1_lon >= ac2_lon:
                        operate_ac = operate_ac2
                        keep_ac = operate_ac1
                        self.operate_dic[operate_acs] = operate_acs[1]
                    else:
                        operate_ac = operate_ac1
                        keep_ac = operate_ac2
                        self.operate_dic[operate_acs] = operate_acs[0]

                    if dist < self.warning_dist:  ## low seperation warning, speed down
                        speed = min(max(self.spd_list[operate_ac] * 1.93 -
                                        self.delta_v, self.min_speed), self.max_speed)
                        bs.stack.stack(f"SPD {self.ac_list[operate_ac]} {speed}")
                        self.f.write(f"00:00:{time}.00>SPD {self.ac_list[operate_ac]} {speed}\n")
                    if dist < self.LOS_dist:  ## too low seperation, force hover (nearly)
                        self.LOS += 1
                        bs.stack.stack(f"SPD {self.ac_list[operate_ac]} {self.min_speed}")
                        self.f.write(f"00:00:{time}.00>SPD {self.ac_list[operate_ac]} {self.min_speed}\n")

                    if dist < self.NMAC_dist:  ## near in-air crash
                        self.NMAC += 1


    def stop_bs(self, U_depart_time_ori, D_depart_time_ori):
        self.f.close()
        bs.stack.stack('STOP')
        efficiency = \
            (np.mean(self.depart_table['U'] - U_depart_time_ori) + np.mean(self.depart_table['D']  -D_depart_time_ori)) / 2
        return [self.LOS, self.NMAC],efficiency


