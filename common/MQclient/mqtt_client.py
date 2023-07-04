#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: MQTT.py
@time: 2023/4/23 18:54
@desc:
"""
import json
import sys

import paho.mqtt.client as mqtt


class MQTTClient:
    def __init__(self, broker_address, topic):
        self.broker_address = broker_address
        self.topic = topic

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

    def on_publish(self, client, userdata, mid):
        print("Message " + str(mid) + " published.")

    def send_message(self, message):
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_publish = self.on_publish
        client.connect(self.broker_address)
        client.loop_start()
        client.publish(self.topic, json.dumps(message))
        client.loop_stop()


msg = {
    "datapoint": [
        {
            "value": "492875336",
            "type": "string",
            "index": "0"
        },
        {
            "value": "2023-04-24T15:48:33.128Z",
            "type": "string",
            "index": "6"
        },
        {
            "value": 0,
            "type": "byte",
            "index": "7"
        },
        {
            "value": "11132.00",
            "type": "float",
            "index": "8"
        },
        {
            "index": "11",
            "type": "string",
            "value": "粤EJC5V3"
        },
        {
            "index": "12",
            "type": "string",
            "value": "1"
        },
        {
            "index": "13",
            "type": "string",
            "value": "/08188228a72a85f08b38ba"
        },
        {
            "index": "14",
            "type": "string",
            "value": "/CgjLoBoA310.jpg"
        },
        {
            "index": "18",
            "type": "string",
            "value": "20230423174821"
        }
    ],
    "from_id": "492875336",
    "msg_id": "1682243313128531625",
    "time": "2023-04-23T19:48:33.128Z",
    "type": "SYNC"
}
if __name__ == '__main__':
    p = sys.argv[0]
    rab = MQTTClient(broker_address='1.2.3.4', topic='9999999')
    rab.send_message(msg)
