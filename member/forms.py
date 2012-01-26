from django import forms
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator

class EditProfileForm(forms.ModelForm):

    password_confirm = forms.CharField(max_length=128,widget=forms.PasswordInput(),validators=[MaxLengthValidator,])

    class Meta:
        exclude = ('username','first_name','is_staff','is_superuser','last_login','date_joined')
        model = User
        widgets = { 'avatar': forms.HiddenInput(), 'password':forms.PasswordInput(), }
