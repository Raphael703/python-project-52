from django.urls import path

from task_manager.tasks.views import TaskFilterView, TaskCreateView, \
    TaskUpdateView, TaskDeleteView, TaskDetailView

urlpatterns = [
    path('', TaskFilterView.as_view(), name='tasks_list'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('create/', TaskCreateView.as_view(), name='task_create'),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
]
