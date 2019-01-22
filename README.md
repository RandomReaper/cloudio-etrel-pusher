# cloudio-endpoint-python-example
Example use of cloudio-endpoint-python

## Simple testing
0. clone the repo and go inside it
    ```
    git clone https://github.com/RandomReaper/cloudio-endpoint-python-example.git && cd cloudio-endpoint-python-example
    ```

0. Create the directory certs **inside the git repo**, containing:

    0. ca-cert.pem
    0. sample-cert.pem
    0. sample-key.pem

0. Get the CN from the certificate : `openssl x509 -in certs/sample-cert.pem -text -noout | grep '=client'`
    ```
    openssl x509 -in certs/sample-cert.pem -text -noout | grep '=client'
            Subject: CN=FEMS1, O=client
    ```

    Here the client name is 'FEMS1'

0. Edit the `sample.cfg` file
    0. username in [cloudio] MUST match the CN in the certificate
    0. name in [endpoint] MUST match the CN in the certificate

0. install the dependencies
    ```
    pip install cloudio-endpoint-python
    ```

0. run with sample expected output
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
    debug:Client rxed: @update/FEMS1/nodes/Sensor1/objects/L1_Volts/attributes/datapoint
    debug:Client rxed: @update/FEMS1/nodes/Sensor1/objects/L2_Volts/attributes/datapoint
    debug:Client rxed: @update/FEMS1/nodes/Sensor1/objects/L3_Volts/attributes/datapoint
    debug:Client rxed: @update/FEMS1/nodes/Sensor1/objects/L1_Amps/attributes/datapoint
    debug:Client rxed: @update/FEMS1/nodes/Sensor1/objects/L2_Amps/attributes/datapoint
    debug:Client rxed: @update/FEMS1/nodes/Sensor1/objects/L3_Amps/attributes/datapoint
    debug:Client rxed: @update/FEMS1/nodes/Sensor2/objects/L1_Volts/attributes/datapoint
    debug:Client rxed: @update/FEMS1/nodes/Sensor2/objects/L2_Volts/attributes/datapoint
    debug:Client rxed: @update/FEMS1/nodes/Sensor2/objects/L3_Volts/attributes/datapoint
    debug:Client rxed: @update/FEMS1/nodes/Sensor2/objects/L1_Amps/attributes/datapoint
    debug:Client rxed: @update/FEMS1/nodes/Sensor2/objects/L2_Amps/attributes/datapoint
    debug:Client rxed: @update/FEMS1/nodes/Sensor2/objects/L3_Amps/attributes/datapoint

    (60 second later...)

    Sending updates
    debug:Client rxed: @update/FEMS1/nodes/Sensor1/objects/L1_Volts/attributes/datapoint
    debug:Client rxed: @update/FEMS1/nodes/Sensor1/objects/L2_Volts/attributes/datapoint
    debug:Client rxed: @update/FEMS1/nodes/Sensor1/objects/L3_Volts/attributes/datapoint
    debug:Client rxed: @update/FEMS1/nodes/Sensor1/objects/L1_Amps/attributes/datapoint
    debug:Client rxed: @update/FEMS1/nodes/Sensor1/objects/L2_Amps/attributes/datapoint
    debug:Client rxed: @update/FEMS1/nodes/Sensor1/objects/L3_Amps/attributes/datapoint
    debug:Client rxed: @update/FEMS1/nodes/Sensor2/objects/L1_Volts/attributes/datapoint
    debug:Client rxed: @update/FEMS1/nodes/Sensor2/objects/L2_Volts/attributes/datapoint
    debug:Client rxed: @update/FEMS1/nodes/Sensor2/objects/L3_Volts/attributes/datapoint
    debug:Client rxed: @update/FEMS1/nodes/Sensor2/objects/L1_Amps/attributes/datapoint
    debug:Client rxed: @update/FEMS1/nodes/Sensor2/objects/L2_Amps/attributes/datapoint
    debug:Client rxed: @update/FEMS1/nodes/Sensor2/objects/L3_Amps/attributes/datapoint
    ```

## Running the sample in docker
0. Follow steps from simple testing, **stop before pip install**
0. Run the docker in the current directory
    ```
    docker run --rm -it -v $PWD:/data:ro python:3.7-slim /bin/bash -c "cd /data ; pip install cloudio-endpoint-python ; python main.py"
    ```

