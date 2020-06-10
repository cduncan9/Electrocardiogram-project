import logging
import math
import matplotlib.pyplot as plt
import heartpy as hp
import numpy as np
import json


logging.basicConfig(filename='bad_data.log',
                    level=logging.INFO)


def output_file(metrics, filename):
    filename_split = filename.split(".")
    file = filename_split[0]
    filename = file + ".json"
    with open(filename, 'x') as out_file:
        json.dump(metrics, out_file)


def calc_beats(time, volts):
    beat_list = list()
    extremes = calc_voltage_extremes(volts)
    maximum = extremes[1]
    for i in range(len(volts)):
        if volts[i] > (maximum / 2):
            beat_list.append(time[i])
    return beat_list


def calc_mean_hr_bpm(time, volts):
    beat_list = calc_beats(time, volts)
    hr_list = list()
    for i in range(len(beat_list)):
        if i > 0:
            diff = beat_list[i] - beat_list[i-1]
            hr_list.append(diff)
    ave_hr = [(1/x)*60 for x in hr_list]
    ave = np.mean(ave_hr)
    return ave


def calc_num_beats(volt):
    num_beats = 0
    extremes = calc_voltage_extremes(volt)
    maximum = extremes[1]
    for v in volt:
        if v > (maximum / 2):
            num_beats += 1
    return num_beats


def calc_voltage_extremes(volt):
    maximum = max(volt)
    minimum = min(volt)
    ans = (minimum, maximum)
    return ans


def calc_duration(time):
    first = time[0]
    last = time[-1]
    return last - first


def filter_data(time, raw_volt):
    sample_rate = 1 / (time[1] - time[0])
    volt = hp.filter_signal(raw_volt, [5, 20], sample_rate, 2, 'bandpass')
    return volt


def make_dictionary(duration, voltage_extremes, num_beats, mean_hr_bpm, beats):
    metrics = {"duration": duration, "voltage_extremes": voltage_extremes,
               "num_beats": num_beats, "mean_hr_bpm": mean_hr_bpm,
               "beats": beats}
    return metrics


def calc_metrics(time, raw_volt):
    volt = filter_data(time, raw_volt)
    duration = calc_duration(time)
    voltage_extremes = calc_voltage_extremes(volt)
    num_beats = calc_num_beats(volt)
    mean_hr_bpm = calc_mean_hr_bpm(time, volt)
    beats = calc_beats(time, volt)
    metrics = make_dictionary(duration, voltage_extremes, num_beats,
                              mean_hr_bpm, beats)
    return metrics


def split_data(temp_line):
    temp_line = temp_line.strip("\n")
    temp_list = temp_line.split(",")
    time = temp_list[0]
    time = time.strip(" ")
    if len(temp_list) == 2:
        volt = temp_list[1]
        volt = volt.strip(" ")
    else:
        volt = ''
    return time, volt


def is_a_number(number):
    try:
        float(number)
    except ValueError:
        return False
    return True


def check_data(temp_time, temp_volt):
    if temp_volt == '':
        return False
    elif temp_time == '':
        return False
    elif is_a_number(temp_time) is False:
        return False
    elif is_a_number(temp_volt) is False:
        return False
    elif math.isnan(float(temp_time)) is True:
        return False
    elif math.isnan(float(temp_volt)) is True:
        return False
    else:
        return True


def read_input(filename):
    time = list()
    volt = list()
    check_max_val = 0
    with open(filename, 'r') as f:
        temp_line = f.readline()
        while temp_line != "":
            temp_time, temp_volt = split_data(temp_line)
            temp_check = check_data(temp_time, temp_volt)
            if temp_check is True:
                temp_time = float(temp_time)
                time.append(temp_time)
                temp_volt = float(temp_volt)
                if temp_volt > 300 or temp_volt < -300:
                    check_max_val = 1
                volt.append(temp_volt)
            else:
                logging.error('Bad data point,'
                              'skipping to next line')
            temp_line = f.readline()
        if check_max_val == 1:
            logging.warning("This file contains a value outside the "
                            "normal operating range of +/- 300 mV.")
    return time, volt


def interface():
    filename = input("Please enter the filename: ")
    ecg_time, ecg_volt = read_input(filename)
    metrics = calc_metrics(ecg_time, ecg_volt)
    output_file(metrics, filename)


if __name__ == '__main__':
    interface()
