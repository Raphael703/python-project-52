from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView


class UserListView(ListView):
    model = get_user_model()
    template_name = 'users/user_list.html'
    context_object_name = 'users'
class UserCreateView(CreateView):
    template_name = 'users/create.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('user_login')
class UserDeleteView(DeleteView):
    model = get_user_model()
    template_name = 'users/delete.html'
    success_url = reverse_lazy('user_list')
