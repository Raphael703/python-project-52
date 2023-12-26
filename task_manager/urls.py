from django.contrib import admin
from django.urls import path, include

from task_manager.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('users/', include('task_manager.users.urls'))
]
