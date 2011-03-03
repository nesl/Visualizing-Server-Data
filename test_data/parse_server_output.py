#!/usr/bin/python
import sys
from pymongo import Connection
connection = Connection('localhost', 90)

db = connection.test_database3

# f = open("output_shorter.daq2", "r")

# Channel format specific to output_shorter.daq2
# Channel format is just a (node, device) pair
channel_format = [(3, "CPU0"),
                  (3, "CPU1"),
                  (3, "RAM0"),
                  (3, "RAM1"),
                  (6, "CPU0"),
                  (6, "CPU1"),
                  (6, "RAM0"),
                  (6, "RAM1"),
                  (2, "CPU0"),
                  (2, "CPU1"),
                  (2, "RAM0"),
                  (2, "RAM1"),
                  (5, "CPU0"),
                  (5, "CPU1"),
                  (5, "RAM0"),
                  (5, "RAM1")]

for line in sys.stdin:
    tokened_line = line.split(' ')
    count = 0
    for token in tokened_line:
        try:
            node, part = channel_format[count]
            mongo_entry = { 'data_channel': count,
                            #'sampling_interval': 1, # in seconds
                            'node': node,
                            'type': part,
                            'power': float(token.lstrip('+')),
                            'daq': 2,
                            }
            db.data.insert(mongo_entry)
        except ValueError, e:
            print ''
        if count == 15:
            break
        count += 1

