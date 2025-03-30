import random
import datetime


# setup reads
metar_lookup_dict = {}
metar_lookup_dict['00'] = ""
metar_lookup_dict['01'] = "BR"
metar_lookup_dict['02'] = "DU"
metar_lookup_dict['03'] = "HZ"
metar_lookup_dict['04'] = "-GR"
metar_lookup_dict['05'] = "GR"
metar_lookup_dict['06'] = "+GR"
metar_lookup_dict['07'] = "SG"
metar_lookup_dict['08'] = "IC"
metar_lookup_dict['21'] = "BCF"
metar_lookup_dict['22'] = "-FG"
metar_lookup_dict['23'] = "FG"
metar_lookup_dict['24'] = "+FG"
metar_lookup_dict['25'] = "-FZFG"
metar_lookup_dict['26'] = "FZFG"
metar_lookup_dict['27'] = "+FZFG"
metar_lookup_dict['28'] = "FZBCFG"
metar_lookup_dict['31'] = "-DZ"
metar_lookup_dict['32'] = "DZ"
metar_lookup_dict['33'] = "+DZ"
metar_lookup_dict['34'] = "-FZDZ"
metar_lookup_dict['35'] = "FZDZ"
metar_lookup_dict['36'] = "+FZDZ"
metar_lookup_dict['37'] = "-DZRA"
metar_lookup_dict['38'] = "DZRA"
metar_lookup_dict['39'] = "+DZRA"
metar_lookup_dict['41'] = "-RA"
metar_lookup_dict['42'] = "RA"
metar_lookup_dict['43'] = "+RA"
metar_lookup_dict['44'] = "-FZRA"
metar_lookup_dict['45'] = "FZRA"
metar_lookup_dict['46'] = "+FZRA"
metar_lookup_dict['47'] = "-RASN"
metar_lookup_dict['48'] = "RASN"
metar_lookup_dict['49'] = "+RASN"
metar_lookup_dict['51'] = "-SN"
metar_lookup_dict['52'] = "SN"
metar_lookup_dict['53'] = "+SN"
metar_lookup_dict['54'] = "-SNRA"
metar_lookup_dict['55'] = "SNRA"
metar_lookup_dict['56'] = "+SNRA"
metar_lookup_dict['57'] = "-PL"
metar_lookup_dict['58'] = "PL"
metar_lookup_dict['59'] = "+PL"
metar_lookup_dict['61'] = "-SHRA"
metar_lookup_dict['62'] = "SHRA"
metar_lookup_dict['63'] = "+SHRA"
metar_lookup_dict['64'] = "-SHSN"
metar_lookup_dict['65'] = "SHSN"
metar_lookup_dict['66'] = "+SHSN"
metar_lookup_dict['71'] = "-SHRASN"
metar_lookup_dict['72'] = "SHRASN"
metar_lookup_dict['73'] = "+SHRASN"
metar_lookup_dict['74'] = "-SHSNRA"
metar_lookup_dict['75'] = "SHSNRA"
metar_lookup_dict['76'] = "+SHSNRA"
metar_lookup_dict['81'] = "-SHPL"
metar_lookup_dict['82'] = "SHPL"
metar_lookup_dict['83'] = "+SHPL"
metar_lookup_dict['84'] = "-SHGR"
metar_lookup_dict['85'] = "SHGR"
metar_lookup_dict['86'] = "+SHGR"
metar_lookup_dict['87'] = "-SHSG"
metar_lookup_dict['88'] = "SHSG"
metar_lookup_dict['89'] = "+SHSG"
metar_lookup_dict['97'] = "UN"
metar_lookup_dict['98'] = ""
metar_lookup_dict['99'] = ""



# import data from Bureau's in-house OMD format.
# this gets the task done, but is not elegant!!!

