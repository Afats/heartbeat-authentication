import csv
import matplotlib.pyplot as plt
import numpy as np
from machine_learning.segmentation import *
# from machine_learning.segmentation import segment_heartbeats
from machine_learning.feature_extraction import *
from machine_learning.training import authenticate_user,train
from sklearn.svm import SVC

def open_this_file(filename):
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
userAuthenticated = 0
print("starting the heartbeat authentication...")
while (user_input != 5):
    print("1 - Generate training data for attackers\n2 - Train Data\n3 - Get new user data\n4 - Predict\n5 - Quit\nEnter operation:",end = "")
    user_input = int(input())

    if (user_input == 1):
        # step1: generate training data... data collection using the sensor
        # using the csv's in segmentation, feature extraction and ML prediction
        heartbeat_2secs = open_this_file('heartbeat_values/160hz/allreadings.csv')
        # could fail -> check the method arg and return val in segmentation.py
        heartbeat_2secs_ = convert_to_floats(heartbeat_2secs)

        heartbeat_tuples = create_heartbeat_tuples(heartbeat_2secs)

        segmented_heartbeats = segment_heartbeats(heartbeat_tuples)

        for segmented_heartbeat in segmented_heartbeats:
            print(segmented_heartbeat)
            print("\n\n")
    elif (user_input == 2):
        # using the csv's in segmentation, feature extraction and ML prediction
        heartbeat_2secs = open_this_file('Temp3.csv')
        # could fail -> check the method arg and return val in segmentation.py
        heartbeat_2secs_ = convert_to_floats(heartbeat_2secs)

        heartbeat_tuples = create_heartbeat_tuples(heartbeat_2secs)

        segmented_heartbeats = segment_heartbeats(heartbeat_tuples)

        for segmented_heartbeat in segmented_heartbeats:
            print(segmented_heartbeat)
            print("\n\n")

        extracted_feature_cycles = dwt_decompose(segmented_heartbeats)
        features_vector = create_features_vector(extracted_feature_cycles)

    elif (user_input == 4):
        clf = SVC(kernel='linear')
        clf = train(clf, "machine_learning/temp2.csv")
        ans = authenticate_user(clf, "machine_learning/tempMustafa.csv")

        # print(ans[0])
        if (userAuthenticated == 1):
            print("AUTHENTICATED\n")
        else:
            print("ACCESS DENIED\n")


    elif (user_input == 3):
        #COPY 1
        userAuthenticated = userAuthenticated + 1
        # step1: generate training data... data collection using the sensor
        # using the csv's in segmentation, feature extraction and ML prediction
        if (userAuthenticated == 1):
            heartbeat_2secs = open_this_file('heartbeat_values/160hz/readings-pankrit-160hz.csv')
        else:
            heartbeat_2secs = open_this_file('heartbeat_values/160hz/readings-mustafa-160hz.csv')
        # could fail -> check the method arg and return val in segmentation.py
        heartbeat_2secs_ = convert_to_floats(heartbeat_2secs)

        heartbeat_tuples = create_heartbeat_tuples(heartbeat_2secs)

        segmented_heartbeats = segment_heartbeats(heartbeat_tuples)

        for segmented_heartbeat in segmented_heartbeats:
            print(segmented_heartbeat)
            print("\n\n")
