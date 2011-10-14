from forms import RegisterForm
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/")
    else:
        form = RegisterForm()

    return render_to_response("accounts/register.html",  {'form': form,  })
