from django.urls import path
from .views import StatusListView, StatusCreateView, StatusUpdateView

urlpatterns = [
    path('', StatusListView.as_view(), name='statuses_list'),
    path('create/', StatusCreateView.as_view(), name='status_create'),
    path('update/<int:pk>', StatusUpdateView.as_view(), name='status_update'),
]
