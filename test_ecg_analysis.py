import pytest
import numpy as np
from testfixtures import LogCapture


@pytest.mark.parametrize("string, exp", [
    ('1, 2', ('1', '2')),
    ('1, ', ('1', '')),
    ('2', ('2', '')),
    ('  , 3', ('', '3'))])
def test_split_data(string, exp):
    from ecg_analysis import split_data
    answer = split_data(string)
    assert answer == exp


@pytest.mark.parametrize("time, volt, expected", [
    ('1', '1', True),
    ('1', '', False),
    ('1', 'Hello', False),
    ('', '1', False),
    ('0.5', '-1.7', True)])
def test_check_data(time, volt, expected):
    from ecg_analysis import check_data
    answer = check_data(time, volt)
    assert answer == expected


@pytest.mark.parametrize("test_num, exp", [
    ("1", True),
    ("0.5", True),
    ("-0.56677", True),
    ("Happy", False),
    ("#*$(", False)])
def test_is_a_number(test_num, exp):
    from ecg_analysis import is_a_number
    answer = is_a_number(test_num)
    assert answer == exp


# def test_filter_data():
#     from ecg_analysis import filter_data
#     time = np.linspace(0, 0.05, 20)
#     sample_data = np.ones(20)
#     noise = [math.sin(2*math.pi*100*time[i]) for i in range(len(time))]
#     volt_w_noise = [sample_data[i] * noise[i] for i in range(len(time))]
#     answer = filter_data(time, volt_w_noise)
#     assert answer[3] == sample_data[3]

def test_calc_duration():
    from ecg_analysis import calc_duration
    time = np.linspace(0, 1, 200)
    expected = 1
    answer = calc_duration(time)
    assert answer == expected


def test_calc_voltage_extremes():
    from ecg_analysis import calc_voltage_extremes
    data = [0, 1, 1, -4, 18, -7, 2, 0]
    expected = (-7, 18)
    answer = calc_voltage_extremes(data)
    assert answer == expected


def test_calc_num_beats():
    from ecg_analysis import calc_num_beats
    time = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    data = [3, 4, 3, 10, 4, 3, 4, 10, 3, 4]
    expected = 2
    answer = calc_num_beats(time, data)
    assert answer == expected


def test_calc_mean_hr_bpm():
    from ecg_analysis import calc_mean_hr_bpm
    time = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
            15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
            27, 28, 29, 30]
    volts = [0, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0, 5,
             0, 0, 0, 5, 0, 0, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0]
    expected = 14.5
    answer = calc_mean_hr_bpm(time, volts)
    assert answer == expected


def test_calc_beats():
    from ecg_analysis import calc_beats
    time = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
            15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
            27, 28, 29, 30, 31]
    volts = [0, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0, 5,
             0, 0, 0, 5, 0, 0, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0, 0]
    expected = [3, 7, 11, 15, 19, 24, 28]
    answer = calc_beats(time, volts)
    assert answer == expected


# def test_calc_metrics():
#     from ecg_analysis import calc_metrics
#     time = [0, .01, .02, .03, .04, .05, .06, .07, .08, .09,
#             .10, .11, .12, .13, .14, .15, .16, .17, .18, .19,
#             .20, .21, .22, .23, .24, .25, .26, .27, .28, .29,
#             .30, .31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37,
#             0.38, 0.39, 0.4, 0.41, 0.42, 0.43, 0.44, 0.45,
#             0.46, 0.47, 0.48, 0.49, 0.5]
#     volts = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0,
#              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0,
#              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
#              0, 0, 0]
#     answer = calc_metrics(time, volts)
#     expected = {"beats": [0.07, 0.28, 0.42], "duration": .5,
#                 "mean_hr_bpm": 357.1428571428572, "num_beats": 3,
#                 "voltage_extremes": (0, 1)}
#     assert answer == expected


def test_log_if_bad_data_is_made():
    from ecg_analysis import log_if_bad_data
    with LogCapture() as log_c:
        log_if_bad_data(False)
    log_c.check(('root', 'ERROR', 'Bad data point, '
                'skipping to next line'))


def test_log_if_bad_data_is_not_made():
    from ecg_analysis import log_if_bad_data
    with LogCapture() as log_c:
        log_if_bad_data(True)
    log_c.check()


def test_log_if_data_too_high_is_made():
    from ecg_analysis import log_if_data_too_high
    with LogCapture() as log_c:
        log_if_data_too_high([24, 25, 26, 27, 28, 29, 30, 310])
    log_c.check(('root', 'WARNING', "This file contains a value "
                 "outside the normal operating range of +/- 300 mV."))


def test_log_if_data_too_high_is_not_made():
    from ecg_analysis import log_if_data_too_high
    with LogCapture() as log_c:
        log_if_data_too_high([24, 25, 26, 27, 28, 29, 30])
    log_c.check()
