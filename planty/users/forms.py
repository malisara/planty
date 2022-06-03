from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Hide help text in the form
        for fieldname in self.Meta.fields:
            self.fields[fieldname].help_text = None


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(max_length=50, required=False)
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)
    username = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']


class ProfileUpdateForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['image']
