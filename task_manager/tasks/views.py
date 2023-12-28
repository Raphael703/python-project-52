from task_manager.mixins import CustomLoginRequiredMixin
from task_manager.tasks.models import Task
class TaskListView(CustomLoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/list.html'
    context_object_name = 'tasks'

# Create your views here.
