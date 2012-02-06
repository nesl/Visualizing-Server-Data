from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from django import forms
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.conf import settings

# Subprocess, to spawn new process and return output
import subprocess, shlex, signal
import stat
import time
import os
import sys
import ssh
import account_info

# Import own files
import add_to_database

# Mongo
from pymongo import Connection

##############################################################################
class UploadFileForm(forms.Form):
    """ Specifies the parameters needed by the form """

    BLADE_CHOICES = [
            ('0', '0'),
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
            ('6', '6'),
    ]
    file  = forms.FileField()
    parameters = forms.CharField(required=False)
    blade = forms.ChoiceField(choices=BLADE_CHOICES, widget=forms.Select(), initial='0')

##############################################################################
def handle_uploaded_file(f):
    """ Writes the file in chunks to the file system with RWX privileges """
    path = settings.ABS_PATH + "Server_data_visualization/uploads/executable"
    destination = open(path, "wb+")
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    # os.chmod(path, stat.S_IXUSR | stat.S_IWUSR | stat.S_IRUSR)

##############################################################################
@login_required
def upload_file(request):
    """ Runs the executable and records time elapsed """
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        form.fields['blade'].initial = [0]
        if form.is_valid():
            handle_uploaded_file(request.FILES["file"])
            file_name = request.FILES["file"].name

            # Select daq based on blade
            blade = request.POST['blade']
            if blade == 0 or blade == 1 or blade == 4:
                daq = 0
            else:
                daq = 2

            # Run the executable
            parameters = request.POST['parameters']
            start = time.time()
            s = ssh.Connection('ac' + blade, username=account_info.username, password=account_info.password)
            results = s.execute('time ~/PowerViz_Executables/executable ' + parameters)
            end = time.time()
            s.close()

            elapsed = str(end - start) + " s"
            cache.set('start_time', start, 7200)
            cache.set('end_time', end, 7200)
            print "Just set start_time to: " + str(cache.get('start_time'))
            print "Just set end_time to: " + str(cache.get('end_time'))

            # Record results to the dictionary
            c = {"results":results[0], "time": elapsed}

            return render_to_response("upload_success.html", {'c': c})

    # Create the form
    c = RequestContext(request)

    # Create the form for uploading the file
    form = UploadFileForm()
    c["form"] = form

    return render_to_response("upload.html", c)
