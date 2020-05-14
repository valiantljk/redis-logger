#!/usr/bin/env python
# coding: utf-8

# Author: Jialin Liu
# Python Version: 3.7
# Redis Version: 6.0.1
# About: A simple logger based on Redis
import redis
import time
import pickle


class RedisLog():
    """
    RedisLog structure
        service_name: str, service name, eg., head-detection
        func_name: str, function name within a service, e.g., detect()
        status: str, status code, 1: ok, 0: error
        error: str, error infor for the service crash, can paste from Exception
        uuid: universal id for tracing back, sending from application level, down to base service
        timestamp: auto-generated unix timestamp whenever a log is produced

    """
    def __init__(self, sname = 'RedisLog', fname = 'NA', status = 1, error = None, uuid = 0):
        self.service_name = sname
        self.func_name = fname
        self.status = status
        self.error = error
        self.uuid = uuid
        self.timestamp = int(time.time())
    def print(self):
        print("Service Name:%s"%self.service_name)
        print("Function Name:%s"%self.func_name)
        print("Status:%s"%self.status)
        print("Error:%s"%self.error)
        print("UUID:%s"%self.uuid)
        print("Timestamp:%s"%self.timestamp)
            
class Redis():
    """
    Redis Class
        serialize: serialize python objects using pickle
        set_expire: set expire on a key
        get_ttl: get expire of a key
        put: put logs into redis
        get: get logs from redis
    """
    def __init__(self, host, port, password):
        try:
            self.redis = redis.StrictRedis(host = host,
                                    port = port,
                                    password = password)
        except Exception as e:
            #redis can not be connected
            self.redis = None
            #user should check if redis is none or not before proceeding
            pass
    def serialize(self, objs):
        """
        objs: list of python objects
        return: list of picked objects, [] if failed
        """
        try:
            pobjs=[]
            for o in objs:
                pobjs.append(pickle.dumps(o))
            return pobjs
        except Exception as e:
            print (e)
            return []
    def set_expire(self, key, ts):
        """
        key: service name
        ts: time in seconds
        return: -1 if fail
        """
        try:
            self.redis.pexpire(key,ts*1000)
        except Exception as e:
            print (e)
            return -1
    def get_ttl(self, key):
        """
        key: service name
        return: time (seconds) before expire, -1 if fail
        """
        try:
            t = self.redis.pttl(key)
            return t/1000
        except Exception as e:
            print(e)
            return -1
    def put(self, key, values):
        """
        key: service name
        values: list of logs or a single log
        return: number of logs inserted, 0 if nothing inserted        
        """
        if isinstance(values, list):
            if(len(values) ==0):
                return 0
        else:
            if values:
                values = [values]
            else:
                # values is none
                return 0
        try:
            #push all values into redis' list tail
            #serialize first
            vobjs = self.serialize(values)
            #push all objects to redis 
            if self.redis:
                self.redis.rpush(key,*vobjs)
                return len(vobjs)
            else:
                return 0
        except Exception as e:
            #in case of expection, push a simple error log into redis
            print (e)
            rlog = RedisLog(fname = 'rpush', status = 0, error = e)
            rlog_obj = self.serialize([rlog])
            try:
                self.redis.rpush('RedisLog',rlog_obj)
            except Exception as e:
                #redis failed with best try
                print (e)
                return 0
    def get(self, key, num=None):
        """
        key: service name
        num: number of logs to get
        return: list of RedisLog or [] if none found
        """
        #get latest num logs from service key
        Logs = []
        try:
            if num != None and num >0:
                objs = self.redis.lrange(key, -num, -1)
            else:
                objs = self.redis.lrange(key,0,-1)
                #print("objs:",objs)
            for o in objs:
                Logs.append(pickle.loads(o))
            return Logs
        except Exception as e:
            print (e)
            return []






