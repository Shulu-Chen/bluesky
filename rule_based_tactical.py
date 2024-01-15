import os
import json
from tqdm import tqdm
import numpy as np
import pandas as pd
import bluesky as bs
from bluesky.tools import geo

from supports.support_methods import SupportMethods


# Bluesky settings
T_STEP = 10000
MANEUVER = True
GUI = False
LOG = True
SIMDT = 1

# experiment parameters
INTERVAL = [30]  # [60, 120]
CAPACITY = [5]  # [2,3,4,5,6,7,8,9,10,11]

# Rule-based tactical deconfliction parameters
MAC_DIST = 10
NMAC_DIST = 150
LOWC_DIST = 500
INTURDER_DIST = 1000
SPEED_UP_DIST = 700
FINISH_DIST = 100
SPEED = [10, 70]
DELTA_SPD = 5


def in_air_deconfliction(t, traf, land_list, loc_list):
    mac = 0
    nmac = 0
    lowc = 0
    counter = 0
    n_ac = traf.lat.shape[0]
    index = np.arange(n_ac).reshape(-1, 1)
    goal_dist_dic = {}

    ## calculating the distance from each aircraft to all others. Will result in a n_ac x n_ac matrix
    d = (
        geo.kwikdist_matrix(
            np.repeat(traf.lat, n_ac),
            np.repeat(traf.lon, n_ac),
            np.tile(traf.lat, n_ac),
            np.tile(traf.lon, n_ac),
        ).reshape(n_ac, n_ac)
        * geo.nm
    )

    for k in range(d.shape[0]):
        glat, glon = traf.ap.route[k].wplat[-2], traf.ap.route[k].wplon[-2]
        goal_dist = (
            geo.kwikdist(traf.lat[k], traf.lon[k], glat, glon) * geo.nm
        )  ##meters
        goal_dist_dic[traf.id[k]] = goal_dist
        if goal_dist < FINISH_DIST:
            land_list[traf.id[k]] = t
    argsort = np.array(np.argsort(d, axis=1))

    for i in range(d.shape[0]):
        id_ = traf.id[i]

        ahead_ac = [
            traf.id2idx(ac_id)
            for ac_id in traf.id
            if goal_dist_dic[ac_id] < goal_dist_dic[id_]
        ]

        equal_ac = [
            traf.id2idx(ac_id)
            for ac_id in traf.id
            if goal_dist_dic[ac_id] == goal_dist_dic[id_] and ac_id != id_
        ]

        # speed up if distance with all ahead aircraft is larger than the throughold
        if all(d[i, k] > SPEED_UP_DIST for k in ahead_ac):
            current_spd = int(np.round((traf.cas[traf.id2idx(id_)] / geo.nm) * 3600))
            speed = min(current_spd + DELTA_SPD, SPEED[1])
            if speed != current_spd and t % SIMDT == 0 and MANEUVER == True:
                bs.stack.stack(f"SPD {id_} {speed}")
                f.write(f"00:00:{t}.00>SPD {id_} {speed}\n")
                f.write(f"00:00:{t}.00>COLOR {id_} 0,255,0\n")
                counter += 1

        for j in range(len(argsort[i])):
            index = int(argsort[i][j])

            # intruder == ownship so we need to skip
            if i == index:
                continue

            # if the intruder is > 1500 meters away, speed up.
            if d[i, index] > INTURDER_DIST:
                continue

            # if the intruder is behind, skip it
            if index not in ahead_ac:
                continue

            if d[i, index] < MAC_DIST:
                # if t % SIMDT == 0:
                mac += 1
                bs.stack.stack(f"DEL {id_}")
                f.write(f"00:00:{t}.00>DEL {id_}\n")
                f.write(f"00:00:{t}.00>ECHO NMAC between {id_} {traf.id[index]}\n")
                continue

            else:
                if d[i, index] <= LOWC_DIST and t % SIMDT == 0:
                    lowc += 1
                if d[i, index] <= NMAC_DIST and t % SIMDT == 0:
                    nmac += 1
                    loc_list["lon"].append(traf.lon[index])
                    loc_list["lat"].append(traf.lat[index])
                current_spd = int(
                    np.round((traf.cas[traf.id2idx(id_)] / geo.nm) * 3600)
                )
                speed = max(current_spd - DELTA_SPD, SPEED[0])
                if speed != current_spd and t % SIMDT == 0 and MANEUVER == True:
                    bs.stack.stack(f"SPD {id_} {speed}")
                    f.write(f"00:00:{t}.00>SPD {id_} {speed}\n")
                    f.write(f"00:00:{t}.00>COLOR {id_} yellow\n")
                    # f.write(f"00:00:{t}.00>ECHO {id_} detect intruder {traf.id[index]}\n")
                    counter += 1
                continue

    return mac, nmac, lowc, counter


