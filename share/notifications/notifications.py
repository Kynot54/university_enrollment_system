import redis

redis_connection_pool = redis.ConnectionPool(host='localhost', port=6379, db=0)

def addSubscription(student_id, section_id, email, web_hook):
    r = redis.Redis(connection_pool=redis_connection_pool)
    subscription_key = f"student:{student_id}:subscriptions"
    info_key = f"student:{student_id}:info"
    # Add the section_id to the set of subscriptions
    r.sadd(subscription_key, str(section_id))
    # Map the email and web_hook to the hash set to store the subscription info
    data = {"email": str(email), "web_hook": str(web_hook)}
    r.hset(info_key, mapping=data)

def listSubscriptions(student_id):
    r = redis.Redis(connection_pool=redis_connection_pool)
    subscription_key = f"student:{student_id}:subscriptions"
    # Return a set of all the subscriptions
    return r.smembers(subscription_key)

def removeSubscription(student_id, section_id):
    r = redis.Redis(connection_pool=redis_connection_pool)
    subscription_key = f"student:{student_id}:subscriptions"
    info_key = f"student:{student_id}:info"
    r.srem(subscription_key, str(section_id))
    # If there are no sections the student is subscribed to, remove the student's info
    if r.scard(subscription_key) == 0:
        r.hdel(info_key)

def getSubscriptionInfo(student_id):
    r = redis.Redis(connection_pool=redis_connection_pool)
    info_key = f"student:{student_id}:info"
    # Return a dict of the student's info for the RabbitMQ producer and the RabbitMQ consumer processes
    byte_dict = r.hgetall(info_key)
    
    converted_dict = {k.decode("utf-8"): v.decode("utf-8") for k, v in byte_dict.items()}
    return converted_dict

def is_student_subscribed(student_id, section_id):
    r = redis.Redis(connection_pool=redis_connection_pool)
    subscription_key = f"student:{student_id}:subscriptions"
    # Used to Error 
    return r.sismember(subscription_key, str(section_id))
