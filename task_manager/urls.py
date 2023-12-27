from django.contrib import admin
from django.urls import path, include

from task_manager.views import index, UserLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('users/', include('task_manager.users.urls'))
]
