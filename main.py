#!/usr/bin/env python
# -*- coding: utf-8 -*-

from client import Sample_Client
import time

import random

# Create client
client = Sample_Client('sample.cfg')
time.sleep(5)

# Simple exemple
while(True):
    print('Sending updates')
    client.publish('Sensor1', 'L1_Volts', random.uniform(207,253))
    client.publish('Sensor1', 'L2_Volts', random.uniform(207,253))
    client.publish('Sensor1', 'L3_Volts', random.uniform(207,253))
    client.publish('Sensor1', 'L1_Amps', random.uniform(1,2))
    client.publish('Sensor1', 'L2_Amps', random.uniform(1,2))
    client.publish('Sensor1', 'L3_Amps', random.uniform(1,2))

    client.publish('Sensor2', 'L1_Volts', random.uniform(207,253))
    client.publish('Sensor2', 'L2_Volts', random.uniform(207,253))
    client.publish('Sensor2', 'L3_Volts', random.uniform(207,253))
    client.publish('Sensor2', 'L1_Amps', random.uniform(1,2)/2)
    client.publish('Sensor2', 'L2_Amps', random.uniform(1,2)/2)
    client.publish('Sensor2', 'L3_Amps', random.uniform(1,2)/2)

    time.sleep(60)
