from pymongo import Connection
import time

connection = Connection('localhost', 90)
db = connection.visual_server_db

start = time.time()
time.sleep(5)
end = time.time()
time.sleep(2)
print "start: ", start
print "End: ", end
results = db.data.find({'type' : {'$regex' : '^CPU.*'}, 'time': {'$gt': start, '$lt': end}})
for result in results:
    print result
