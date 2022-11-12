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
  recvSocket.settimeout(2)

  counter = 0
  readings = []
  while isRunning: 
    try:
      data, addr = recvSocket.recvfrom( 8000 )
      print data
      print len(data)
      print type(data)
      if(len(data) < 64):
          print "plotting "
          yAxis = readings
          plot_measurements(readings)
	  readings = []
      else:
          for i in range(16):
	       print struct.unpack("I", data[i*4:(i+1)*4])[0]
	       readings.append(struct.unpack("I", data[i*4:(i+1)*4])[0])
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




