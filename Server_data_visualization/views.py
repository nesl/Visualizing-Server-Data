from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from django import forms

# Subprocess, to spawn new process and return output
import subprocess
import settings
import stat

import os

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file  = forms.FileField()

def handle_uploaded_file(f):
    destination = open(settings.ABS_PATH + "Server_data_visualization/uploads/" + f.name, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()


def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES["file"])
            file_name = request.FILES["file"].name
            args = [settings.ABS_PATH +\
            "Server_data_visualization/uploads/" + file_name]
            print args
            p = subprocess.Popen(args,\
                    stdout=subprocess.PIPE).communicate()[0]
            #return HttpResponseRedirect('/success/url/')
            return HttpResponse(file_name + " output:\n" + p)
    else:
        form = UploadFileForm()
        c = {}
        c.update(csrf(request))
        c["form"] = form
    return render_to_response("upload.html", c)
