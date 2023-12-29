from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext as _


def index(request):
    return render(request, 'index.html')


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'users/login.html'
    next_page = reverse_lazy('index')
    success_message = _('You are logged in')


class UserLogoutView(SuccessMessageMixin, LogoutView):
    next_page = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _('You are logged out'))
        return super().dispatch(request, *args, **kwargs)
