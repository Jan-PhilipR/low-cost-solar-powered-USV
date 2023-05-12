#!/usr/bin/python

import io
import sys
import fcntl
import time
import copy
import string
import datetime
from AtlasI2C import (
	 AtlasI2C
)

def print_devices(device_list, device):
    for i in device_list:
        if(i == device):
            print("--> " + i.get_device_info())
        else:
            print(" - " + i.get_device_info())
    #print("")

def get_devices():
    device = AtlasI2C()
    device_address_list = device.list_i2c_devices()
    device_list = []

    for i in device_address_list:
        device.set_i2c_address(i)
        response = device.query("i")
        
        # check if the device is an EZO device
        checkEzo = response.split(",")
        if len(checkEzo) > 0:
            if checkEzo[0].endswith("?I"):
                # yes - this is an EZO device
                moduletype = checkEzo[1]
                response = device.query("name,?").split(",")[1]
                device_list.append(AtlasI2C(address = i, moduletype = moduletype, name = response))
    return device_list

def main():

    device_list = get_devices()

    if len(device_list) == 0:
        print ("No EZO devices found")
        exit()

    device = device_list[0]

    print_devices(device_list, device)

    while True:
        
        for dev in device_list:
                dev.write("R")
                
        time.sleep(1.5)
        for dev in device_list:
            with open("/home/pi/atlas/whitebox-raspberry-ezo/logged_data.csv", "a") as file:
                try:
                    
                    
                    print("-------------")
                    #get and print current timestamp
                    timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                    print(str(timestamp))
                    
                    #print sensor data
                    print(dev.read())
                    
                    #get sensor data
                    sensor_data = dev.query("R")
                    # write sensor data and timestamp to the file
                    file.write(timestamp + " " + str(sensor_data) + "\n")


                except IOError:
                    print("Query failed \n - Address may be invalid, use list command to see available addresses")

        time.sleep(30)
if __name__ == '__main__':
    main()
