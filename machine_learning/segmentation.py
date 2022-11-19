#python program to segment accelerometer heartbeat values to obtain a full heartbeat cycle
# step 1 - read in the data and divide into 2 second chunks
# step 2 - identity the AO and RF peaks using the shortest distance between 2 peaks that's greater than 200ms, starting from the highest peak.
# This performs well in trying to find the AO and RF as AO to RF intervals are larger than 200ms
# Now that we have obtained the AO to RF distance, we multiply 0.5 to it to obtain the ATC to AO distance, from that we can obtain a full heartbeat cycle.

#import heartbeatvals.csv
import csv
import matplotlib.pyplot as plt
import numpy as np
# from scipy.signal import argrelextrema
# from sklearn import preprocessing

frequency = 160.0

#read in the data
def open_file(filename):
    print(filename)
    heartbeat_2secs = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        heartbeat_secs = list(reader)
        # remove incorrect data (from pressing the left button)
        heartbeat_2secs = [x[10:] for x in heartbeat_secs]
    return heartbeat_2secs

# heartbeat_2secs = open_file('../heartbeat_values/160hz/readings-mustafa-160hz.csv')

def convert_to_floats(heartbeat_2secs):
    #convert the all the heartbeat_2secs data in each list to floats/100.0
    for i in range(len(heartbeat_2secs)):
        heartbeat_2secs[i] = [float(x)/100.0 for x in heartbeat_2secs[i]]
        #print(heartbeat_2secs[i])
        #print("----------------\n\n")
    return heartbeat_2secs

# convert_to_floats(heartbeat_2secs)

#plot the heartbeat data
def plot_heartbeats_all(heartbeat_2secs):
    #take each heartbeat_2secs list and plot it
    for i in range(len(heartbeat_2secs)):
        x_axis = [(x/len(heartbeat_2secs[0])) for x in range(len(heartbeat_2secs[0]))]
        y_axis = heartbeat_2secs
        plt.title("Heartbeat z-values for 2 seconds")
        plt.xlabel("Time (seconds)")
        plt.ylabel("Acceleration (m/s^2)")
        plt.plot(x_axis, y_axis[i])
        plt.show()


# plot_heartbeats_all(heartbeat_2secs)

#plot the 2-second tuple heartbeat data
def plot_heartbeats(heartbeat_tuple_2secs):
    x = [x[0] for x in heartbeat_tuple_2secs]
    y = [x[1] for x in heartbeat_tuple_2secs]
    plt.plot(x, y)
    plt.title("Heartbeat z-values for 2 seconds")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Acceleration (m/s^2)")
    plt.show()
    

# create a pair of x axis and y axis for each heartbeat_2secs value
def create_heartbeat_tuples(heartbeat_2secs):
    heartbeat_tuples = []
    for i in range(len(heartbeat_2secs)):
        x_vals = [(x/frequency) for x in range(len(heartbeat_2secs[i]))]
        y_vals = heartbeat_2secs[i]
        heartbeat_tuples.append(list(zip(x_vals, y_vals)))

    return heartbeat_tuples

# heartbeat_tuples = create_heartbeat_tuples(heartbeat_2secs)

# mark AO and RF on the plotted graph
# mark start and end of heartbeat cycle
def plot_segmented_heartbeats(heartbeat_tuples, ao_tuple, rf_tuple, closest_peak_distance):
    x = [x[0] for x in heartbeat_tuples]
    y = [x[1] for x in heartbeat_tuples]
    plt.plot(x, y)
    plt.title("Heartbeat z-values for 2 seconds -- segmented")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Acceleration (m/s^2)")
    plt.scatter(ao_tuple[0], ao_tuple[1], color='red')
    plt.scatter(rf_tuple[0], rf_tuple[1], color='green')
    plt.axvline(x=ao_tuple[0] - 0.5*closest_peak_distance, color='yellow')
    start_line = ao_tuple[0] - 0.5*closest_peak_distance
    plt.axvline(x= start_line + 1.5*closest_peak_distance, color='yellow')
    plt.axhline(y=np.mean(y), color='black')
    plt.show()
           

# segment_heartbeats(heartbeat_tuples)   
# print("\n\n-----------------------------------\n\n")
# identify the AO and RF peaks using the shortest distance between 2 peaks that's greater than 200ms, starting from the highest peak.
def segment_heartbeats(heartbeat_tuples):

    all_heartvalues = []
    # identify the highest peak (y value) in each heartbeat_tuple_2secs
    for heartbeat_tuple_2secs in heartbeat_tuples:

        
        #plot_heartbeats(heartbeat_tuple_2secs)
        ao_peak = max(heartbeat_tuple_2secs, key=lambda x: x[1])

        print("AO peak: ", ao_peak)

        # find the average of all values in heartbeat_tuple_2secs
        average = np.mean([x[1] for x in heartbeat_tuple_2secs])




        # find closest peak to the AO peak that's greater than 200ms
        ao_rf_distance = 0.5
        rf_peak = 0
        for i in range(len(heartbeat_tuple_2secs)):
            if (heartbeat_tuple_2secs[i][0] - ao_peak[0] > 0.2 and heartbeat_tuple_2secs[i][0] - ao_peak[0] < ao_rf_distance and heartbeat_tuple_2secs[i][1] > average):
                ao_rf_distance = heartbeat_tuple_2secs[i][0] - ao_peak[0]
                rf_peak = heartbeat_tuple_2secs[i]

        
        print("RF peak: ", rf_peak)
        print("AO-RF distance: ", ao_rf_distance)
        print("\n\n\n")

        #plot_segmented_heartbeats(heartbeat_tuple_2secs, ao_peak, rf_peak, ao_rf_distance)

        # return array of heartbeat_tuple_2secs values in the range: 0.5*closest_peak_distance - 1.5*closest_peak_distance
        start_of_hearbeat_cycle = ao_peak[0] - 0.5*ao_rf_distance
        end_of_heartbeat_cycle = start_of_hearbeat_cycle + 1.5*ao_rf_distance
        
        heartvalues = []
        for i in range(len(heartbeat_tuple_2secs)):
            if (heartbeat_tuple_2secs[i][0] >= start_of_hearbeat_cycle and heartbeat_tuple_2secs[i][0] <= end_of_heartbeat_cycle):
                heartvalues.append(heartbeat_tuple_2secs[i])

        all_heartvalues.append(heartvalues)
    return all_heartvalues


# segmented_heartbeats = segment_heartbeats(heartbeat_tuples)

# for segmented_heartbeat in segmented_heartbeats:
#     print(segmented_heartbeat)
#     print("\n\n")

