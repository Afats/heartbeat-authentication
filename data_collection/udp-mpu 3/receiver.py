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

UDP_REPLY_PORT = 47371 # node listens for reply packets (UTC time) on this port

isRunning = True

xAxis = [(i/160.0) for i in range(320)]

def plot_measurements(values):
  print len(values)
  plt.plot(xAxis,values)
  plt.title('Hearbeat - Acceleration in z-Direction')
  plt.xlabel('Measurement time (s)')
  plt.ylabel('Acceleration (G)')
  plt.show()
  


def udpListenThread():
 # listen on UDP socket port UDP_REPLY_PORT
  recvSocket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
  recvSocket.bind(("aaaa::1", UDP_REPLY_PORT))
  recvSocket.settimeout(0.5)

  counter = 0
  readings = [0]*320
  seen = set()
  while isRunning: 
    try:
      data, addr = recvSocket.recvfrom( 4000 )

      seq_num = struct.unpack("h", data[0:2])[0]
      seen.add(seq_num)
	
      print "Sequence Number"
      print seq_num
      for i in range(32):
          print struct.unpack("h", data[(i+1)*2:(i+2)*2])[0]
          readings[seq_num*32+i] = struct.unpack("h", data[(i+1)*2:(i+2)*2])[0]

      if len(seen) == 10:
          print "plotting "
          yAxis = readings
          plot_measurements(readings)
          readings = [0]*320
          seen = set()

      counter += 1
      print counter

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




