import os
import select
import subprocess
import settings
import shlex
import sys
import time
import settings
from pymongo import Connection
from cStringIO import StringIO

##############################################################################
def add_to_database(daq_data, daq):
    """ This function adds the daq data to mongodb """

    # Open the daq configuration file and daq file created from running the
    # executable
    if daq == 0:
        daq_config = open(settings.ABS_PATH + "cmd/config/daq0_description", "r")
    else:
        daq_config = open(settings.ABS_PATH + "cmd/config/daq2_description", "r")

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

    # Read the daq data and store into Mongodb
    for line in daq_data:
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
                                    'time': time.time()
                                    }
                    db.data.insert(mongo_entry)
            except ValueError, e:
                pass # Noop
            if count == 15:
                break
            count += 1

    # Close the files
    daq_config.close()

##############################################################################

class LineReader(object):

    def __init__(self, fd):
        self._fd = fd
        self._buf = ''

    def fileno(self):
        return self._fd

    def readlines(self):
        data = os.read(self._fd, 4096)
        if not data:
            # EOF
            return None
        self._buf += data
        if '\n' not in data:
            return []
        tmp = self._buf.split('\n')
        lines, self._buf = tmp[:-1], tmp[-1]
        return lines

##############################################################################

if __name__ == "__main__":
    cmd = "sudo " + settings.ABS_PATH + "cmd/daq daq0"
    target = shlex.split(cmd)
    PIPE = subprocess.PIPE
    engine = subprocess.Popen(target, bufsize=0, stdout=PIPE, stderr=PIPE)

    proc_stdout = LineReader(engine.stdout.fileno())
    #proc_stderr = LineReader(engine.stderr.fileno())
    readable = [proc_stdout]

    # Connect to Mongodb
    connection = Connection('localhost', 90)
    #connection.drop_database('visual_server_db')
    db = connection.visual_server_db
    #db.create_collection('data', {'capped': True, 'size': 29304000})

    while readable:
        ready, _, _ = select.select(readable, [], [], 10.0)
        if ready is None:
            continue
        stream = ready[0]
        lines = stream.readlines()
        add_to_database(lines, 0)
        #for line in lines:
            #print line

