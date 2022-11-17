# multi-level feature extraction of the segmented heartbeat cycles using Discrete Wavelet Transform (DWT)


# The DWT decomposes SCG signals into five levels with level 1 to 5 represent signal components 
# in the frequency range of 25 ∼ 50 Hz, 12.5 ∼ 25 Hz, 6.25 ∼ 12.5 Hz, 3.13 ∼ 6.25 Hz and 1.56 ∼ 3.13 Hz, respectively. 
# To reduce noise in the SCG signal, we only use the detailed coefficients from the second level to the fourth level 
# as the feature vector for heartbeat authentication.

import pywt
from segmentation import segmented_heartbeats
import matplotlib.pyplot as plt
import numpy as np


def plot_heartbeat_cycle(heartbeat_cycle, title):
    x = [x[0] for x in heartbeat_cycle]
    y = [x[1] for x in heartbeat_cycle]
    plt.plot(x, y)
    plt.title(title)
    plt.xlabel("Time (seconds)")
    plt.ylabel("Acceleration (m/s^2)")
    plt.show()


def plot_heartbeat_cycle_dwt(heartbeat_cycle, heartbeat_timeline, title):
    x = [x[0] for x in heartbeat_timeline]
    y = [x for x in heartbeat_cycle]

    # append x with mean values for length of y-x
    if (len(x) < len(y)):
        x = x + [np.mean(x) for i in range(len(y) - len(x))]

    plt.plot(x, y)
    plt.title(title)
    plt.xlabel("Time (seconds)")
    plt.ylabel("Acceleration (m/s^2)")
    plt.show()

for segmented_heartbeat in segmented_heartbeats:
    print("Segmented heartbeat: ", segmented_heartbeat)
    plot_heartbeat_cycle(segmented_heartbeat, "Raw Heartbeat Cycle")
    
    # By iteratively applying the wavelet decomposition on the approximation coefficients, 
    # the DWT can separate the original signals into multiple levels 
    # that contain components in different frequency ranges

    # get all scg values from the heartbeat cycle
    segmented_scgs = [x[1] for x in segmented_heartbeat]

    for i in range (1, 6): 
        coeffs = pywt.dwt(segmented_scgs, 'db1')   
        cA2, cD2 = coeffs
        plot_heartbeat_cycle_dwt(cA2, segmented_heartbeat, "Level " + str(i))
        segmented_scgs = cA2
        



        
    

