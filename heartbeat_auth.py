import csv
import matplotlib.pyplot as plt
import numpy as np
from machine_learning.segmentation import *
from machine_learning.feature_extraction import *
from machine_learning.training import *

def open_file(filename):
    #read in the data
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        heartbeat_secs = list(reader)
        # remove incorrect data (from pressing the left button)
        heartbeat_2secs = [x[10:] for x in heartbeat_secs]
    return heartbeat_2secs

# ------------------------------
# main
user_input = 0
while (user_input != 4):
    print(input("1 - Generate training data\n2 - Train\n3 - Predict\n4 - Quit\nEnter operation:"))


if (user_input == 1):
    # step1: generate training data... data collection using the sensor
    # call to receiver3.py to get data into a csv
    pass
elif (user_input == 2):
    # using the csv's in segmentation, feature extraction and ML prediction
    heartbeat_2secs = open_file('../heartbeat_values/160hz/readings-mustafa-160hz.csv')
    # could fail -> check the method arg and return val in segmentation.py
    heartbeat_2secs = convert_to_floats(heartbeat_2secs)

    heartbeat_tuples = create_heartbeat_tuples(heartbeat_2secs)

    segment_heartbeats = segment_heartbeats(heartbeat_tuples)

    for segmented_heartbeat in segmented_heartbeats:
        print(segmented_heartbeat)
        print("\n\n")

elif (user_input == 3):
    pass
elif (user_input == 4):
    pass

