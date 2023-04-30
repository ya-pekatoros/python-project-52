from django.urls import path
from .views import StatusListView, StatusCreateView, StatusDeleteView, StatusUpdateView

urlpatterns = [
    path("status/<int:pk>/delete/", StatusDeleteView.as_view(), name="status-delete"),
    path("status/<int:pk>/update/", StatusUpdateView.as_view(), name="status-update"),
    path("statuses/", StatusListView.as_view(), name='statuses'),
    path("status/create/", StatusCreateView.as_view(), name="status-create")
]
