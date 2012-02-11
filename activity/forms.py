# -*- coding: utf-8 -*-  
from django import forms
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
from NearsideBindings.base.forms import IdListField
from NearsideBindings.activity.models import Activity, Location

class ActivityForm(forms.ModelForm):
    host_groups = IdListField(required=False)
    inform_users = IdListField(required=False)
    class Meta:
        model = Activity
        exclude = ('hosts','participators',)
        widgets = {
            'avatar':forms.HiddenInput(),
            'location':forms.HiddenInput(),
            'description':forms.Textarea(attrs={'rows':7,})
        }

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
    