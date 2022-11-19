# Connect to Border Router
1) Create modern Ubuntu VM 
2) git clone https://github.com/contiki-os/contiki.git
3) run make tunslip6 (in contiki/tools)
4) install net-tools with `sudo apt-get update -y` and `sudo apt-get install -y net-tools`
5) Install required python dependenices
6) Connect sensortag with USB cable
7) run `sudo ./tunslip6 -B 115200 -s /dev/ttyACM0 aaaa::1/64` (in contiki/tools)
8) run python script

# Heartbeat Authentication

Base files added. 
Currently some of the hearbeat data seems to increase continuously as per the plots. Better samples needed

pip install matplotlib

# Increased Precision of Accelerometer
Too increase the precision from the accelerometer please replace the original contiki driver with the modified driver `mpu-9250-sensor.c`. It returns the raw sensor value. It can be converted to G with the following formula:

(raw_data * 1.0) / (32768 / 2);

You find the file in `contiki-git/platform/srf06-cc26xx/sensortag`

To use that file please make sure to run `make clean` before building the source code. (FYI: The sensor is per default in 2G range configured that has the highest possible precision.)
