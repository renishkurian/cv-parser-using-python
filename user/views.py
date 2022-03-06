from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django import forms
from django.http import HttpResponse
# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from django.contrib.auth.models import User

from user.form import UserRegister


def home(request):
    return render(request,'user/layout/app.html')
class Register(SuccessMessageMixin,CreateView):



    model = User
    template_name = "user/signup.html"

    form_class = UserRegister
    success_url = reverse_lazy('login')

    success_message = 'account created sucessfully'


class Profile(LoginRequiredMixin,DetailView):
    template_name ='user/profile.html'
    model = User
