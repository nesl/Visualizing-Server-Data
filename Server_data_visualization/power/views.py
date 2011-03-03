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
db = connection.test_database3

def charts_menu(request):
    return render_to_response('power/charts_menu.html',
        context_instance=RequestContext(request))

def results(request, field, field_val):
    # print "POST: ",request.GET.get('channel')
    get_val = request.GET.get('channel')
    if get_val != None:
        field = "data_channel"
        field_val = int(get_val)

    data_list = {"field":field, "field_val":field_val}
    return render_to_response('power/detail.html', {'data_list': data_list})

def posted_results(request):
    # print "POST: ",request.GET.get('channel')
    req = request.GET
    for field, field_val in req.iteritems():
        print "field: ", field
        print "field_val: ", field_val
        if field != "type":
            data_list = {"field" :field, "field_val" : int(field_val)}
        else:
            if field_val.startswith("CPU") or field_val.startswith("RAM"):
                data_list = {"field" :field, "field_val" : field_val}
    return render_to_response('power/detail.html', {'data_list': data_list})

def get_data(request, field, field_val):
    print "POST: ",request.GET.get('sub')
    data = []
    if field != "type":
        data_list = db.data.find({field: int(field_val)})
    else:
        if field_val == "CPU":
            data_list = db.data.find({field: {'$regex' : '^CPU.*'}})
        elif field_val == "RAM":
            data_list = db.data.find({field: {'$regex' : '^RAM.*'}})
        else:
            data_list = db.data.find({field: field_val})

    for obj in data_list:
        data.append(obj)
    return HttpResponse(json.dumps(data, default=json_util.default))

def handle_uploaded_file(f):
    destination = open('home/nesl/test.txt', 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

def upload_file(request):
    print "I'm IN UPLOAD FILE\n"
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render_to_response('upload.html', {'form': form})
