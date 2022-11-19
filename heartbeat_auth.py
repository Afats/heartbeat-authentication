import csv
import matplotlib.pyplot as plt
import numpy as np

def open_file(filename):
    #read in the data
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        heartbeat_secs = list(reader)
        # remove incorrect data (from pressing the left button)
        heartbeat_2secs = [x[10:] for x in heartbeat_secs]
    return heartbeat_2secs

def main():
    # data collection using the sensor




    # 
    heartbeat_2secs = open_file('../heartbeat_values/160hz/readings-mustafa-160hz.csv')

    convert_to_floats(heartbeat_2secs)

