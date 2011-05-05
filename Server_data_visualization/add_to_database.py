#!/usr/bin/python
import sys
from pymongo import Connection


def add_to_database(daq):
    connection = Connection('localhost', 90)
    connection.drop_database('visual_server_db')
    db = connection.visual_server_db

    daq_file = open("daq_results.txt", "r")

    # Channel format specific to config/daq0_description
    # and config/daq2_description
    # Channel format is just a (node, device) pair if(daq == 0):
    if daq == 0:
        channel_format = [(0, "CPU0"),
                          (0, "CPU1"),
                          (0, "RAM0"),
                          (0, "RAM1"),
                          (-1, "CPU0"),
                          (-1, "CPU1"),
                          (-1, "RAM0"),
                          (-1, "RAM1"),
                          (4, "CPU0"),
                          (4, "CPU1"),
                          (4, "RAM0"),
                          (4, "RAM1"),
                          (1, "CPU0"),
                          (1, "CPU1"),
                          (1, "RAM0"),
                          (1, "RAM1")]
    else:
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

    for line in daq_file:
        tokened_line = line.split(' ')
        count = 0
        for token in tokened_line:
            try:
                node, part = channel_format[count]
                if token != "+nan":
                    mongo_entry = { 'data_channel': count,
                                    'node': node,
                                    'type': part,
                                    'power': float(token.lstrip('+')),
                                    'daq': daq,
                                    }
                    db.data.insert(mongo_entry)
            except ValueError, e:
                print ''
            if count == 15:
                break
            count += 1

add_to_database(0)
