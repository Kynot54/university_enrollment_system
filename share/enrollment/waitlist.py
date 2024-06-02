import redis
import time
import datetime

redis_connection_pool = redis.ConnectionPool(host='localhost', port=6379, db=0)

waitlists = "Waitlists"
time_modified = "Time Modified"

# Creates a Waitlist for a Section - Registar API Call
def createWaitlist(section_id):
    r = redis.Redis(connection_pool=redis_connection_pool)
    r.sadd(waitlists, str(section_id))
    # Adds the Time Modified to the Waitlist
    r.set(f"Time Since Section Last Modified: {str(section_id)}", str(time.time()))

# Adds a Student to the Waitlist and Creates Waitlist if None Exists for that Class - Student API Call
def addWaitlists(section_id, id):
        r = redis.Redis(connection_pool=redis_connection_pool)
        if r.sismember(waitlists, section_id) == 1:
            position = r.zcard(section_id) + 1
            r.zadd(section_id, {id: position})   # Adds Student to Waitlist with Position Number in order to Track Users By Position 'Score' - Not Used to Track actual position (use rank instead)
            # Adds the Time Modified to the Waitlist
            r.set(f"Time Since Section Last Modified: {str(section_id)}", str(time.time()))
        else:
            raise LookupError("Waitlist Does Not Exist")

# Prints the Waitlist with the Positions of Each Student - Instructor API Call
def displayWaitlist(section_id):
    r = redis.Redis(connection_pool=redis_connection_pool)
    section_id = str(section_id)
    if r.sismember(waitlists, section_id) == 1:    # Error Checks to See if Waitlist Exists
        return r.zrange(section_id, 0, -1)
    else:
        raise LookupError("Waitlist Does Not Exist")

# Checks the Waitlist Position of a Student - Student API Call
def checkWaitlistPosition(section_id, id):
    r = redis.Redis(connection_pool=redis_connection_pool)
    if r.sismember(waitlists, str(section_id)) == 1:
        return r.zrank(str(section_id), id)          # Starts with '0' index; starting with '1' for normal users
    else:
        raise LookupError("Waitlist Does Not Exist")
        
# Checks the Waitlist Size to See if it is Full and Whether or Not a Student Can be Added - Student API Call
def checkWaitlistSize(section_id):
    r = redis.Redis(connection_pool=redis_connection_pool)
    return r.zcard(str(section_id))

# Checks to See if a Student is Waitlisted in More than 3 Classes - Student API Call
def checkNumberOfWaitlistEnrollments(id):
    r = redis.Redis(connection_pool=redis_connection_pool)
    section_ids = r.smembers(waitlists)
    count = 0 
    for waitlist in section_ids:
        if r.zscore(waitlist, id) is not None:
            count += 1
    return count

# Removes a Student From the Waitlist when Dropping or Being Dropped - Instructor or Student API Call
def removeWaitlist(section_id, id):
    r = redis.Redis(connection_pool=redis_connection_pool)
    try: 
        # Adds the Time Modified to the Waitlist
        r.set(f"Time Since Section Last Modified: {str(section_id)}", str(time.time()))
        r.zrem(section_id, id)    
    except:
        raise LookupError("Student Does Not Exist in Waitlist")

# Similar to removeWaitlist, but also pulls the student to be enrolled in the class - Student API Call
def removeAndAddWaitlist(section_id):
    r = redis.Redis(connection_pool=redis_connection_pool)
    if r.zcard(section_id) > 1:
        # Adds the Time Modified to the Waitlist
        r.set(f"Time Since Section Last Modified: {str(section_id)}", str(time.time()))
        student = r.zpopmin(section_id)
        student = student[0][0].decode('utf-8')
        return student
    elif r.zcard(section_id) == 1:
        last_student = r.zrevrange(section_id, 0, 0)
        last_student = last_student[0]

        r.zrem(section_id, last_student)
        r.delete(section_id)
        last_student = last_student.decode('utf-8')
        
        return last_student
        
    
# Deletes a Waitlist - Registrar API Call
def deleteWaitlist(section_id):
    r = redis.Redis(connection_pool=redis_connection_pool)
    try:
        r.srem(waitlists, section_id)
        r.zremrangebyrank(section_id, 0, -1)
    except:
        raise LookupError("Waitlist Does Not Exist")
    
def getModifiedTime(section_id):
    r = redis.Redis(connection_pool=redis_connection_pool)
    timestamp = r.get(f"Time Since Section Last Modified: {str(section_id)}")
    timestamp = int(timestamp)
    return timestamp.datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)