def get_obs_data(filepath="", retrieve_random=False, obs_count=-1, start_pos=0, end_pos=0):
    airport_file = open(filepath)

    airport_data = airport_file.readlines()

    if retrieve_random:
        start_pos = random.randrange(len(airport_data))
        end_pos = start_pos

    need_more = False
    if obs_count > 0:
        start_pos = 0
        end_pos = len(airport_data)
        need_more = True
        done_count = 0

    return_list = []

    aws_tags = ["DATE", "TIME", "CL", "CL30", "VI", "VI10", "WX1ME", "WS", "WD", "AT:", "DP", "RH", "RF", "QFE", "QNH", "QFF", "TI:", "BV"]
    good_tag_count = 0

    data_pos = start_pos
    aws_data = {"station_wsi": "0-20000-0-94975"}
    at_least_one_good = False
    while data_pos <= end_pos or at_least_one_good == False or need_more == True:
        aad = airport_data[data_pos]

        aad_cols = aad.split(' ')
        for tag in aws_tags:
            for aad_col in aad_cols:
                if tag in aad_col:
                    if tag == "DATE":
                        date_cols = aad_col.split(":")
                        date_text = date_cols[-1]
                        date_year = int(date_text[0:4])
                        date_month = int(date_text[4:6])
                        date_day = int(date_text[6:8])
                        aws_data['date'] = datetime.datetime(date_year, date_month, date_day)
                        good_tag_count += 1
                        break
                    elif tag == "TIME":
                        time_cols = aad_col.split(":")
                        time_hour = int(time_cols[1][:2])
                        time_minute = int(time_cols[1][2:4])
                        aws_data['time'] = datetime.time(time_hour, time_minute)
                        good_tag_count += 1
                        break
                    elif tag == "CL":
                        cl_cols = aad_col.split(":")
                        cl_vals = cl_cols[-1].split('/')
                        layer_count = 0
                        for cl_val in cl_vals:
                            if cl_val != "99999":
                                if "cloud" not in aws_data:
                                    aws_data["cloud"] = []

                                aws_data["cloud"].append(float(cl_val))
                        good_tag_count += 1
                        break
                    elif tag == "VI":
                        vi_cols = aad_col.split(":")
                        if "visibility" not in aws_data:
                            aws_data["visibility"] = {}
                        aws_data["visibility"] = float(vi_cols[-1])
                        good_tag_count += 1
                        break
                    elif tag == "WX1ME":
                        wx_cols = aad_col.split(":")
                        wx0 = wx_cols[-1][1:3]
                        if int(wx0) > 0:
                            aws_data["wx"] = []
                            aws_data["wx"].append(metar_lookup_dict[wx0])


                        good_tag_count += 1
                        break
                    elif tag == "WS":
                        ws_cols = aad_col.split(":")
                        aws_data["wind_speed"] = {}
                        aws_data["wind_speed"]["average"] = float(ws_cols[-1][:3])
                        aws_data["wind_speed"]["min"] = float(ws_cols[-1][4:7])
                        aws_data["wind_speed"]["max"] = float(ws_cols[-1][8:11])
                        good_tag_count += 1
                        break
                    elif tag == "WD":
                        wd_cols = aad_col.split(":")
                        aws_data["wind_direction"] = {}
                        aws_data["wind_direction"]["average"] = float(wd_cols[-1][:3])
                        aws_data["wind_direction"]["minus_std_dev"] = float(wd_cols[-1][4:7])
                        aws_data["wind_direction"]["plus_std_dev"] = float(wd_cols[-1][8:11])
                        good_tag_count += 1
                        break
                    elif tag == "AT:":
                        at_cols = aad_col.split(":")
                        aws_data['air_temperature'] = {}
                        aws_data['air_temperature']['average'] = float(at_cols[-1][:4])
                        aws_data['air_temperature']['min'] = float(at_cols[-1][5:9])
                        aws_data['air_temperature']['max'] = float(at_cols[-1][10:14])
                        good_tag_count += 1
                        break
                    elif tag == "DP":
                        dp_cols = aad_col.split(":")
                        aws_data['dew_point'] = {}
                        aws_data['dew_point']['average'] = float(dp_cols[-1][:4])
                        aws_data['dew_point']['min'] = float(dp_cols[-1][5:9])
                        aws_data['dew_point']['max'] = float(dp_cols[-1][10:14])
                        good_tag_count += 1
                        break
                    elif tag == "RH":
                        rh_cols = aad_col.split(":")
                        aws_data["rel_humidity"] = {}
                        aws_data["rel_humidity"]["average"] = float(rh_cols[-1][:3])
                        aws_data["rel_humidity"]["min"] = float(rh_cols[-1][4:7])
                        aws_data["rel_humidity"]["max"] = float(rh_cols[-1][8:11])
                        good_tag_count += 1
                        break
                    elif tag == "RF":
                        rf_cols = aad_col.split(":")
                        aws_data['rainfall'] = float(rf_cols[-1])
                        good_tag_count += 1
                        break
                    elif tag == "QFE":
                        qfe_cols = aad_col.split(":")
                        if "pressure" not in aws_data:
                            aws_data["pressure"] = {}

                        aws_data['pressure']['qfe'] = float(qfe_cols[-1])
                        good_tag_count += 1
                        break
                    elif tag == "QNH":
                        qnh_cols = aad_col.split(":")
                        if "pressure" not in aws_data:
                            aws_data["pressure"] = {}

                        aws_data['pressure']['qnh'] = float(qnh_cols[-1])
                        good_tag_count += 1
                        break
                    elif tag == "QFF":
                        qff_cols = aad_col.split(":")
                        if "pressure" not in aws_data:
                            aws_data["pressure"] = {}

                        aws_data['pressure']['qff'] = float(qff_cols[-1])
                        good_tag_count += 1
                        break
                    elif tag == "TI:":
                        ti_cols = aad_col.split(":")
                        if "engineering" not in aws_data:
                            aws_data["engineering"] = {}

                        aws_data['engineering']['internal_temp'] = float(ti_cols[-1])
                        good_tag_count += 1
                        break
                    elif tag == "BV":
                        bv_cols = aad_col.split(":")

                        if "engineering" not in aws_data:
                            aws_data["engineering"] = {}

                        aws_data['engineering']['battery_voltage'] = float(bv_cols[-1])
                        good_tag_count += 1
                        break

        if good_tag_count > 14:
            return_list.append(aws_data)
            aws_data = {"station_wsi": "0-20000-0-94975"}
            at_least_one_good = True
            good_tag_count = 0

            done_count += 1
            if done_count >= obs_count:
                need_more = False
                end_pos = data_pos

        data_pos += 1

    return return_list