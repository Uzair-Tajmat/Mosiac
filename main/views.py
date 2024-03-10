from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request,'index.html')
# Create your views here.
