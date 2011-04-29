from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from django import forms

# Subprocess, to spawn new process and return output
import subprocess, shlex
import settings
import stat

import os

import add_to_database

class UploadFileForm(forms.Form):
    """ Specifies the parameters needed by the form """
    # title = forms.CharField(max_length=50)
    file  = forms.FileField()
    params = forms.CharField(required=False)

def handle_uploaded_file(f):
    """ Writes the file in chunks to the file system with RWX privileges """
    path = settings.ABS_PATH + "Server_data_visualization/uploads/" + f.name
    destination = open(path, "wb+")
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    os.chmod(path, stat.S_IXUSR | stat.S_IWUSR | stat.S_IRUSR)

def upload_file(request):
    """ Starts the DAQ, runs the executable, and stops the DAQ """
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES["file"])
            file_name = request.FILES["file"].name

            # Start the DAQ and get PID
            cmd = "sudo" + " " + settings.ABS_PATH + "cmd/daq daq0"
            args = shlex.split(cmd)
            print "ARGS: ", args
            process = subprocess.Popen(args,\
                    stdout=subprocess.PIPE,stderr=subprocess.PIPE)

            # Run the executable
            params = request.POST['params']
            args = "time " + settings.ABS_PATH +\
            "Server_data_visualization/uploads/" + file_name + " " + params
            results = subprocess.Popen((args),\
                    stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True).communicate()

            # Stop the DAQ and get the DAQ results
            os.system("sudo kill %s" % (process.pid))
            print "STOPPING THE DAQ"
            daq_results = process.communicate()

            # Save the DAQ results to output file for reference later
            f = open("daq_results.txt", 'w')
            f.write(daq_results[0])
            f.close()

            # Add the information to the database
            add_to_database.add_to_database(0)

            # Strip only the user, system, and elapsed time from the time
            # results. Cutoff after elapsed, which is 7 characters long.
            time = results[1][:results[1].find("elapsed") + 7]

            # Record results to the dictionary
            c = {"results":results[0], "time":time}
            return render_to_response("upload_success.html", {'c': c})

        else:
            # Ask for the upload again if the form is not valid
            form = UploadFileForm()
            c = {}
            c.update(csrf(request))
            c["form"] = form

            return render_to_response("upload.html", c)

    else:
        # Create the form for uploading the file
        form = UploadFileForm()
        c = {}
        c.update(csrf(request))
        c["form"] = form

        return render_to_response("upload.html", c)
