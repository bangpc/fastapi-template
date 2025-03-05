import yaml
import json
import pathlib
import sys
import traceback
import os
import requests
import redis
import uuid
import base64
import numpy as np
import cv2

from app.logs import LogHandler
from .decorators.auto_tracing import auto_tracing


class Redis:
    @classmethod
    def __init__(self, 
                 host: str, 
                 port: int, 
                 db: int, 
                 password: str):
        self.logger = LogHandler.get_logger("general")
        self.client = redis.Redis(host=host, 
                                  port=port,
                                  db=db,
                                  password=password)
        self.logger.info("Load redis success")
    
    @classmethod
    @auto_tracing()
    def push(
            self,
            logger, 
            message: dict, 
            task: str
        ):
        """_summary_

        Args:
            logger (_type_): _description_
            message (dict): _description_
            task (str): _description_
        """        
        body = [[], 
                {"messages":[message]}, 
                {"callbacks": None, "errbacks": None, "chain": None, "chord": None}]
        json_body = json.dumps(body)
        body_base64 = base64.b64encode(json_body.encode('utf-8')).decode('utf-8')
        str_uuid = str(uuid.uuid4().hex)
        uuid_0 = str(uuid.uuid4().hex)
        uuid_1 = str(uuid.uuid4().hex)
        uuid_2 = str(uuid.uuid4().hex)
        redis_body = {
            "body": body_base64,
            "content-encoding":"utf-8",
            "content-type":"application/json",
            "headers":{
                "argsrepr":"()",
                "eta":None,
                "expires":None,
                "group":None,
                "group_index":None,
                "id":uuid_0,
                "ignore_result":"false",
                "kwargsrepr":"replace_result_base64",
                "lang":"py",
                "origin":"gen331@d4db3e00fd2c",
                "parent_id":None,
                "retries":5,
                "root_id":uuid_0,
                "shadow":None,
                "task": task,
                "timelimit":[None,None]
            },
            "properties":{
                "body_encoding":"base64",
                "correlation_id":uuid_0,
                "delivery_info":{
                    "exchange":"",
                    "routing_key": task
                },
                "delivery_mode":2,
                "delivery_tag":uuid_2,
                "priority":0,
                "reply_to":uuid_1}}
        try:
            self.client.lpush(task, json.dumps(redis_body))
            logger.success("Pushed to redis")
        except Exception as e:
            logger.error(traceback.format_exc())
        
    @classmethod
    @auto_tracing()
    def push_with_image(
            self,
            logger, 
            message: dict, 
            task: str,
            image: np.array
        ):
        """_summary_

        Args:
            logger (_type_): _description_
            message (dict): _description_
            task (str): _description_
            image (np.array): _description_
        """        
        logger.info("Message: ", message)
        logger.info("Message type: ", type(message))
        img_uuid = str(uuid.uuid4().hex)
        uuid_0 = str(uuid.uuid4().hex)
        uuid_1 = str(uuid.uuid4().hex)
        uuid_2 = str(uuid.uuid4().hex)
        message["img_uuid"] = img_uuid
        body = [[], 
                {"messages":[message]}, 
                {"callbacks": None, "errbacks": None, "chain": None, "chord": None}]
        json_body = json.dumps(body)
        body_base64 = base64.b64encode(json_body.encode('utf-8')).decode('utf-8')

        redis_body = {
            "body": body_base64,
            "content-encoding":"utf-8",
            "content-type":"application/json",
            "headers":{
                "argsrepr":"()",
                "eta":None,
                "expires":None,
                "group":None,
                "group_index":None,
                "id":uuid_0,
                "ignore_result":"false",
                "kwargsrepr":"replace_result_base64",
                "lang":"py",
                "origin":"gen331@d4db3e00fd2c",
                "parent_id":None,
                "retries":5,
                "root_id":uuid_0,
                "shadow":None,
                "task": task,
                "timelimit":[None,None]
            },
            "properties":{
                "body_encoding":"base64",
                "correlation_id":uuid_0,
                "delivery_info":{
                    "exchange":"",
                    "routing_key": task
                },
                "delivery_mode":2,
                "delivery_tag":uuid_2,
                "priority":0,
                "reply_to":uuid_1}}

        img_encode = cv2.imencode(".jpg", image)[1]
        data_encode = np.array(img_encode)
        byte_encode = data_encode.tobytes() 
        try:
            self.client.set(img_uuid, byte_encode, ex=600)
            self.client.lpush(task, json.dumps(redis_body))            
            logger.success("Pushed to redis")
        except Exception as e:
            logger.error(traceback.format_exc())
    

    @classmethod
    @auto_tracing()
    def push_with_queue(
            self,
            logger, 
            message: dict, 
            queue: str,
            task: str
        ):
        """_summary_

        Args:
            logger (_type_): _description_
            message (dict): _description_
            queue (str): _description_
            task (str): _description_
        """        
        body = [[], 
                {"messages":[message]}, 
                {"callbacks": None, "errbacks": None, "chain": None, "chord": None}]
        json_body = json.dumps(body)
        body_base64 = base64.b64encode(json_body.encode('utf-8')).decode('utf-8')
        str_uuid = str(uuid.uuid4().hex)
        uuid_0 = str(uuid.uuid4().hex)
        uuid_1 = str(uuid.uuid4().hex)
        uuid_2 = str(uuid.uuid4().hex)
        redis_body = {
            "body": body_base64,
            "content-encoding":"utf-8",
            "content-type":"application/json",
            "headers":{
                "argsrepr":"()",
                "eta":None,
                "expires":None,
                "group":None,
                "group_index":None,
                "id":uuid_0,
                "ignore_result":"false",
                "kwargsrepr":"replace_result_base64",
                "lang":"py",
                "origin":"gen331@d4db3e00fd2c",
                "parent_id":None,
                "retries":5,
                "root_id":uuid_0,
                "shadow":None,
                "task": task,
                "timelimit":[None,None]
            },
            "properties":{
                "body_encoding":"base64",
                "correlation_id":uuid_0,
                "delivery_info":{
                    "exchange":"",
                    "routing_key": task
                },
                "delivery_mode":2,
                "delivery_tag":uuid_2,
                "priority":0,
                "reply_to":uuid_1}}
        try:
            self.client.lpush(queue, json.dumps(redis_body))
            logger.success("Pushed to redis")
        except Exception as e:
            logger.error(traceback.format_exc())