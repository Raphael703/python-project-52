from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import ListView, DeleteView, CreateView, UpdateView

from task_manager.mixins import CustomLoginRequiredMixin
from task_manager.users.forms import CustomUserCreationForm


class LoginRequiredAndUserSelfCheckMixin(CustomLoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user == self.get_object()

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        else:
            messages.error(
                self.request,
                _('You do not have permission to modify another user.'))
            return redirect('user_list')


class UserListView(ListView):
    model = get_user_model()
    template_name = 'users/list.html'
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, CreateView):
    template_name = 'users/create.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    success_message = _('The user has been successfully registered')


class UserUpdateView(LoginRequiredAndUserSelfCheckMixin, SuccessMessageMixin,
                     UpdateView):
    model = get_user_model()
    form_class = CustomUserCreationForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('user_list')
    success_message = _('User successfully updated')


class UserDeleteView(LoginRequiredAndUserSelfCheckMixin, SuccessMessageMixin,
                     DeleteView):
    model = get_user_model()
    template_name = 'users/delete.html'
    success_url = reverse_lazy('user_list')
    success_message = _('User successfully deleted')

    def post(self, request, *args, **kwargs):
        if self.get_object().created_tasks.exists() or \
                self.get_object().assigned_tasks.exists():
            messages.error(
                self.request,
                _('Unable to delete a user because it is being used'))
            return redirect('user_list')
        return super().post(request, *args, **kwargs)
