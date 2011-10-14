from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from activation import send_activation
from threading import Thread

class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")

    class Meta:
        model = User
        fields = ("username", "email", )

    def clean_email(self):
        email = self.cleaned_data["email"]

        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email

        raise forms.ValidationError("A user with that email address already exists.")

    def save(self):
        user = super(RegisterForm, self).save(commit=False)
        user.is_active = False

        thread = Thread(target=send_activation,  args=[user])
        thread.setDaemon(True)
        thread.start()
        user.save()
