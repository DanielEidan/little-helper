# time_util
from time import sleep as original_sleep
from random import gauss

sleep_percentage = 1
STDEV = 0.5

def sleep(t, custom_percentage=None):
    if custom_percentage is None:
        custom_percentage = sleep_percentage
    time = randomize_time(t)*custom_percentage
    original_sleep(time)

def randomize_time(mean):
    allowed_range = mean * STDEV
    stdev = allowed_range / 3  # 99.73% chance to be in the allowed range
    t = 0
    while abs(mean - t) > allowed_range:
        t = gauss(mean, stdev)
    return t