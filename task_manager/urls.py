from django.urls import path
from django.urls import include

urlpatterns = [
    path('', include('task_manager.users.urls')),
    path('', include('task_manager.statuses.urls')),
    path('', include('task_manager.tasks.urls')),
    path('', include('task_manager.labels.urls')),
]
