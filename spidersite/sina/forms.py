#--coding=utf-8
from django import forms


class EditForm(forms.Form):
	password = forms.CharField(label='密码',widget=forms.PasswordInput())
	nickname = forms.CharField(label='用户名',max_length=50)
	sina_username = forms.CharField(label='新浪账号',max_length=50)
	sina_password = forms.CharField(label='新浪密码',widget=forms.PasswordInput())
	brief = forms.CharField(widget=forms.Textarea(),max_length=100,required=False)