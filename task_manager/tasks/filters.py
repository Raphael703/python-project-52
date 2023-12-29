from django.forms import CheckboxInput
from django_filters import FilterSet
from django_filters.filters import BooleanFilter, ModelChoiceFilter
from django.utils.translation import gettext as _
from task_manager.tasks.models import Task
from task_manager.labels.models import Label


class TaskFilterSet(FilterSet):
    own_tasks = BooleanFilter(
        widget=CheckboxInput,
        field_name='creator',
        method='filter_own_tasks',
        label=_('Only your own tasks'),
    )

    label = ModelChoiceFilter(
        queryset=Label.objects.all(),
        field_name='labels',
        label=_('Label'),
    )

    def filter_own_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(creator=self.request.user)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor', 'label', 'own_tasks']
