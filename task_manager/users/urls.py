from django.urls import path
from .views import (
    UserListView,
    UserCreateView,
    UserLoginView,
    logout_view,
    UserDeleteView,
    UserUpdateView
)

urlpatterns = [
    path("users/<int:pk>/delete/", UserDeleteView.as_view(), name="user-delete"),
    path("users/<int:pk>/update/", UserUpdateView.as_view(), name="user-update"),
    path("users/", UserListView.as_view(), name='users'),
    path("users/create/", UserCreateView.as_view(), name="user-create"),
    path("login/", UserLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
]
