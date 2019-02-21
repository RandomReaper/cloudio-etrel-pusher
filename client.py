#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, time
import logging
import json
import ssl
import paho.mqtt.client as mqtt         # pip install paho-mqtt

from utils import path_helpers          # pip install cloudio-endpoint-python
from utils import datetime_helpers
from cloudio.mqtt_helpers import MqttConnectOptions, MqttReconnectClient

from configobj import ConfigObj         # pip install configobj

# Enable logging
logging.basicConfig(format='%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logging.getLogger(__name__).setLevel(logging.INFO)

class Sample_Client():
    """ Endpoint cloud.iO pour les données météorologiques du pvlab """
    MQTT_ERR_SUCCESS = mqtt.MQTT_ERR_SUCCESS

    log = logging.getLogger(__name__)

    def __init__(self, configFile):

        self._isConnected = False
        self._useReconnectClient = True             # Chooses the MQTT client
        config = self.parseConfigFile(configFile)

        self._qos = int(0)

        caFile = None
        if ('ca') in config['cloudio']:
            # Check if file exists
            if not os.path.isfile(config['cloudio']['ca']):
                raise RuntimeError(u'CA file \'%s\' does not exist!' % config['cloudio']['ca'])
            else:
                caFile = config['cloudio']['ca']

        clientCertFile = None
        if ('cert') in config['cloudio']:
            # Check if file exists
            if not os.path.isfile(config['cloudio']['cert']):
                raise RuntimeError(u'Client certificate file \'%s\' does not exist!' % config['cloudio']['cert'])
            else:
                clientCertFile = config['cloudio']['cert']

        clientKeyFile = None
        if ('key') in config['cloudio']:
            # Check if file exists
            if not os.path.isfile(config['cloudio']['key']):
                raise RuntimeError(u'Client private key file \'%s\' does not exist!' % config['cloudio']['key'])
            else:
                clientKeyFile = config['cloudio']['key']

        self.log.info('Starting MQTT client...')

        if not self._useReconnectClient:
            self._client = mqtt.Client()

            self._client.on_connect = self.onConnect
            self._client.on_disconnect = self.onDisconnect
            self._client.on_message = self.onMessage

            if clientCertFile:
                self._client.tls_set(ca_certs=caFile,  # CA certificate
                                     certfile=clientCertFile,  # Client certificate
                                     keyfile=clientKeyFile,  # Client private key
                                     tls_version=ssl.PROTOCOL_TLSv1_2,
                                     ciphers=None)
                self._client.tls_insecure_set(True)


            self._client.connect(config['cloudio']['host'],keepalive=60)
            self._client.loop_start()
        else:
            self.connectOptions = MqttConnectOptions()

            if clientCertFile:
                self.connectOptions._caFile = caFile
                self.connectOptions._clientCertFile = clientCertFile
                self.connectOptions._clientKeyFile = clientKeyFile
                self.connectOptions._tlsVersion = 'tlsv1.2'
                self.connectOptions._username = config['cloudio']['username']
                self.connectOptions._password = config['cloudio']['password']

            self._client = MqttReconnectClient(config['cloudio']['host'],
                                                    clientId=config['endpoint']['name'],
                                                    clean_session=True,
                                                    options=self.connectOptions)

            self._client.setOnConnectedCallback(self.onConnected)
            self._client.setOnMessageCallback(self.onMessage)

            self._client.start()

    def close(self):
        if not self._useReconnectClient:
            self._client.disconnect()
        else:
            self._client.stop()

    def parseConfigFile(self, configFile):
        global config

        config = None

        pathConfigFile = path_helpers.prettify(configFile)

        if pathConfigFile and os.path.isfile(pathConfigFile):
            config = ConfigObj(pathConfigFile)

        if config:
            # Check if most important configuration parameters are present
            assert ('cloudio') in config, 'Missing group \'cloudio\' in config file!'
            assert ('host') in config['cloudio'], 'Missing \'host\' parameter in cloudio group!'
            assert ('port') in config['cloudio'], 'Missing \'port\' parameter in cloudio group!'
            assert ('username') in config['cloudio'], 'Missing \'username\' parameter in cloudio group!'
            assert ('password') in config['cloudio'], 'Missing \'password\' parameter in cloudio group!'
        else:
            sys.exit(u'Error reading config file')

        return config

    def waitUntilConnected(self):
        while not self.isConnected():
            time.sleep(0.2)

    def isConnected(self):
        return self._isConnected

    def onConnect(self, client, userdata, flags, rc):
        if rc == 0:
            self._isConnected = True
            self.log.info('Connected to cloud.iO')
            self._subscribeToUpdatedCommands()

    def onConnected(self):
        self._isConnected = True
        self._subscribeToUpdatedCommands()

    def onDisconnect(self, client, userdata, rc):
        self.log.info('Disconnect from cloud.iO: ' + str(rc))

    def onMessage(self, client, userdata, msg):
        print('debug:Client rxed: ' + msg.topic)
        if not hasattr(self, '_observer'):
            return

        print('Client rxed: ' + msg.topic)

    def _subscribeToUpdatedCommands(self):
        (result, mid) = self._client.subscribe(u'@update/'+config['endpoint']['name']+'/#', 1)
        return True if result == self.MQTT_ERR_SUCCESS else False

    ################################################################################################################
    ### Send value
    ################################################################################################################

    def publish_ts(self, endpoint, node, object, value, timestamp):
        topic = '@update/'+endpoint+'/nodes/'+node+'/objects/'+object+'/attributes/datapoint'
        payload = {}
        payload['timestamp'] = timestamp
        payload['value'] = float(value)
        payload['type'] = "Number"
        payload['constraint'] = 'Measure'
        self._client.publish(topic, json.dumps(payload), qos=self._qos)

    def publish_ep(self, endpoint, node, object, value):
        self.publish_ts(endpoint, node, object, value, datetime_helpers.getCurrentTimestamp()/1000)

    def publish(self, node, object, value):
        self.publish_ts(config['endpoint']['name'], node, object, value)
