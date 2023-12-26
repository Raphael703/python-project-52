from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy


def index(request):
    return render(request, 'index.html')


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    next_page = reverse_lazy('index')
