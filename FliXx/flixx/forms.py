from django import forms
from django.forms import ModelForm
from flixx.models import user
class SignUp(ModelForm):
    class Meta:
        model = user
        widgets={
            'Password':forms.PasswordInput()
        }
        fields = ['Username', 'Name', 'Password']
class LogIn(forms.Form):
   Username=forms.CharField(max_length=10)
   Password=forms.CharField(widget=forms.PasswordInput())
class reviewing(forms.Form):
    review=forms.CharField(max_length=500)

class search (forms.Form):
    Search = forms.CharField(max_length=50)