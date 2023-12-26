from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, CreateView, UpdateView

from task_manager.users.forms import CustomUserCreationForm


class UserListView(ListView):
    model = get_user_model()
    template_name = 'users/list.html'
    context_object_name = 'users'


class UserCreateView(CreateView):
    template_name = 'users/create.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('user_login')


class UserUpdateView(UpdateView):
    model = get_user_model()
    form_class = CustomUserCreationForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('user_list')


class UserDeleteView(DeleteView):
    model = get_user_model()
    template_name = 'users/delete.html'
    success_url = reverse_lazy('user_list')
