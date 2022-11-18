# multi-level feature extraction of the segmented heartbeat cycles using Discrete Wavelet Transform (DWT)


# The DWT decomposes SCG signals into five levels with level 1 to 5 represent signal components 
# in the frequency range of 25 ∼ 50 Hz, 12.5 ∼ 25 Hz, 6.25 ∼ 12.5 Hz, 3.13 ∼ 6.25 Hz and 1.56 ∼ 3.13 Hz, respectively. 
# To reduce noise in the SCG signal, we only use the detailed coefficients from the second level to the fourth level 
# as the feature vector for heartbeat authentication.

# use the discrete Meyer wavelet

import pywt
from segmentation import segmented_heartbeats
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate

# NORMALIZATION before moving on to the extraction

def normalize_heartbeats(segmented_heartbeats):
    normalized_heartbeats = []

    max_len = 0
    for beat_cycle in normalized_heartbeats:
        if (len(beat_cycle) > max_len):
            max_len = len(beat_cycle)
    
    for segmented_heartbeat in segmented_heartbeats:

        # finding the highest peak (y val) in each cycle
        # dividing each y val by the highest peak to normalize the data
        cycle_highest_peak = max(segmented_heartbeat, key=lambda x: x[1])
        print("\nmax amplitude of the beat: ",cycle_highest_peak)
        print("\n/////////--------.......-------///////\n")

        normalized_heartbeat = []
        for beat in segmented_heartbeat:
            normalized_altitude = beat[1] / cycle_highest_peak[1]

            beat = (beat[0], normalized_altitude)

            # appending zeros to the end of each heartbeat cycle to guarantee consistent durations
            if (len(beat) < max_len):
                beat = beat + [(beat[-1][0] + 0.001, 0) for i in range(max_len - len(beat))]

            normalized_heartbeat.append(beat)
        normalized_heartbeats.append(normalized_heartbeat)
    return normalized_heartbeats

normalized_heartbeats = normalize_heartbeats(segmented_heartbeats)

for norm_beats in normalized_heartbeats:
    print("normalized heartbeats by pankrit ")
    print(norm_beats)
    print("\n\n")

def plot_heartbeat_cycle(heartbeat_cycle, title):
    x = [x[0] for x in heartbeat_cycle]
    y = [x[1] for x in heartbeat_cycle]
    plt.plot(x, y)
    plt.title(title)
    plt.xlabel("Time (seconds)")
    plt.ylabel("Acceleration (m/s^2)")
    plt.show()


def plot_heartbeat_cycle_dwt(heartbeat_cycle, title):
    x = [(x/len(heartbeat_cycle)) for x in range(len(heartbeat_cycle))]
    y = [x for x in heartbeat_cycle]

    # append x with mean values for length of y-x
    if (len(x) < len(y)):
        x = x + [np.mean(x) for i in range(len(y) - len(x))]

    plt.plot(x, y)
    plt.title(title)
    plt.xlabel("Time (seconds)")
    plt.ylabel("Acceleration (m/s^2)")
    plt.show()


def interpolate_heartbeats(segmented_heartbeats):

    for segmented_heartbeat in segmented_heartbeats:
        # get all scg values from the heartbeat cycle
        scgs = [x[1] for x in segmented_heartbeat]
        # get all time values from the heartbeat cycle
        times = [x[0] for x in segmented_heartbeat]

        # linearly interpolate the scg values to 200 values
        # f = scipy.interpolate.interp1d(times, scgs, kind='linear')
        f = scipy.interpolate.interp1d(times, scgs, kind='cubic')
        times_new = np.linspace(times[0], times[-1], 200)
        scgs_new = f(times_new)

        # replace the old scg values with the new interpolated scgs
        for i in range(len(segmented_heartbeat)):
            segmented_heartbeat[i] = (segmented_heartbeat[i][0], scgs_new[i])
        
        plot_heartbeat_cycle(segmented_heartbeat, "Interpolated Heartbeat Cycle")
    

# interpolate_heartbeats(segmented_heartbeats)


def dwt_decompose(segmented_heartbeats):

    normalized_heartbeats = normalize_heartbeats(segmented_heartbeats)

    for n_heartbeat in normalized_heartbeats:

        print("Normalized heartbeat: ", n_heartbeat)
        plot_heartbeat_cycle(n_heartbeat, "Raw Normalized Heartbeat Cycle")
        
        # By iteratively applying the wavelet decomposition on the approximation coefficients, 
        # the DWT can separate the original signals into multiple levels 
        # that contain components in different frequency ranges

        # get all scg values from the heartbeat cycle
        n_scgs = [x[1] for x in n_heartbeat]
        # wavelet = pywt.Wavelet('dmey')
        for i in range (1, 6): 
            coeffs = pywt.dwt(n_scgs, 'dmey')   
            cA, cD = coeffs
            print("\n\ncA: ", cA)
            print("-----\n")
            plot_heartbeat_cycle_dwt(cA, "Level " + str(i))
            n_scgs = cA
            

dwt_decompose(segmented_heartbeats)

        
    

