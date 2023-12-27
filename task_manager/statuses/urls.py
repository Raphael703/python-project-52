from django.urls import path
from .views import StatusListView

urlpatterns = [
    path('', StatusListView.as_view(), name='statuses_list'),
]
