#python program to segment accelerometer heartbeat values to obtain a full heartbeat cycle
# step 1 - read in the data and divide into 2 second chunks
# step 2 - identity the AO and RF peaks using the shortest distance between 2 peaks that's greater than 200ms, starting from the highest peak.
# This performs well in trying to find the AO and RF as AO to RF intervals are larger than 200ms
# Now that we have obtained the AO to RF distance, we multiply 0.5 to it to obtain the ATC to AO distance, from that we can obtain a full heartbeat cycle.

#import heartbeatvals.csv
import csv
import matplotlib.pyplot as plt

#read in the data
with open('../heartbeat_values/heartvals_2secs.csv', 'r') as f:
    reader = csv.reader(f)
    heartbeat = list(reader)
    #print(heartbeat)

#convert the all the heartbeat data in each list to floats/100.0
for i in range(len(heartbeat)):
    heartbeat[i] = [float(x)/100.0 for x in heartbeat[i]]

print (heartbeat)

#plot the heartbeat data
def plot_heartbeats(heartbeat):
    #take each heartbeat list and plot it
    for i in range(len(heartbeat)):
        x_axis = [(x/256.0) for x in range(len(heartbeat[0]))]
        y_axis = heartbeat
        plt.title("Heartbeat z-values for 2 seconds")
        plt.xlabel("Time (seconds)")
        plt.ylabel("Acceleration (g)")
        plt.plot(x_axis, y_axis[i])
        plt.show()


plot_heartbeats(heartbeat)
