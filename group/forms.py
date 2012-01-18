# -*- coding: utf-8 -*-  
from django import forms
from django.utils.safestring import mark_safe
from NearsideBindings.group.models import Group,MemberShip


class GroupForm(forms.ModelForm):
    class Meta:
        model=Group
        exclude = ('founder','members','avatar')
    
    def create_group(self,user):
        if self.is_valid():
            group=self.save()
            group.founder=user
            group.save()
            membership=MemberShip.objects.create(user=user,group=group,is_admin=True)
            return (True,group,membership)
        else: return (False,None,None)
    def __getitem__(self,name):
        field=forms.ModelForm.__getitem__(self,name)
        if field.errors:
            print "error: %s" % name
            self.fields[name].widget.attrs['class']=field.css_classes('error')
        return field


        

