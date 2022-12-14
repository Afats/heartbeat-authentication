#!/usr/bin/python

# should be executed with python2

import socket
import math
import time
import datetime
import struct
import StringIO
from threading import Thread
import sys
import matplotlib.pyplot as plt
import csv

UDP_REPLY_PORT = 47371 # node listens on this port for measurements

isRunning = True

xAxis = [(i/160.0) for i in range(320)]

def save_and_plot_measurements(values):
  file_name = time.asctime() + '.csv'
  with open(file_name, 'wb') as csv_file:
	wr = csv.writer(csv_file)
	wr.writerow(values)
  plt.plot(xAxis,values)
  plt.title('Heartbeat - Acceleration in z-Direction')
  plt.xlabel('Measurement time (s)')
  plt.ylabel('Acceleration (2G/2^15)')
  plt.show()
  


def udpListenThread():
  # listen on UDP socket port UDP_REPLY_PORT
  recvSocket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
  recvSocket.bind(("aaaa::1", UDP_REPLY_PORT))
  recvSocket.settimeout(0.5)

  last_packet_arrival_time = time.time()
  readings = [0]*320
  seen = set()
  while isRunning: 
    try:
      data, addr = recvSocket.recvfrom( 4000 )

      if(last_packet_arrival_time + 2 < time.time()):
        # reset all buffers
	  readings = [0]*320
          seen = set()

      last_packet_arrival_time = time.time()

      seq_num = struct.unpack("h", data[0:2])[0]
      seen.add(seq_num)
	
      print "Sequence Number: ", seq_num
      for i in range(32):
          print struct.unpack("h", data[(i+1)*2:(i+2)*2])[0]
          readings[seq_num*32+i] = struct.unpack("h", data[(i+1)*2:(i+2)*2])[0]

      if len(seen) == 10:
          print "plotting "
          yAxis = readings
          save_and_plot_measurements(readings)
          readings = [0]*320
          seen = set()

    except socket.timeout:
      pass  


# start UDP listener as a thread
t1 = Thread(target=udpListenThread)
t1.start()
print "Listening for incoming packets on UDP port", UDP_REPLY_PORT

time.sleep(1)

print "Exit application by pressing (CTRL-C)"


try:
  while True:
    # wait for application to finish (ctrl-c)
    time.sleep(1)
except KeyboardInterrupt:
  print "Keyboard interrupt received. Exiting."
  isRunning = False




