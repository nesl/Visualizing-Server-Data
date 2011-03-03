from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf

from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file  = forms.FileField()

def handle_uploaded_file(f):
    destination = open('uploads/uploaded.txt', 'wx')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            #return HttpResponseRedirect('/success/url/')
            return HttpResponse("SUCCESS\n")
    else:
        print "HI"
        form = UploadFileForm()
        c = {}
        c.update(csrf(request))
        c['form'] = form
    return render_to_response('upload.html', c)
