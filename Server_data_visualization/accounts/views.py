from forms import RegisterForm
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, Http404
from django.core.context_processors import csrf
from activation import activate_user

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/")
    else:
        form = RegisterForm()

    context = {'form': form}
    context.update(csrf(request))
    return render_to_response("accounts/register.html", context)

def activate(request):
    user = request.GET.get('user')
    code = request.GET.get('code')

    if activate_user(user,  code):
        return HttpResponseRedirect("/")
    else:
        raise Http404
