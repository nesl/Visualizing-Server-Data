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
    path = settings.ABS_PATH + "Server_data_visualization/uploads/" + f.name
    destination = open(path, "w+")
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    os.chmod(path, stat.S_IXUSR | stat.S_IWUSR | stat.S_IRUSR)

    #fd = os.open(settings.ABS_PATH + "Server_data_visualization/uploads/" +
    #        f.name,


def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES["file"])
            file_name = request.FILES["file"].name
            args = [settings.ABS_PATH +\
            "Server_data_visualization/uploads/" + file_name]
            print args
            results = subprocess.Popen(args,\
                    stdout=subprocess.PIPE).communicate()[0]
            c = {"results":results}
            return render_to_response("upload_success.html", {'c': c})
            #return HttpResponse(file_name + " output:\n" + p)
    else:
        form = UploadFileForm()
        c = {}
        c.update(csrf(request))
        c["form"] = form
    return render_to_response("upload.html", c)
