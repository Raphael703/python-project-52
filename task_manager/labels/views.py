from django.contrib.messages.views import SuccessMessageMixin
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
