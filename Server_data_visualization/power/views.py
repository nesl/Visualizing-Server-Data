# Create your views here.
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext

from pymongo import Connection
from pymongo import json_util
import json

# Set up connection with Mongodb
connection = Connection('localhost', 90)
db = connection.visual_server_db

def charts_menu(request):
    return render_to_response('power/charts_menu.html',
        context_instance=RequestContext(request))

def results(request, field, field_val):
    get_val = request.GET.get('channel')
    if get_val != None:
        field = "data_channel"
        field_val = int(get_val)

    data_list = {"field":field, "field_val":field_val}
    return render_to_response('power/detail.html', {'data_list': data_list})

def posted_results(request):
    req = request.GET
    for field, field_val in req.iteritems():
        if field != "type":
            data_list = {"field" :field, "field_val" : int(field_val)}
        else:
            if field_val.startswith("CPU") or field_val.startswith("RAM"):
                data_list = {"field" :field, "field_val" : field_val}
    return render_to_response('power/detail.html', {'data_list': data_list})

def get_data(request, field, field_val):
    if field != "type":
        data_list = db.data.find({field: int(field_val)})
    else:
        if field_val == "CPU":
            data_list = db.data.find({field: {'$regex' : '^CPU.*'}})
        elif field_val == "RAM":
            data_list = db.data.find({field: {'$regex' : '^RAM.*'}})
        else:
            data_list = db.data.find({field: field_val})

    data = []
    for obj in data_list:
        data.append(obj)
    return HttpResponse(json.dumps(data, default=json_util.default))
