from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView


class UserListView(ListView):
    model = get_user_model()
    template_name = 'users/user_list.html'
    context_object_name = 'users'
