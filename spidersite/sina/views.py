# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.

def test(request):
	return HttpResponse("test by pzc 2018-8-17")
@login_required
def home(request):