#!/usr/bin/env python  
# -*- coding:utf-8 _*-
""" 
@author: xl
@file: mq_service.py 
@time: 2021/08/09
@contact: 
@site:  
@software: PyCharm 
"""
import asyncio
import json
import socket
import threading
from traceback import format_exc

from kafka import KafkaProducer
import os

from loguru import logger

from rosetta_service_monitor.client.conf import CONF
from rosetta_service_monitor.client.enums import WarnningType


class MQService:
    def __init__(self, conf):
        self._topic = conf.KAFKA_CONFIG.TOPIC
        self._server = conf.KAFKA_CONFIG.KAFKA_SERVER
        producer = KafkaProducer(
            bootstrap_servers=self._server,
            value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode("utf8"),
        )
        self.producer = producer

    async def send_mq(self, project_name: str, err_msg: str, trace_id: str, request: dict,
                      warnning_type: WarnningType = WarnningType.normal, **kwargs):
        hostname = socket.gethostname()
        host_info = {
            'hostname': hostname,
            'ip': os.getenv("HOST_IP") or socket.gethostbyname(hostname),
            'pod_name': os.getenv("MY_POD_NAME"),
            'pod_ip': os.getenv("POD_IP")
        }

        msg = {
            'project_name': project_name,
            'trace_id': trace_id,
            'reason': err_msg,
            'request': request,
            'hostinfo': host_info,
            'stage': warnning_type.value
        }
        msg.update(kwargs)
        future = self.producer.send(
            topic=self._topic,
            value=msg,
        )
        record_metadata = future.get(timeout=10)
        return record_metadata.topic

    def close(self):
        if self.producer is not None:
            self.producer.close()
            self.producer = None


mq_serveice = MQService(conf=CONF)
