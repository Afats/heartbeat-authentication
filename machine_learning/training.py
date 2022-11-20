import pywt
# from segmentation import segmented_heartbeats
# from feature_extraction import dwt_decompose
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate
import pandas as pd
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn import metrics

# clf = SVC(kernel='linear')

def train(clf, train_with):
    x = pd.read_csv(train_with)
    a = np.array(x)
    y  = np.array(x["Type"])
    x = np.array(x.loc[:, x.columns != 'Type'])

    # ACCURACY CHECK
    # X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3)
    # clf.fit(X_train, y_train)
    # y_pred = clf.predict(X_test)
    # print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

    clf.fit(x, y)

    return clf

# print(x.shape)
# print(y.shape)
def authenticate_user(clf, other_file):
    # x1 = pd.read_csv("temp_testing.csv")
    x1 = pd.read_csv(other_file)
    a1 = np.array(x1.loc[:, x1.columns != 'Type'])

    # print(a1)
    print(clf.predict(a1))
    print(type(clf.predict(a1)))
    return clf.predict(a1)


# ACCURACY CHECK
# clf = SVC(kernel='linear')
# clf = train(clf, "temp2.csv")
