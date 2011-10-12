from django.shortcuts import render_to_response
from django.core.context_processors import csrf

def login(request):
    """ Shows the sign in screen """

    c = {}
    c.update(csrf(request))
    return render_to_response("registration/signin.html", c)
