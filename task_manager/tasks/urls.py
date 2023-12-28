from django.urls import path

from task_manager.tasks.views import TaskListView

urlpatterns = [
    path('', TaskListView.as_view(), name='tasks_list'),
]
