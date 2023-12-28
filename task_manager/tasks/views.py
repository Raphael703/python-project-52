from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import ListView, CreateView, UpdateView, \
    DeleteView, DetailView

from task_manager.mixins import CustomLoginRequiredMixin
from task_manager.tasks.models import Task


class TaskListView(CustomLoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/list.html'
    context_object_name = 'tasks'


class TaskDetailView(CustomLoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/detail.html'


class TaskCreateView(CustomLoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    template_name = 'tasks/create.html'
    fields = ['name', 'description', 'status', 'executor']
    success_url = reverse_lazy('tasks_list')
    success_message = _('The task has been created')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class TaskUpdateView(CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    fields = ['name', 'description', 'status', 'executor']
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks_list')
    success_message = _('The task has been successfully changed')


class TaskDeleteView(CustomLoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks_list')
    success_message = _('The task has been successfully deleted')

    def check_task_creator(self):
        if self.get_object().creator != self.request.user:
            messages.error(
                self.request,
                _('Only the author of the task can delete it'))
            return False
        return True

    def get(self, request, *args, **kwargs):
        if not self.check_task_creator():
            return redirect('tasks_list')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not self.check_task_creator():
            return redirect('tasks_list')
        return super().post(request, *args, **kwargs)
