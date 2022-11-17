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

def normalize_heartbeats(segmented_heartbeats):
    # step 1: normalize the SCG signals of each heartbeat cycle 
    # by dividing with the maximum amplitude of the cycle.

    # get the max len among all the heartbeat cycles
    max_len = 0
    for heartbeat_cycle in segmented_heartbeats:
        if (len(heartbeat_cycle) > max_len):
            max_len = len(heartbeat_cycle)

    

    for heartbeat_cycle in segmented_heartbeats:

        # get max amplitude
        max_amplitude = max([x[1] for x in heartbeat_cycle])

        # normalize the heartbeat cycle
        for i in range(len(heartbeat_cycle)):
            heartbeat_cycle[i] = (heartbeat_cycle[i][0], heartbeat_cycle[i][1]/max_amplitude)
        
        # append zeros at the end of each heartbeat cycle to guarantee the same duration
        if (len(heartbeat_cycle) < max_len):
            heartbeat_cycle = heartbeat_cycle + [(heartbeat_cycle[-1][0] + 0.001, 0) for i in range(max_len - len(heartbeat_cycle))]


    return segmented_heartbeats


def plot_heartbeat_cycle(heartbeat_cycle, title):
    x = [x[0] for x in heartbeat_cycle]
    y = [x[1] for x in heartbeat_cycle]
    plt.plot(x, y)
    plt.title(title)
    plt.xlabel("Time (seconds)")
    plt.ylabel("Acceleration (m/s^2)")
    plt.show()


def plot_heartbeat_cycle_dwt(heartbeat_cycle, heartbeat_timeline, title):
    # x = [x[0] for x in heartbeat_timeline]
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
            plot_heartbeat_cycle_dwt(cA, n_heartbeat, "Level " + str(i))
            n_scgs = cA
            

dwt_decompose(segmented_heartbeats)

        
    

