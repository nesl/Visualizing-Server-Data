from django.core.mail import send_mail
from hashlib import md5
from django.template import loader, Context
from django.contrib.auth.models import User

def send_activation(user):
    code = md5(user.username).hexdigest()
    print "user: " + user.username
    print "code: " + code
    url = "http://172.17.10.10/accounts/activate/?user=%s&code=%s" % (user.username,  code)
    print(url)
    template = loader.get_template('accounts/activation.html')
    context = Context({
        'username': user.username,
        'url': url,
    })

    send_mail('Activate ' + user.username + ' at PowerViz', template.render(context), 'no-reply@example.com', ['power.visualizer@gmail.com', 'jtsao22@gmail.com'])
    print "Sent email!"

def activate_user(username,  code):
    if code == md5(username).hexdigest():
        user = User.objects.get(username=username)
        user.is_active = True
        user.save()
        send_mail('Your PowerViz account has been activated!', 'You can now log on to PowerViz!', 'no-reply@example.com', [user.email])
        return True
    else:
        return False
