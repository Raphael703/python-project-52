from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from task_manager.mixins import CustomLoginRequiredMixin
from task_manager.tasks.models import Task


class TaskListView(CustomLoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/list.html'
    context_object_name = 'tasks'

# Create your views here.

class TaskCreateView(CustomLoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    template_name = 'tasks/create.html'
    fields = ['name', 'description', 'status', 'executor']
    success_url = reverse_lazy('tasks_list')
    success_message = _('The task has been successfully created')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

