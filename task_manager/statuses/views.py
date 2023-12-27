from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from task_manager.statuses.models import Status


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/list.html'
