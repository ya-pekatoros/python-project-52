from django.urls import path
from .views import StatusListView, StatusCreateView, StatusDeleteView, StatusUpdateView

urlpatterns = [
    path("statuses/<int:pk>/delete/", StatusDeleteView.as_view(), name="status-delete"),
    path("statuses/<int:pk>/update/", StatusUpdateView.as_view(), name="status-update"),
    path("statuses/", StatusListView.as_view(), name='statuses'),
    path("statuses/create/", StatusCreateView.as_view(), name="status-create")
]
