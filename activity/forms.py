# -*- coding: utf-8 -*-  
from django import forms
from django.utils.safestring import mark_safe
from NearsideBindings.activity.models import Activity, Location
from NearsideBindings.base.utils import timebaseslug
from NearsideBindings.settings import RESERVED_ACTIVITY_SLUGS
from django.core.validators import validate_slug
from django.core.exceptions import ValidationError

def validate_slug_access(slug):
    if len(slug)<4 or slug in RESERVED_ACTIVITY_SLUGS:
        raise ValidationError(u'"%s" is too short or reserved ' % slug)

class ActivityForm(forms.ModelForm):

    slug = forms.SlugField(required=True,validators=[validate_slug,validate_slug_access,],initial=timebaseslug,help_text="用于url，例如http://example.com/activities/slug")
    #location = forms.ModelChoiceField(queryset=Location.objects.filter(parent=0),empty_label='请选择地点',widget=forms.Select(attrs={'class':'location'}))

    class Meta:
        model = Activity
        exclude = ('hosts','participators',)
        widgets = {
            'avatar':forms.HiddenInput(),
            'location':forms.HiddenInput(),
        }

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
    