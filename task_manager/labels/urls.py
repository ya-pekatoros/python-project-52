from django.urls import path
from .views import LabelListView, LabelCreateView, LabelDeleteView, LabelUpdateView

urlpatterns = [
    path("label/<int:pk>/delete/", LabelDeleteView.as_view(), name="label-delete"),
    path("label/<int:pk>/update/", LabelUpdateView.as_view(), name="label-update"),
    path("labels/", LabelListView.as_view(), name='labels'),
    path("label/create/", LabelCreateView.as_view(), name="label-create")
]
