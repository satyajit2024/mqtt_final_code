import redis
redis_cli = redis.Redis(host="98.70.76.242",port=6379,password="Bfl@2024#redis",db=0)

def set_data_to_redis(expire_time=None,**kwargs):
    global redis_cli
    print("Data....",kwargs)
    device_id = kwargs["deviceId"]
    redis_cli.sadd("device_ids", device_id  )
    redis_cli.expire("device_ids", 3600)
    redis_cli.hmset(f"cpu_temp/{device_id}",mapping=kwargs)
    if expire_time:
        redis_cli.expire(f"cpu_temp/{device_id}", expire_time)
    print("Data Saved Successfully........")