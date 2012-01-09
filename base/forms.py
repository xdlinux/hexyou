# -*- coding: utf-8 -*-  
from django import forms
from django.utils.safestring import mark_safe
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


def popover(self,title,content):
    self.widget.attrs['rel']="popover"
    self.widget.attrs['data-content']=content.encode('utf-8')
    self.widget.attrs['data-original-title']=title.encode('utf-8')
    return self

forms.Field.popover=popover

def getitem(self,sp,s):
    if sp.errors:
        self.fields[s].widget.attrs['class']=sp.css_classes('error')
        ms=("<span class='error help-inline'>%s</span>" % sp.errors[0])
        return str(sp).decode('utf-8')+ms
    else:
        return str(sp).decode('utf-8')

class LoginForm(forms.Form):
    """docstring"""
    username=forms.RegexField(regex=r'\w[a-zA-Z0-9_]{1,20}',required=True)
    password=forms.CharField(max_length=32,min_length=6,required=True,widget=forms.PasswordInput)
    def __getitem__(self,s):
        return getitem(self,forms.Form.__getitem__(self,s),s)

class SignupForm(UserCreationForm):
    last_name = forms.CharField(max_length=45,required=True)
    email = forms.EmailField(max_length=75,required=True)
    student_num = forms.RegexField(regex=r'\d{8}',error_messages={'invalid':'请输入正确的学号'})

    contact_qq = forms.RegexField(regex=r'\d+',required=False,
            min_length=4,
            error_messages={'invalid':'请输入正确的QQ号(由纯数字组成)'}
            )
    contact_msn = forms.RegexField(regex=r'\S+',required=False)
    contact_fanfou = forms.RegexField(regex=r'\S+',required=False)
    contact_twitter = forms.RegexField(regex=r'\w+',required=False)

    def __init__(self,data=None):
        UserCreationForm.__init__(self,data)
        self.fields['username'].popover(u'用户名',u'请指定您的登陆用户名，用户名只能由字母、数字和下划线组成')
        self.fields['last_name'].popover(u'姓名',u'请输入您的真实姓名，以便更好地使用本站服务')
        self.fields['email'].popover(u'电子邮箱',u'请输入您的常用电子邮箱，此邮箱将会成为您的登陆邮箱和找回密码时的安全邮箱')
        self.fields['student_num'].popover(u'学号',u'请正确输入您的学号，以便我们识别出您的院系和专业')
        self.fields['password1'].popover(u'密码',u'密码由字母、数字和下划线组成，请妥善保管！')
        self.fields['password2'].popover(u'重复密码',u'重复输入密码以确认输入无误')
        self.fields['password1'].min_length=6


    class Meta:
        model = User
        fields = ("username",
                "email",
                "password1",
                "password2",
                "last_name",
                "student_num",
                "contact_qq",
                "contact_msn",
                "contact_fanfou",
                "contact_twitter",
                )
    def __getitem__(self,s):
        return getitem(self,UserCreationForm.__getitem__(self,s),s)