def evaluate_scenario(scn_file, result_dic, location):
    if not GUI:
        bs.init(mode="sim", detached=True)
    else:
        bs.init(mode="sim")
        bs.net.connect()

    bs.stack.stack("IC " + scn_file)
    bs.stack.stack("DT 1; FF")

    if LOG:
        bs.stack.stack(f"CRELOG rb 1")
        bs.stack.stack(f"rb  ADD id, lat, lon, alt, tas, vs, hdg")
        bs.stack.stack(f"rb  ON 1  ")
    total_lowc_num = 0
    total_nmac_num = 0
    total_mac_num = 0
    total_speed_change = 0
    landing_list = {}

    for T in tqdm(range(T_STEP)):
        bs.sim.step()
        # if T%SIMDT == 0:
        # add_speed_disturb(int(bs.sim.simt), bs.traf)
        mac_num, nmac_num, lowc_num, speed_change = in_air_deconfliction(
            int(bs.sim.simt), bs.traf, landing_list, location
        )
        total_lowc_num += lowc_num
        total_nmac_num += nmac_num
        total_mac_num += mac_num
        total_speed_change += speed_change

    f.close()

    SupportMethods.merge_scn_file(
        f"scenario/{SCN_PATH}/{SCN_NAME}",
        f"scenario/{SCN_PATH}/rb_{SCN_NAME}",
        "scenario/rb_result.scn",
    )

    fly_time = 0
    for ac in landing_list.items():
        fly_time += int(ac[1]) - int(ac[0][1:])
        final_landing_time = int(ac[1])

    result_dic["LOWC"].append(total_lowc_num)
    result_dic["est_MAC"].append(total_nmac_num * 0.005038 * 0.005 / fly_time * 3600)
    result_dic["NMAC"].append(total_nmac_num)
    result_dic["MAC"].append(total_mac_num)
    result_dic["avg_speed_change"].append(round(total_speed_change / 30, 2))
    result_dic["flying_time"].append(round(fly_time / len(landing_list), 2))
    result_dic["throughput"].append(round(30 / final_landing_time * 3600, 2))


for inter in INTERVAL:
    for c in CAPACITY:
        SCN_PATH = f"hybird_{inter}_{c}_test"
        result = {
            "LOWC": [],
            "NMAC": [],
            "est_MAC": [],
            "MAC": [],
            "avg_speed_change": [],
            "flying_time": [],
            "throughput": [],
        }
        location = {"lon": [], "lat": []}
        for i in range(1):
            file_id = i
            SCN_NAME = f"{file_id}.scn"
            f = open(f"scenario/{SCN_PATH}/rb_{SCN_NAME}", "w")
            evaluate_scenario(SCN_PATH + "/" + SCN_NAME, result, location)
            df = pd.DataFrame(location)
            df.to_csv(f"result\\{SCN_PATH}_rb.csv", index=False)

        result["avg_speed_change_mean"] = round(np.mean(result["avg_speed_change"]), 1)
        result["flying_time_mean"] = round(np.mean(result["flying_time"]), 1)
        result["MAC_mean_ft"] = round(
            np.mean(result["MAC"]) * 3600 / (np.sum(result["flying_time"])), 3
        )
        lowc_ft = []
        nmac_ft = []
        for i in range(len(result["LOWC"])):
            lowc_ft.append(result["LOWC"][i] * 3600 / (result["flying_time"][i] * 30))
            nmac_ft.append(result["NMAC"][i] * 3600 / (result["flying_time"][i] * 30))
        result["LOWC_mean_ft"] = round(np.mean(lowc_ft), 1)
        result["LOWC_std_ft"] = round(np.std(lowc_ft), 1)
        result["NMAC_mean_ft"] = round(np.mean(nmac_ft), 3)
        result["NMAC_std_ft"] = round(np.std(nmac_ft), 3)
        result["est_MAC_mean"] = round(np.mean(result["est_MAC"]), 9)
        result["est_MAC_std"] = round(np.std(result["est_MAC"]), 9)
        print(result)

        json_object = json.dumps(result, indent=4)

        if not os.path.exists("result\\rule_based"):
            os.makedirs("result\\rule_based")

        with open(f"result\\rule_based\\{SCN_PATH}.json", "w") as outfile:
            outfile.write(json_object)
