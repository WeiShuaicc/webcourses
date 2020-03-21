import redis
#redis数据库 decode_responses默认转换

r = redis.Redis(host='localhost', port=6379, db=0, charset="utf8", decode_responses=True )

r.set("mobile", "123")
r.expire("mobile", 1)#过期设置
import time
time.sleep(1)
print(r.get("mobile"))