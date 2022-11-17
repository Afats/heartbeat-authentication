#python program to segment accelerometer heartbeat values to obtain a full heartbeat cycle
# step 1 - read in the data and divide into 2 second chunks
# step 2 - identify the AO and RF peaks using the shortest distance between 2 peaks that's greater than 200ms, starting from the highest peak.
# This performs well in trying to find the AO and RF as AO to RF intervals are larger than 200ms
# Now that we have obtained the AO to RF distance, we multiply 0.5 to it to obtain the ATC to AO distance, from that we can obtain a full heartbeat cycle.

#import heartbeatvals.csv
import csv
import matplotlib.pyplot as plt
from sklearn import preprocessing
import numpy as np
from scipy.signal import argrelextrema

#read in the data
with open('../heartbeat_values/heartvals_2secs.csv', 'r') as f:
    reader = csv.reader(f)
    heartbeat_2secs = list(reader)
    #print(heartbeat_2secs)

#convert all the heartbeat_2secs data in each list to floats/100.0
for i in range(len(heartbeat_2secs)):
    heartbeat_2secs[i] = [float(x)/100.0 for x in heartbeat_2secs[i]]

# print (heartbeat_2secs)

#plot the heartbeat data
def plot_heartbeats(heartbeat_2secs):
    #take each heartbeat_2secs list and plot it
    for i in range(len(heartbeat_2secs)):
        x_axis = [(x/256.0) for x in range(len(heartbeat_2secs[0]))]
        y_axis = heartbeat_2secs
        plt.title("Heartbeat z-values for 2 seconds")
        plt.xlabel("Time (seconds)")
        plt.ylabel("Acceleration (g)")
        plt.plot(x_axis, y_axis[i])
        plt.show()


# plot_heartbeats(heartbeat_2secs)


# create a pair of x axis and y axis for each heartbeat_2secs value
def create_heartbeat_tuples(heartbeat_2secs):
    heartbeat_tuples = []
    for i in range(len(heartbeat_2secs)):
        x_vals = [(x/256.0) for x in range(len(heartbeat_2secs[i]))]
        y_vals = heartbeat_2secs[i]
        heartbeat_tuples.append(list(zip(x_vals, y_vals)))
        # print(heartbeat_tuples)

    return heartbeat_tuples

heartbeat_tuples = create_heartbeat_tuples(heartbeat_2secs)
# print(heartbeat_tuples)


# mark the highest peak and the closest peak on the plotted graph
def plot_segmented_heartbeats(heartbeat_tuples, ao_tuple, rf_tuple):
    x = [x[0] for x in heartbeat_tuples]
    y = [x[1] for x in heartbeat_tuples]
    plt.plot(x, y)
    plt.title("Heartbeat z-values for 2 seconds -- segmented")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Acceleration (g)")
    plt.scatter(ao_tuple[0], ao_tuple[1], color='red')
    plt.scatter(rf_tuple[0], rf_tuple[1], color='green')
    plt.show()



#step 2 - identify the AO and RF peaks using the shortest distance between 2 peaks that's greater than 200ms, starting from the highest peak.
def segment_heartbeats(heartbeat_tuples):   
        # find the local maximum y values of heartbeat_tuples  ***(within a x range of 0.5 seconds ???)***
        for heartbeat_tuple_2secs in heartbeat_tuples:
            # using scipy to find the local maxima
            local_maxima = argrelextrema(np.array(heartbeat_tuple_2secs)[:,1], np.greater)
            local_maxima_values = np.array(heartbeat_tuple_2secs)[local_maxima]
            local_maxima_values = [tuple(x) for x in local_maxima_values]
            # print(local_maxima_values)


            # *** review candiate set adding process, and peak removing process ***

            # We then perform a pruning algorithm to remove noisy peaks. 
            # Starting from the highest peaks, we add the peaks into a candidate set one-by-one in the descending order of their amplitudes. 
            # If the current peak is within a time interval of 200ms to one of the candidate peaks in the set, the current peak is removed. 

            # Sort the local maxima y values by their descending amplitudes
            candidate_set = sorted(local_maxima_values, key=lambda x: x[1], reverse=True) 
            # print(candidate_set)


            # *** iterate thru local maxima values and remove the ones in local_maxima that are within 200ms of a peak in the candidate_set instead ???****

            # if the distance is less than 200ms to the current candidate, remove the peak from candidate_set
            for i in range(len(candidate_set)):
                for j in range(i+1, len(candidate_set)):
                    if ((candidate_set[i][0] - candidate_set[j][0]) < 0.2 or (candidate_set[j][0] - candidate_set[i][0]) < 0.2):
                        candidate_set.remove(candidate_set[j])
                        break
            
            #  print(candidate_set)

            # Since there could be multiple heartbeat cycles in the two-second SCG sequence, there are multiple candidates of AO and RF peaks. 
            # Choose the two peaks that are the closest to each other since the AO-RF interval is usually smaller than the RF-AO interval.


            # find the shortest distance between 2 peaks that's greater than 200ms, starting from the highest peak.
            shortest_distance = 0.5
            for i in range(len(candidate_set)):
                for j in range(i+1, len(candidate_set)):
                    if ((candidate_set[i][0] - candidate_set[j][0]) < shortest_distance and (candidate_set[i][0] - candidate_set[j][0]) > 0.2):
                        shortest_distance = candidate_set[i][0] - candidate_set[j][0]
                        ao_candidates = candidate_set[i]
                        rf_candidates = candidate_set[j]

            print("AO candidates", ao_candidates)
            print("RF candidates", rf_candidates)
            print("Shortest distance: ", shortest_distance)

            # sort the candidate_set by ascending time values
            # candidate_set = sorted(candidate_set, key=lambda x: x[0])
            # print(candidate_set)

            
            # find the 2 peaks that have a distance closest to the shortest distance, 
            # and the amplitude of the ao peak is greater than the rf peak, 
            # and the x value of the ao peak is less than the rf peak
            for i in range(len(candidate_set)):
                for j in range(i+1, len(candidate_set)):
                    if (((candidate_set[i][0] - candidate_set[j][0]) >= shortest_distance and candidate_set[i][1] > candidate_set[j][1] and candidate_set[i][0] < candidate_set[j][0]) or ((candidate_set[j][0] - candidate_set[i][0]) >= shortest_distance and candidate_set[j][1] > candidate_set[i][1] and candidate_set[j][0] < candidate_set[i][0])):
                        ao_peak = candidate_set[i]
                        rf_peak = candidate_set[j]
                        print("AO peak: ", ao_peak)
                        print("RF peak: ", rf_peak)
           

