from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile,Comment

class Signupform(UserCreationForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','email','password1','password2']

class loginForm(forms.Form):
    username=forms.CharField(label="Username",widget=forms.TextInput(attrs={'placeholder':"Enter Your Username Or Email"}))
    password=forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'placeholder':'Enter Your Password'}))



class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model=User
        fields=[
            'username',
            'first_name',
            'last_name',
            'email',
        ]


class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        exclude=('user',)

class CommentForm(forms.ModelForm):
    content=forms.CharField(label='',widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Text goes here...!!!','rows':'4','cols':'50'}))
    class Meta:
        model=Comment
        fields=("content",)