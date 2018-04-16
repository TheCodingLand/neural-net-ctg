import os
import logging
import redis
import time
import managekey

b = redis.StrictRedis(host='redis', decode_responses=True, port=6379, db=2)
logging.warning("Connected to Redis, Database 2, port 6379")

while True:

    keys = b.keys('train*')
    if len(keys) == 0:
        #easier on CPU usage
        time.sleep(0.1)
    for key in keys:
        try:
            c = b.hgetall(key)
        except:
            logging.error('Failed to deal with key %s' % key)
            b.delete(key)
            continue
        

    

        
            





