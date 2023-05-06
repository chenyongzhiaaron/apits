#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: RabbitMQSender.py
@time: 2023/4/23 16:44
@desc:
"""
import json

import pika


class RabbitMQSender:
    def __init__(self, host, queue_name=None, exchange_name=None, exchange_type=None, routing_key=None):
        """
        RabbitMQSender 类的构造函数。AMQP 协议默认
        参数：
        - host: RabbitMQ 服务器的主机地址。
        - queue_name: 队列名称。如果指定了该参数，则消息将被发送到指定的队列。
        - exchange_name: 主题交换机名称。如果指定了该参数，则消息将被发送到指定的主题交换机。
        - exchange_type: 主题交换机类型。如果指定了 exchange_name 参数，则必须指定此参数。例如，'direct' 或 'topic'。
        - routing_key: 路由键。如果指定了 exchange_name 参数，则必须指定此参数。路由键用于将消息路由到特定的队列。
        """
        self.host = host
        self.queue_name = queue_name
        self.exchange_name = exchange_name
        self.exchange_type = exchange_type
        self.routing_key = routing_key
        self.connection = None
        self.channel = None

    def connect(self):
        """
        连接到 RabbitMQ 服务器，并根据需要声明队列和交换机。
        """
        # 连接到 RabbitMQ 服务器
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        self.channel = self.connection.channel()

        # 如果指定了 exchange_name 参数，则声明主题交换机
        if self.exchange_name:
            self.channel.exchange_declare(exchange=self.exchange_name, exchange_type=self.exchange_type)

        # 如果指定了 queue_name 参数，则声明队列，并将其绑定到主题交换机上
        if self.queue_name:
            self.channel.queue_declare(queue=self.queue_name)
            if self.exchange_name:
                self.channel.queue_bind(queue=self.queue_name, exchange=self.exchange_name,
                                        routing_key=self.routing_key)

    def send_message(self, message):
        """
        发送一条消息到指定的队列或主题。
        参数：
        - message: 要发送的消息。
        """
        # 如果指定了 queue_name 参数，则将消息发送到指定的队列
        if self.queue_name:
            self.channel.basic_publish(exchange='', routing_key=self.queue_name, body=message)
        # 如果指定了 exchange_name 参数，则将消息发送到指定的主题交换机
        elif self.exchange_name:
            self.channel.basic_publish(exchange=self.exchange_name, routing_key=self.routing_key, body=message)

    def close(self):
        """
        关闭与 RabbitMQ 的连接。
        """
        self.connection.close()


if __name__ == '__main__':
    msg = {
        "datapoint": [
            {
                "value": "492875336",
                "type": "string",
                "index": "0"
            },
            {
                "value": "2023-04-23T17:48:33.128Z",
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
                "index": "18",
                "type": "string",
                "value": "20230423174821"
            }
        ],
        "from_id": "492875336",
        "msg_id": "1682243313128531625",
        "time": "2023-04-23T17:48:33.128Z",
        "type": "SYNC"
    }
    rab = RabbitMQSender(host='192.1.1.59:1883', exchange_name='/bridge/492/rtdata',
                         # exchange_type='topic',
                         # routing_key='connected'
                         )
    rab.send_message(json.dumps(msg))
