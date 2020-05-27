# Install redis_logger
* Install from pypi with pip3
```
pip3 install -i https://test.pypi.org/simple/ redis-logger==0.0.6
```

* or Install from source code [Recommended for service on Aliyun]
```
python3 setup.py install 
```

# Local test
* Start the redis server:
```
redis-server /usr/local/etc/redis.conf
```
* Start the route_guide gRpc server:
```
cd examples
python3 route_guide_server.py
```
* Run the route_guide client:
```
cd examples
python3 route_guide_client.py
```
* Check the Redis Logs
```
cd tests/
python3 test_redis_logger.py
```
* Expected results (both client and server generated logs and pushed into redis):
```
Service Name:route_guide_server
Function Name:GetFeature
Status:0
Error:single log error at server side
UUID:0c464df8-9581-11ea-833c-acde48001122
Timestamp:1589419207
Total Logs:1
Service Name:route_guide_client
Function Name:guide_get_feature
Status:0
Error:single log error at client side
UUID:0c464df8-9581-11ea-833c-acde48001122
Timestamp:1589419207
Total Logs:1
```

# Integration on K8S
* Install from source
```
git clone https://github.com/valiantljk/redis-logger
cd redis-logger
python3 setup.py install --user
```
* Modify your code
```
from redis_logger import * 
import uuid 


# check if upstream service pass in a uuid, if not, generate a new one and pass on to downstream service
request_info = request.request_info # assumed uuid is wrapped in request_info from upstream service, in the form of 'someinfo[uuid]someotherinfo'
if '[' in request_info:
    uuid0 = request_info[request_info.find('[')+1:request_info.find(']')]
else:
    #if no uuid found, then generate a new random one 
    uuid0 = str(uuid.uuid1())

###################################
#Initialize Redis Logger
host = os.getenv('RedisHost', default = '172.20.15.142')
port = os.getenv('RedisPort', default = '6379')
password = os.getenv('RedisPass', default = None)
r = Redis(host, port, password)
#Construct a Log
rlog0 = RedisLog(sname = 'human_detection_alarm_server', 
                     fname = 'DetectHumanFromVideo',
                     status = status,
                     error = "{}\t{}\t{}".format(request.video_url, label, score),
                     uuid = uuid0)
key = 'human_detection_alarm_server'
r.put(key, rlog0)
###################################

```

# Validation
Connect the cluster's vpn first.
* Use redis-cli to validate
```
#redis-cli -h 172.20.15.142 -p 6379 lrange keyname start_offset end_offset
redis-cli -h 172.20.15.142 -p 6379 lrange human_detection_alarm_server 0 1
```
* Use program to validate
```
python3 test_redis_logger.py human_detection_alarm_server 
```
```
This will print all logs for key=human_detection_alarm_server in human-readable fromat, e.g., 
UUID:9e17930e-9bd0-11ea-9728-e2a089bbf5e8
Timestamp:1590113090
Service Name:human_detection_alarm_server
Function Name:DetectHumanFromVideo
Status:1
Error:https://test.cdn.sunmi.com/VIDEO/MOTION/B63BB39511C8A2205BC3E81BC45CE84C	0	0.29689615964889526
UUID:e54680dc-9bd0-11ea-a4cf-e2a089bbf5e8
Timestamp:1590113210
Total Logs:339
```

# Current Keys
EVENT_ANALYSIS
head_detection_server
human_detection_alarm_server