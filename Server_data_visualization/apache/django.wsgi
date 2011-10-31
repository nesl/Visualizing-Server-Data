import os
import sys

paths = [
        '/data/dev/Visualizing-Server-Data',
        '/data/dev/Visualizing-Server-Data/Server_data_visualization',
        '/data/dev/Visualizing-Server-Data/Server_data_visualization/power',
        '/data/dev/Visualizing-Server-Data/cmd/'
        ]

for path in paths:
    if path not in sys.path:
        sys.path.append(path)

# # Include path to folder before project
# if path0 not in sys.path:
#     sys.path.append(path0)
# 
# # Include path to project
# if path1 not in sys.path:
#     sys.path.append(path1)
# 
# # Include path to power
# if path2 not in sys.path:
#     sys.path.append(path2)
# 
# # Include path to power
# if path2 not in sys.path:
#     sys.path.append(path2)

os.environ['DJANGO_SETTINGS_MODULE'] = 'Server_data_visualization.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
