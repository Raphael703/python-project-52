from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from task_manager.labels.models import Label
from task_manager.mixins import CustomLoginRequiredMixin


class LabelListView(CustomLoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/list.html'
    context_object_name = 'labels'


class LabelCreateView(CustomLoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    template_name = 'labels/create.html'
    fields = ['name']
    success_url = reverse_lazy('labels_list')
    success_message = _('The label has been successfully created')


class LabelUpdateView(CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    fields = ['name']
    template_name = 'labels/update.html'
    success_url = reverse_lazy('labels_list')
    success_message = _('The label has been successfully changed')


class LabelDeleteView(CustomLoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('labels_list')
    success_message = _('The label has been successfully deleted')

    def post(self, request, *args, **kwargs):
        if self.get_object().tasks.exists():
            messages.error(
                self.request,
                _('Unable to delete a label because it is being used'))
            return redirect('labels_list')
        return super().post(request, *args, **kwargs)
