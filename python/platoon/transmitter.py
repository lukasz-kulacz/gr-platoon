#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2022 gr-platoon author.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy
from gnuradio import gr

import pynmea2
import serial
import requests
from threading import Thread

gps_string = ""

def read_gps(device_name):
    global gps_string
    global gps_enabled
    try:
        with serial.Serial(device_name) as ser:
            print('!!! GPS serial reader started')
            while True:
                line = ser.readline().decode('ascii', errors='replace')
                if line.find('GNRMC') != -1:
                    gps_string = line
    except serial.serialutil.SerialException as ex:
        print('!!! GPS serial problem:')
        print(ex)
        print(' ')
    except:
        print('!!! GPS general problem')                

class transmitter(gr.basic_block):
    """
    docstring for block transmitter
    """
    def __init__(self, platoon_id, server_url, gps_dev):
        gr.basic_block.__init__(self,
            name="transmitter",
            in_sig=[],
            out_sig=[])
        self.platoon_id = platoon_id
        self.server_url = server_url
        self.gps_dev = gps_dev

        self.new_thread = Thread(target=read_gps, args=(self.gps_dev,))
        self.new_thread.daemon = True
        self.new_thread.start()

    def communicate(self):
        #print("GPS: ", gps_string)
        
        hasGpsData = False
        try:
            nmea = pynmea2.parse(gps_string)
            #print("GPS: ", gps_string)

            latitude = nmea.latitude
            longitude = nmea.longitude
            timestamp_gps = nmea.datetime.strftime("%Y-%m-%d %H:%M:%S.%f")
            speed = nmea.spd_over_grnd if nmea.spd_over_grnd is not None else 0.0
            azimuth = nmea.true_course if nmea.true_course is not None else 0.0
        
            hasGpsData = True

        except pynmea2.nmea.ParseError as ex:
            print('ParseError')   
        except AttributeError as ex:
            print('AttributeError')


        if hasGpsData:
            url = self.server_url + '/' + str(self.platoon_id) 
            data = {
              "position": {
                "latitude": latitude,
                "longitude": longitude
              },
              "movement": {
                "timestamp_gps": timestamp_gps,
                "speed": speed,
                "azimuth": azimuth
              }
            }

            print('Request: ', data)
            response = requests.post(url, json = data)
            print('Response: ', response.status_code)
            if response.status_code == 200:
                response = response.json()
                try:
                    print('Response: ', response)
                except:
                    pass

                if 'platoon' in response and 'frequency' in response['platoon']:
                    return response['platoon']['frequency']
                else:
                    return 400e6
            else: 
                return 400e6 
        else:
            return 400e6       
        
