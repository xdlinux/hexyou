# -*- coding: utf-8 -*-  
from django import forms
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator,MaxLengthValidator, EMPTY_VALUES
from NearsideBindings.activity.models import Activity, Location



class IdListField(forms.CharField):

    def to_python(self,value):
        if value in EMPTY_VALUES:
            return []
        value = value.split(',')
        try:
            value = [ int(single) for single in value if single ]
        except (ValueError,TypeError):
            raise ValidationError(u'Invalid id list')
        return value


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
    