# cloudio-endpoint-python-example
Example use of cloudio-endpoint-python

## Simple testing
1. clone the repo and go inside it
    ```
    git clone https://github.com/RandomReaper/cloudio-endpoint-python-example.git && cd cloudio-endpoint-python-example
    ```

1. Create the directory certs **inside the git repo**, containing:

    * ca-cert.pem
    * sample-cert.pem
    * sample-key.pem

1. Get the CN from the certificate : `openssl x509 -in certs/sample-cert.pem -text -noout | grep '=client'`
    ```
    openssl x509 -in certs/sample-cert.pem -text -noout | grep '=client'
            Subject: CN=ENDPOINT_NAME, O=client
    ```

    Here the client name is 'ENDPOINT_NAME'

1. Edit the `sample.cfg` file
    1. username in [cloudio] MUST match the CN in the certificate
    1. name in [endpoint] MUST match the CN in the certificate

1. Install the dependencies
    ```
    pip install cloudio-endpoint-python
    ```

1. Run with sample, expected output:
    ```
    python main.py
    2019-01-22 12:34:32.903 - client - INFO - Starting MQTT client...
    2019-01-22 12:34:32.903 - cloudio.mqttreconnectclient - INFO - Stopping MqttReconnectClient thread
    2019-01-22 12:34:32.903 - cloudio.mqttreconnectclient - INFO - Starting MqttReconnectClient thread
    2019-01-22 12:34:32.903 - cloudio.mqttreconnectclient - INFO - Mqtt client reconnect thread running...
    2019-01-22 12:34:32.903 - cloudio.mqttreconnectclient - INFO - Trying to connect to cloud.iO...
    2019-01-22 12:34:32.949 - cloudio.mqttreconnectclient - INFO - Connection to cloud.iO broker established
    2019-01-22 12:34:33.938 - cloudio.mqttreconnectclient - INFO - Thread: Job done - leaving
    2019-01-22 12:34:33.938 - cloudio.mqttreconnectclient - INFO - Connected to cloud.iO broker
    Sending updates
    debug:Client rxed: @update/ENDPOINT_NAME/nodes/Sensor1/objects/L1_Volts/attributes/datapoint
    debug:Client rxed: @update/ENDPOINT_NAME/nodes/Sensor1/objects/L2_Volts/attributes/datapoint
    debug:Client rxed: @update/ENDPOINT_NAME/nodes/Sensor1/objects/L3_Volts/attributes/datapoint
    debug:Client rxed: @update/ENDPOINT_NAME/nodes/Sensor1/objects/L1_Amps/attributes/datapoint
    debug:Client rxed: @update/ENDPOINT_NAME/nodes/Sensor1/objects/L2_Amps/attributes/datapoint
    debug:Client rxed: @update/ENDPOINT_NAME/nodes/Sensor1/objects/L3_Amps/attributes/datapoint
    debug:Client rxed: @update/ENDPOINT_NAME/nodes/Sensor2/objects/L1_Volts/attributes/datapoint
    debug:Client rxed: @update/ENDPOINT_NAME/nodes/Sensor2/objects/L2_Volts/attributes/datapoint
    debug:Client rxed: @update/ENDPOINT_NAME/nodes/Sensor2/objects/L3_Volts/attributes/datapoint
    debug:Client rxed: @update/ENDPOINT_NAME/nodes/Sensor2/objects/L1_Amps/attributes/datapoint
    debug:Client rxed: @update/ENDPOINT_NAME/nodes/Sensor2/objects/L2_Amps/attributes/datapoint
    debug:Client rxed: @update/ENDPOINT_NAME/nodes/Sensor2/objects/L3_Amps/attributes/datapoint

    (60 second later...)

    Sending updates
    debug:Client rxed: @update/ENDPOINT_NAME/nodes/Sensor1/objects/L1_Volts/attributes/datapoint
    debug:Client rxed: @update/ENDPOINT_NAME/nodes/Sensor1/objects/L2_Volts/attributes/datapoint
    debug:Client rxed: @update/ENDPOINT_NAME/nodes/Sensor1/objects/L3_Volts/attributes/datapoint
    debug:Client rxed: @update/ENDPOINT_NAME/nodes/Sensor1/objects/L1_Amps/attributes/datapoint
    debug:Client rxed: @update/ENDPOINT_NAME/nodes/Sensor1/objects/L2_Amps/attributes/datapoint
    debug:Client rxed: @update/ENDPOINT_NAME/nodes/Sensor1/objects/L3_Amps/attributes/datapoint
    debug:Client rxed: @update/ENDPOINT_NAME/nodes/Sensor2/objects/L1_Volts/attributes/datapoint
    debug:Client rxed: @update/ENDPOINT_NAME/nodes/Sensor2/objects/L2_Volts/attributes/datapoint
    debug:Client rxed: @update/ENDPOINT_NAME/nodes/Sensor2/objects/L3_Volts/attributes/datapoint
    debug:Client rxed: @update/ENDPOINT_NAME/nodes/Sensor2/objects/L1_Amps/attributes/datapoint
    debug:Client rxed: @update/ENDPOINT_NAME/nodes/Sensor2/objects/L2_Amps/attributes/datapoint
    debug:Client rxed: @update/ENDPOINT_NAME/nodes/Sensor2/objects/L3_Amps/attributes/datapoint
    ```

