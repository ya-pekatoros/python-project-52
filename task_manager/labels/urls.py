from django.urls import path
from .views import LabelListView, LabelCreateView, LabelDeleteView, LabelUpdateView

urlpatterns = [
    path("labels/<int:pk>/delete/", LabelDeleteView.as_view(), name="label-delete"),
    path("labels/<int:pk>/update/", LabelUpdateView.as_view(), name="label-update"),
    path("labels/", LabelListView.as_view(), name='labels'),
    path("labels/create/", LabelCreateView.as_view(), name="label-create")
]
