from django import forms
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator

class EditProfileForm(forms.ModelForm):
    class Meta:
        exclude = ('username','first_name','is_staff','is_superuser','last_login','date_joined','password')
        model = User
        widgets = { 'avatar': forms.HiddenInput()}
