import pywt
# from segmentation import segmented_heartbeats
# from feature_extraction import dwt_decompose
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate
import pandas as pd
from sklearn.svm import SVC

clf = SVC(kernel='linear')

x = pd.read_csv("temp2.csv")
a = np.array(x)
y  = np.array(x["Type"])
x = np.array(x[1:57])

clf.fit(x, y)

print(x.shape)
