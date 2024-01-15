import random

SPEED_LIST = [64, 66, 68, 70]

class OperationWriter():

    def __init__(self,
                 scn_name,
                 log=False,
                 log_name="TerminalLog"):

        scn_path = scn_name
        self.f = open(scn_path, "w")
        self.log = log
        self.log_name = log_name

    def init_scn(self):
        if self.log:
            self.f.write(f"00:00:00.00>CRELOG {self.log_name}_gui 1\n")
            self.f.write(f"00:00:00.00>{self.log_name}_gui ADD id,lat, lon, alt, tas, vs\n")
            self.f.write(f"00:00:00.00>{self.log_name}_gui ON 1\n")

        self.f.write("00:00:00.00>TRAILS ON \n")
        self.f.write("00:00:00.00>TAXI OFF 4\n")
        self.f.write("0:00:00.00>PAN 30, -90 \n")
        self.f.write("0:00:00.00>ZOOM 3 \n")
        self.f.write("00:00:00.00>CIRCLE a, 30.0, -90.0 0.5\n")
        self.f.write("0:00:00.00>FF \n")
        self.f.write("\n")

    def generate_merge_file(self, schedule_table):
        id = 0
        for p in schedule_table:
            orig = p[1]
            time = p[0]

            if orig=="U":

                acid="U"+str(time)

                self.f.write(f"00:00:{time}.00>CRE {acid} EC35 N_7 0 0\n")
                self.f.write(f"00:00:{time}.00>ORIG {acid} N_7\n")
                self.f.write(f"00:00:{time}.00>DEST {acid} N_3\n")

                v = random.choice(SPEED_LIST)
                self.f.write(f"00:00:{time}.00>SPD {acid} {v}\n")
                self.f.write(f"00:00:{time}.00>ALT {acid} 400\n")

                v = random.choice(SPEED_LIST)
                self.f.write(f"00:00:{time}.00>ADDWPT {acid} N_1, 400, {v}\n")

                v = random.choice(SPEED_LIST)
                self.f.write(f"00:00:{time}.00>ADDWPT {acid} N_2, 400, {v}\n")
                self.f.write(f"00:00:{time}.00>VNAV {acid} ON\n")
                self.f.write("\n")

            if orig=="D":
                acid="D"+str(time)
                self.f.write(f"00:00:{time}.00>CRE {acid} EC35 N_9 0 0\n")
                self.f.write(f"00:00:{time}.00>ORIG {acid} N_9\n")
                self.f.write(f"00:00:{time}.00>DEST {acid} N_3\n")

                v = random.choice(SPEED_LIST)
                self.f.write(f"00:00:{time}.00>SPD {acid} {v}\n")
                self.f.write(f"00:00:{time}.00>ALT {acid} 400\n")

                v = random.choice(SPEED_LIST)
                self.f.write(f"00:00:{time}.00>ADDWPT {acid} N_1, 400, {v}\n")

                v = random.choice(SPEED_LIST)


                self.f.write(f"00:00:{time}.00>ADDWPT {acid} N_2, 400, {v}\n")
                self.f.write(f"00:00:{time}.00>VNAV {acid} ON\n")
                self.f.write("\n")

    def generate_cross_file(self, schedule_table):
        id = 0
        for p in schedule_table:
            orig = p[1]
            time = p[0]

            if orig=="U":

                acid="U"+str(time)

                self.f.write(f"00:00:{time}.00>CRE {acid} EC35 N_7 0 0\n")
                self.f.write(f"00:00:{time}.00>ORIG {acid} N_7\n")
                self.f.write(f"00:00:{time}.00>DEST {acid} M_4\n")

                v = random.choice(SPEED_LIST)
                self.f.write(f"00:00:{time}.00>SPD {acid} {v}\n")
                self.f.write(f"00:00:{time}.00>ALT {acid} 400\n")

                v = random.choice(SPEED_LIST)
                self.f.write(f"00:00:{time}.00>ADDWPT {acid} N_1, 400, {v}\n")

                self.f.write(f"00:00:{time}.00>VNAV {acid} ON\n")
                self.f.write("\n")

            if orig=="D":
                acid="D"+str(time)
                self.f.write(f"00:00:{time}.00>CRE {acid} EC35 N_9 0 0\n")
                self.f.write(f"00:00:{time}.00>ORIG {acid} N_9\n")
                self.f.write(f"00:00:{time}.00>DEST {acid} M_2\n")

                v = random.choice(SPEED_LIST)
                self.f.write(f"00:00:{time}.00>SPD {acid} {v}\n")
                self.f.write(f"00:00:{time}.00>ALT {acid} 400\n")

                v = random.choice(SPEED_LIST)
                self.f.write(f"00:00:{time}.00>ADDWPT {acid} N_1, 400, {v}\n")

                self.f.write(f"00:00:{time}.00>VNAV {acid} ON\n")
                self.f.write("\n")


    def generate_hybird_file(self, schedule_table):
        id = 0
        for p in schedule_table:
            orig = p[1]
            time = p[0]

            if orig=="U":

                acid="U"+str(time)

                self.f.write(f"00:00:{time}.00>CRE {acid} EC35 N_7 0 0\n")
                self.f.write(f"00:00:{time}.00>ORIG {acid} N_7\n")
                self.f.write(f"00:00:{time}.00>DEST {acid} N_3\n")

                v = random.choice(SPEED_LIST)
                self.f.write(f"00:00:{time}.00>SPD {acid} {v}\n")
                self.f.write(f"00:00:{time}.00>ALT {acid} 400\n")

                v = random.choice(SPEED_LIST)
                self.f.write(f"00:00:{time}.00>ADDWPT {acid} N_1, 400, {v}\n")

                v = random.choice(SPEED_LIST)
                self.f.write(f"00:00:{time}.00>ADDWPT {acid} N_2, 400, {v}\n")
                self.f.write(f"00:00:{time}.00>VNAV {acid} ON\n")
                self.f.write("\n")

            if orig=="D":
                acid="D"+str(time)
                self.f.write(f"00:00:{time}.00>CRE {acid} EC35 N_9 0 0\n")
                self.f.write(f"00:00:{time}.00>ORIG {acid} N_9\n")
                self.f.write(f"00:00:{time}.00>DEST {acid} N_3\n")

                v = random.choice(SPEED_LIST)
                self.f.write(f"00:00:{time}.00>SPD {acid} {v}\n")
                self.f.write(f"00:00:{time}.00>ALT {acid} 400\n")

                v = random.choice(SPEED_LIST)
                self.f.write(f"00:00:{time}.00>ADDWPT {acid} N_1, 400, {v}\n")

                v = random.choice(SPEED_LIST)


                self.f.write(f"00:00:{time}.00>ADDWPT {acid} N_2, 400, {v}\n")
                self.f.write(f"00:00:{time}.00>VNAV {acid} ON\n")
                self.f.write("\n")

            if orig=="C":
                acid="C"+str(time)
                self.f.write(f"00:00:{time}.00>CRE {acid} EC35 M_2 0 0\n")
                self.f.write(f"00:00:{time}.00>ORIG {acid} M_2\n")
                self.f.write(f"00:00:{time}.00>DEST {acid} M_4\n")

                v = random.choice(SPEED_LIST)
                self.f.write(f"00:00:{time}.00>SPD {acid} {v}\n")
                self.f.write(f"00:00:{time}.00>ALT {acid} 400\n")

                v = random.choice(SPEED_LIST)
                self.f.write(f"00:00:{time}.00>ADDWPT {acid} N_2, 400, {v}\n")

                self.f.write(f"00:00:{time}.00>VNAV {acid} ON\n")
                self.f.write("\n")

    def end_generator(self):
        print("Save scenario file successfully")
        self.f.close()

