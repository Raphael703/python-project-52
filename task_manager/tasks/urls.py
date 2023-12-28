from django.urls import path

from task_manager.tasks.views import TaskListView, TaskCreateView, TaskUpdateView

urlpatterns = [
    path('', TaskListView.as_view(), name='tasks_list'),
    path('create/', TaskCreateView.as_view(), name='task_create'),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
]
