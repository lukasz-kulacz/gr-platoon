#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2022 gr-platoon author.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy
from gnuradio import gr

import serial
import requests
from threading import Thread

gps_string = ""

def read_gps(device_name):
    global gps_string
    global gps_enabled
    with serial.Serial(device_name) as ser:
        while True:
            gps_string = ser.readline().decode('ascii', errors='replace')
            

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
        print("GPS: ", gps_string)

        url = self.server_url + '/' + str(self.platoon_id) 
        data = {
            "gps": gps_string
        }

        response = requests.post(url, json = data)
        print(response)
        if response.status_code == 200:
            response = response.json()
            if 'freq' in response:
                return response['freq']
            else:
                return 400e6
        else: 
            return 400e6        
    
