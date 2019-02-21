#!/usr/bin/env python3

# https://goflex-switzerland.etrel.com/UrchinWebApi/chargingSessions?chargingFrom=2019-02-13T00:00:00.000Z

import requests
import json
from datetime import datetime, timezone, timedelta
from requests.auth import HTTPBasicAuth
import dateutil.parser
import time
from client import Sample_Client
import secret

def getJson( suburl ):
    username = secret.etrel['username']
    password = secret.etrel['password']

    url_base = "https://goflex-switzerland.etrel.com/UrchinWebApi/"

    r = requests.get(url_base + suburl, auth=HTTPBasicAuth(username, password))

    return json.loads(r.text)

def timestamp ( str ):
    return dateutil.parser.parse( str ).timestamp()

# Create client
client = Sample_Client('sample.cfg')
time.sleep(1)

import random
client.publish_ep('goflex-cs-HEVS00001-04', 'Sensor1', 'L1_Volts', random.uniform(207,253))

stop = datetime.utcnow()
start = stop - timedelta(days=2)

parsed = getJson("chargingSessions?chargingFrom=" + start.isoformat())

#print(json.dumps(parsed, indent=4, sort_keys=True))

print (parsed['PagingInfo']['NumOfRows'])

for chargingSession in parsed['Content']:
    if "HEVS" not in chargingSession['ChargePoint']['FriendlyCode']:
        continue

    print ("chargingSession['ChargePoint']['FriendlyCode']:" + chargingSession['ChargePoint']['FriendlyCode'])
    print ("chargingSession['MeterActiveEnergyStart']:" + str())
    print ("chargingSession['ChargingFrom']:" + str(chargingSession['ChargingFrom']))
    print ("chargingSession['Identification']['User']['Email']:" + str(chargingSession['Identification']['User']['Email']))

    client.publish_ts(
    'goflex-cs-' + chargingSession['ChargePoint']['FriendlyCode'],
    'charger',
    'ActiveEnergy',
    chargingSession['MeterActiveEnergyStart'],
    timestamp(str(chargingSession['ChargingFrom'])+"Z")
    )

    if ('MeterActiveEnergyEnd' in chargingSession):
        print ("chargingSession['MeterActiveEnergyEnd']:" + str(chargingSession['MeterActiveEnergyEnd']))
        print ("chargingSession['ChargingTo']:" + str(chargingSession['ChargingTo']))
        client.publish_ts(
        'goflex-cs-' + chargingSession['ChargePoint']['FriendlyCode'],
        'charger',
        'ActiveEnergy',
        chargingSession['MeterActiveEnergyEnd'],
        timestamp(str(chargingSession['ChargingTo'])+"Z")
        )
        client.publish_ts(
        'goflex-cs-' + chargingSession['ChargePoint']['FriendlyCode'],
        'charger',
        'Power',
        0.0,
        timestamp(str(chargingSession['ChargingTo'])+"Z")
        )
    else:
        info = getJson("currentSessionOnlineData?email=" + str(chargingSession['Identification']['User']['Email']))
        for i in info:
            print ("i['LastCommunicationTime']:" + str(i['LastCommunicationTime']))
            print ("ts:" + str(timestamp(str(i['LastCommunicationTime']))))
            print ("i['ChargePoint']['FriendlyCode']:" + str(i['ChargePoint']['FriendlyCode']))
            print ("i['Measurements']['ActiveEnergyConsumed']:" + str(i['Measurements']['ActiveEnergyConsumed']))
            print ("i['Measurements']['Power']:" + str(i['Measurements']['Power']))
            client.publish_ts(
            'goflex-cs-' + chargingSession['ChargePoint']['FriendlyCode'],
            'charger',
            'ActiveEnergy',
            i['Measurements']['ActiveEnergyConsumed'],
            timestamp(str(i['LastCommunicationTime']))
            )
            client.publish_ts(
            'goflex-cs-' + chargingSession['ChargePoint']['FriendlyCode'],
            'charger',
            'Power',
            i['Measurements']['Power'],
            timestamp(str(i['LastCommunicationTime']))
            )
    print ("##############")
