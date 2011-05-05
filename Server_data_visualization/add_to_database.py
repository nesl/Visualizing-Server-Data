#!/usr/bin/python
import sys
from pymongo import Connection


def add_to_database(daq):

    # Connect to Mongodb
    connection = Connection('localhost', 90)
    connection.drop_database('visual_server_db')
    db = connection.visual_server_db

    # Open the daq configuration file and daq file created from running the
    # executable
    if daq == 0:
        daq_config = open("../cmd/config/daq0_description", "r")
    else:
        daq_config = open("../cmd/config/daq2_description", "r")
    daq_file = open("daq_results.txt", "r")


    # Read daq configuration file
    config = daq_config.readline()
    token_list = config.split(" ")

    channel_format = [] # Channel format is a (node, device) list
    counter = 0
    daq_channel = []
    for token in token_list:
        daq_channel.append(token)
        if counter >= 2 or token.count('"') == 2:
            if token.count('"') != 2:
                # Read daq channel line such as:
                # "Node 0: CPU0"
                node = daq_channel[1].replace(':', '')
                peripheral = daq_channel[2].replace('",', '')
                channel_format.append((int(node),peripheral))
            else:
                # Parse N/C channels
                channel_format.append((-1, "N/C"))
            daq_channel = []
            counter = 0
        else:
            counter += 1

    # Read the daq file and store the data into Mongodb
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

    # Close the files
    daq_file.close()
    daq_config.close()