segment_heartbeats(heartbeat_tuples)   
print("\n\n-----------------------------------\n\n")
# identify the AO and RF peaks using the shortest distance between 2 peaks that's greater than 200ms, starting from the highest peak.
def segment_heartbeats2(heartbeat_tuples):

    all_heartvalues = []
    # identify the highest peak (y value) in each heartbeat_tuple_2secs
    for heartbeat_tuple_2secs in heartbeat_tuples:
        highest_peak = max(heartbeat_tuple_2secs, key=lambda x: x[1])

        print("Highest peak: ", highest_peak)


        # find closest peak to the highest peak that's greater than 200ms
        closest_peak_distance = 0.5
        closest_peak = 0
        for heartbeat_tuple_2secs in heartbeat_tuples:
            for i in range(len(heartbeat_tuple_2secs)):
                if (heartbeat_tuple_2secs[i][0] - highest_peak[0] > 0.2 and heartbeat_tuple_2secs[i][0] - highest_peak[0] < closest_peak_distance):
                    closest_peak_distance = heartbeat_tuple_2secs[i][0] - highest_peak[0]
                    closest_peak = heartbeat_tuple_2secs[i]
        
        print("Closest peak: ", closest_peak)
        print("Closest peak distance: ", closest_peak_distance)
        print("\n\n\n")

        # plot_segmented_heartbeats(heartbeat_tuple_2secs, highest_peak, closest_peak)

        # return array of heartbeat_tuple_2secs values in the range: 0.5*closest_peak_distance - 1.5*closest_peak_distance

        heartvalues = []
        for i in range(len(heartbeat_tuple_2secs)):
            if (heartbeat_tuple_2secs[i][0] > 0.5*closest_peak_distance and heartbeat_tuple_2secs[i][0] < 1.5*closest_peak_distance):
                heartvalues.append(heartbeat_tuple_2secs[i])
        all_heartvalues.append(heartvalues)
        # print(all_heartvalues)
    return all_heartvalues


segmented_heartbeats = segment_heartbeats2(heartbeat_tuples)

for segmented_heartbeat in segmented_heartbeats:
    print(segmented_heartbeat)
    print("\n\n")


print("\n\n-----------------------------------\n\n")
# NORMALIZATION before moving on to the extraction

# finding the highest peak (y val) in each cycle
# dividing each y val by the highest peak to normalize the data
def normalize_heartbeats(segmented_heartbeats):
    normalized_heartbeats = []
    cycle_highest_peak = 0
    # for i in range(len(segmented_heartbeat)):
    for segmented_heartbeat in segmented_heartbeats:
        # normalized_heartbeat = preprocessing.normalize(segmented_heartbeat)
        cycle_highest_peak = max(segmented_heartbeat, key=lambda x: x[1])
        print("\nmax amplitude of the beat: ",cycle_highest_peak)
        print("\n/////////--------.......-------///////\n")
        # print(segmented_heartbeat)

        normalized_heartbeat = []
        for beat in segmented_heartbeat:
            normalized_altitude = beat[1] / cycle_highest_peak[1]
            temp_beat = (beat[0], normalized_altitude)
            beat = temp_beat
            normalized_heartbeat.append(beat)

        normalized_heartbeats.append(normalized_heartbeat)

    return normalized_heartbeats

normalized_heartbeats = normalize_heartbeats(segmented_heartbeats)

for norm_beats in normalized_heartbeats:
    print(norm_beats)
    print("\n\n")
    