## Running the sample in docker
1. Follow steps from simple testing, **stop before pip install**
1. Run the docker in the current directory
    ```
    docker run --rm -it -v $PWD:/data:ro python:3.7-slim /bin/bash -c "cd /data ; pip install cloudio-endpoint-python ; python main.py"
    ```

## Subscribing to messages

```
mosquitto_sub -v -h SAMPLE_CFG_CLOUDIO_HOST --insecure --cafile ./ca-cert.pem -t "@update/SAMPLE_CFG_ENDPOINT_NAME/#" -p SAMPLE_CFG_CLOUDIO_PORT -u USERNAME -P PASSWORD
@update/SAMPLE_CFG_ENDPOINT_NAME/nodes/Sensor1/objects/L1_Volts/attributes/datapoint {"timestamp": 1548221965, "type": "Number", "value": 241.38483194127764, "constraint": "Measure"}
@update/ENDPOINT_NAME/nodes/Sensor1/objects/L2_Volts/attributes/datapoint {"timestamp": 1548221965, "type": "Number", "value": 243.60132351323574, "constraint": "Measure"}
@update/ENDPOINT_NAME/nodes/Sensor1/objects/L3_Volts/attributes/datapoint {"timestamp": 1548221965, "type": "Number", "value": 208.6602533870006, "constraint": "Measure"}
@update/ENDPOINT_NAME/nodes/Sensor1/objects/L1_Amps/attributes/datapoint {"timestamp": 1548221965, "type": "Number", "value": 1.0822960860557291, "constraint": "Measure"}
@update/ENDPOINT_NAME/nodes/Sensor1/objects/L2_Amps/attributes/datapoint {"timestamp": 1548221965, "type": "Number", "value": 1.3783484402101434, "constraint": "Measure"}
@update/ENDPOINT_NAME/nodes/Sensor1/objects/L3_Amps/attributes/datapoint {"timestamp": 1548221965, "type": "Number", "value": 1.3854391014561802, "constraint": "Measure"}
@update/ENDPOINT_NAME/nodes/Sensor2/objects/L1_Volts/attributes/datapoint {"timestamp": 1548221965, "type": "Number", "value": 238.54038771602745, "constraint": "Measure"}
@update/ENDPOINT_NAME/nodes/Sensor2/objects/L2_Volts/attributes/datapoint {"timestamp": 1548221965, "type": "Number", "value": 232.46068414178478, "constraint": "Measure"}
@update/ENDPOINT_NAME/nodes/Sensor2/objects/L3_Volts/attributes/datapoint {"timestamp": 1548221965, "type": "Number", "value": 222.05393224639485, "constraint": "Measure"}
@update/ENDPOINT_NAME/nodes/Sensor2/objects/L1_Amps/attributes/datapoint {"timestamp": 1548221965, "type": "Number", "value": 0.8248346293150215, "constraint": "Measure"}
@update/ENDPOINT_NAME/nodes/Sensor2/objects/L2_Amps/attributes/datapoint {"timestamp": 1548221965, "type": "Number", "value": 0.6004553170845794, "constraint": "Measure"}
@update/ENDPOINT_NAME/nodes/Sensor2/objects/L3_Amps/attributes/datapoint {"timestamp": 1548221965, "type": "Number", "value": 0.8691650945318636, "constraint": "Measure"}

```

