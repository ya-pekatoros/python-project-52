from django.urls import path
from .views import TaskListView, TaskCreateView, TaskDeleteView, TaskUpdateView, TaskDetailView

urlpatterns = [
    path("task/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("task/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("task/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/", TaskListView.as_view(), name='tasks'),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create")
]
