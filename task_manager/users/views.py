from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import ListView, DeleteView, CreateView, UpdateView

from task_manager.users.forms import CustomUserCreationForm


class LoginRequiredAndUserPassesTestMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.pk == self.kwargs['pk']

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                _('You are not logged in! Please sign in.'))
            return redirect('login')
        else:
            messages.error(
                self.request,
                _('You do not have permission to modify another user.'))
            return redirect('user_list')


class UserListView(ListView):
    model = get_user_model()
    template_name = 'users/list.html'
    context_object_name = 'users'


class UserCreateView(CreateView):
    template_name = 'users/create.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')


class UserUpdateView(LoginRequiredAndUserPassesTestMixin, SuccessMessageMixin,
                     UpdateView):
    model = get_user_model()
    form_class = CustomUserCreationForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('user_list')
    success_message = _('User successfully updated')


class UserDeleteView(LoginRequiredAndUserPassesTestMixin, SuccessMessageMixin,
                     DeleteView):
    model = get_user_model()
    template_name = 'users/delete.html'
    success_url = reverse_lazy('user_list')
    success_message = _('User successfully deleted')
