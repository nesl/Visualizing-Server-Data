# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.views.decorators.cache import never_cache

from pymongo import Connection
from pymongo import json_util
from pymongo import DESCENDING
import json
import time

##############################################################################
# Set up connection with Mongodb
connection = Connection('localhost', 90)
db = connection.visual_server_db

# ---------------------------------------------------------------------------#
#                            Static Data                                     #
# ---------------------------------------------------------------------------#

# ---------------------------------------------------------------------------#
@login_required
def charts_menu(request):
    """ Shows the charts menu for the daq, cpu, memory, data_channel, etc. """
    return render_to_response('power/charts_menu.html',
        context_instance=RequestContext(request))

# ---------------------------------------------------------------------------#
@login_required
def posted_results(request):
    """ Passes the field and field_val (i.e. data_channel and 0) to the
    chart.html page """
    req = request.GET
    for field, field_val in req.iteritems():
        if field != "type":
            data_list = {"field": field, "field_val": int(field_val)}
        else:
            if field_val.startswith("CPU") or field_val.startswith("RAM"):
                data_list = {"field": field, "field_val": field_val}
    return render_to_response('power/chart.html', {'data_list': data_list})

# ---------------------------------------------------------------------------#
@login_required
def get_data(request, field, field_val):
    """ Returns the power data from mongo (This is called by the highchart) """
    start_time = cache.get('start_time')
    end_time = cache.get('end_time')

    print "Start:     " + str(start_time)
    print "End:       " + str(end_time)
    print "Field:     " + str(field)
    print "Field_val: " + str(field_val)

    if field != "type":
        data_list = db.data.find({field: int(field_val),\
            'time': {'$gt': start_time, '$lt': end_time}},\
            {"power":1, "time":1})
    else:
        if str(field_val) == "CPU":
            data_list = db.data.find({\
                'type': {'$regex' : '^CPU.*'},\
                'time': {'$gt': start_time, '$lt': end_time}},\
                {"power": 1, "time":1})
        elif str(field_val) == "RAM":
            data_list = db.data.find({\
                'type': {'$regex' : '^RAM.*'},\
                'time': {'$gt': start_time, '$lt': end_time}},\
                {"power": 1, "time":1})
        else:
            data_list = db.data.find({\
                field: field_val,\
                'time': {'$gt': start_time, '$lt': end_time}},\
                {"power": 1, "time":1})

    data = []
    for obj in data_list:
        data.append(obj)
    return HttpResponse(json.dumps(data, default=json_util.default))


# ---------------------------------------------------------------------------#
#                            Live   Data                                     #
# ---------------------------------------------------------------------------#

# ---------------------------------------------------------------------------#
@login_required
@never_cache
def live_results(request):
    """ Passes the field and field_val (i.e. data_channel and 0) to the
    livechart.html page """
    req = request.GET
    for field, field_val in req.iteritems():
        if field != "type":
            data_list = {"field": field, "field_val": int(field_val)}
        else:
            if field_val.startswith("CPU") or field_val.startswith("RAM"):
                data_list = {"field": field, "field_val": field_val}
    return render_to_response('power/livechart.html', {'data_list': data_list})

# ---------------------------------------------------------------------------#
@login_required
@never_cache
def get_live_data(request, field, field_val):
    """ Returns the live "power" data from mongo (Called by live highchart) """
    start_time = time.time()

    if field != "type":
        data_list = db.data.find({\
                field: int(field_val),\
                'time': {'$gt': start_time }},\
                {"power": 1, "time":1})\
                .sort("time", DESCENDING).limit(1)
    else:
        if str(field_val) == "CPU":
            data_list = db.data.find({\
                    'type': {'$regex' : '^CPU.*'},\
                    'time': {'$gt': start_time}},\
                    {"power": 1, "time":1})\
                    .sort("time", DESCENDING).limit(1)
        elif str(field_val) == "RAM":
            data_list = db.data.find({\
                    'type': {'$regex' : '^RAM.*'},\
                    'time': {'$gt': start_time}},\
                    {"power": 1, "time":1})\
                    .sort("time", DESCENDING).limit(1)
        else:
            data_list = db.data.find({\
                    field: field_val,\
                    'time': {'$gt': start_time}},\
                    {"power": 1, "time": 1})\
                    .sort("time", DESCENDING).limit(1)

    data = []
    for obj in data_list:
        data.append(obj)
    return HttpResponse(json.dumps(data, default=json_util.default))
