# -*- coding: utf-8 -*-  
from django import forms
from django.utils.safestring import mark_safe
from django.forms.extras.widgets import SelectDateWidget
from NearsideBindings.activity.models import Activity, Location

ACTIVITY_TYPES = (
    ('a','丧心病狂'),
    ('a','广大人民群众喜闻乐见'),
)

class ActivityForm(forms.Form):
    title = forms.CharField(max_length=45,required=True)
    types = forms.ChoiceField(choices=ACTIVITY_TYPES)
    start = forms.DateTimeField()
    end = forms.DateTimeField()
    location = forms.CharField(max_length=45,required=True)
    description = forms.CharField(widget=forms.Textarea)
    image = forms.ImageField()
