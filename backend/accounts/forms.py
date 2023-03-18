from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    
    profile_picture = forms.ImageField(required=False)
    class Meta(UserCreationForm):
        model = CustomUser
        fields =  ("email", "name", "profile_picture", )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'name')
