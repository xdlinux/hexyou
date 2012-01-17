# -*- coding: utf-8 -*-  
from django import forms
from django.utils.safestring import mark_safe

CONDITIONS = (
    ('public','允许任何人加入'),
    ('managed','需要管理员批准才能加入'),
    ('private','只有被邀请的人才能加入'),
)

GROUP_TYPES = (
    ('real','实体组织'),
    ('virtual','虚拟组织'),
)

class FoundGroup(forms.Form):
    name = forms.CharField(max_length=20)
    description = forms.CharField(widget=forms.Textarea)
    types = forms.ChoiceField(choices=GROUP_TYPES,widget=forms.RadioSelect)
    condition = forms.ChoiceField(choices=CONDITIONS,widget=forms.RadioSelect)
    avatar = forms.ImageField()