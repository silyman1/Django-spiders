#--coding=utf-8
from django import forms


class EditForm(forms.Form):

	nickname = forms.CharField(label='昵称',max_length=50)
	sina_username = forms.CharField(label='新浪账号',max_length=50)
	sina_password = forms.CharField(label='新浪密码')
	brief = forms.CharField(widget=forms.Textarea(attrs={'cols':'80','rows':'40'}),max_length=100,required=False)