import pywt
# from segmentation import segmented_heartbeats
# from feature_extraction import dwt_decompose
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate
import pandas as pd
from sklearn.svm import SVC
from feature_extraction import create_features_vector

# features vector
# create_features_vector(extracted_feature_cycles)


clf = SVC(kernel='linear')

x = pd.read_csv("temp2.csv")
a = np.array(x)
y  = np.array(x["Type"])
x = np.array(x.loc[:, x.columns != 'Type'])

clf.fit(x, y)

# print(x.shape)
# print(y.shape)

x1 = pd.read_csv("temp_testing.csv")
a1 = np.array(x1.loc[:, x1.columns != 'Type'])

# print(a1)
print(clf.predict(a1))
