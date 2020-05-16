# Install redis_logger
* Install from pypi with pip3
```
pip3 install -i https://test.pypi.org/simple/ redis-logger==0.0.6
```

* or Install from source code
```
python3 setup.py install 
```

* Use it in your code
```
from redis_logger import * 
r = Redis(host, port, password)
log0 = RedisLog(sname = 'service_name', 
                         fname = 'function_name',
                         status = 0,
                         error = 'error info',
                         uuid = uuid0)
key = 'service_name'
r.put(key, log0)
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

# Detailed Steps for Integration on K8S
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



```
