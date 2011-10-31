from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from django import forms
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

# Subprocess, to spawn new process and return output
import subprocess, shlex, signal
import settings
import stat
import time
import os
import sys
import ssh
import account_info

# Import own files
import add_to_database


# Forms
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
    # title = forms.CharField(max_length=50)
    file  = forms.FileField()
    parameters = forms.CharField(required=False)
    blade = forms.ChoiceField(choices=BLADE_CHOICES, widget=forms.RadioSelect)

def handle_uploaded_file(f):
    """ Writes the file in chunks to the file system with RWX privileges """
    # path = settings.ABS_PATH + "Server_data_visualization/uploads/" + f.name
    path = settings.ABS_PATH + "Server_data_visualization/uploads/executable"
    destination = open(path, "wb+")
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    # os.chmod(path, stat.S_IXUSR | stat.S_IWUSR | stat.S_IRUSR)

@login_required
def upload_file(request):
    """ Starts the DAQ, runs the executable, and stops the DAQ """
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES["file"])
            file_name = request.FILES["file"].name

            # Add a one second buffer
            time.sleep(1)

            # Obtain root privileges
            # os.setuid(0)

            # Select daq based on blade
            blade = request.POST['blade']
            if blade == 0 or blade == 1 or blade == 4:
                daq = 0
            else:
                daq = 2

            # Start the DAQ and get PID
            cmd = "sudo " + settings.ABS_PATH + "cmd/daq daq" + str(daq)
            args = shlex.split(cmd)
            #args = cmd
            #print "ARGS: " , args
            #process = subprocess.Popen(['sudo', settings.ABS_PATH + "cmd/daq\
                    #daq" + str(daq)],\
            process = subprocess.Popen(args,\
                    stdout=subprocess.PIPE,stderr=subprocess.PIPE)


            # Copy the executable
            #args = "scp " + settings.ABS_PATH +\
                    #"Server_data_visualization/uploads/executable nesl@ac"\
                    #+ blade + ":~/PowerViz_Executables"
            #print "Args: " + args
            #results = subprocess.Popen(args, stdout=subprocess.PIPE,\
                    #stderr=subprocess.PIPE, shell=True).communicate()

            # Run the executable
            parameters = request.POST['parameters']
            #args = "ssh nesl@ac" + blade + " time ~/PowerViz_Executables/executable " + parameters
            #print "ARGS: " , args
            #results = subprocess.Popen((args),\
                    #stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True).communicate()

            start = time.time()
            s = ssh.Connection('ac' + blade, username=account_info.username, password=account_info.password)
            results = s.execute('time ~/PowerViz_Executables/executable ' + parameters)
            elapsed = str(time.time() - start) + " s"
            s.close()

            # Add a one second buffer
            time.sleep(1)

            # Stop the DAQ and get the DAQ results
            print "STOPPING PID: ", process.pid
            os.system("sudo kill -9 %s" % (process.pid))
            #process.kill()
            daq_results = process.communicate()

            print "DAQ_RESULTS: " + daq_results[0]
            print "\n"
            print "DAQ_ERR: " + daq_results[1]
            print "\n"

            print "Results: " , results

            # If no errors or the comedi device is not busy
            if results == None or daq_results[1].find("busy") == -1:
                print "GOT IN HERE"
                # Save the DAQ results to output file for reference later
                f = open(settings.ABS_PATH + "Server_data_visualization/daq_results.txt", "w")
                f.write(daq_results[0])
                f.close()

                # Add the information to the database in another process
                add_to_database.add_to_database(daq)

                # Strip only the user, system, and elapsed time from the time
                # results. Cutoff after elapsed, which is 7 characters long.

                #etime = results[1][:results[1].find("elapsed") + 7]
                #print "etime: " +  etime

                # Record results to the dictionary
                c = {"results":results[0], "time": elapsed}
            else:
                # Report the error
                if results[1] == None:
                    c = {"results":results[1], "time":0}
                else:
                    c = {"results":"The daq is currently being used by\
                    another process.", "time":0}
            return render_to_response("upload_success.html", {'c': c})

    # Create the form
    c = RequestContext(request)
    # Create the form for uploading the file
    form = UploadFileForm()
    c["form"] = form

    return render_to_response("upload.html", c)
