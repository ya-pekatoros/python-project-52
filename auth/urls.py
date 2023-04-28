from django.urls import path
from .views import UsersListView, UserCreateView, UserLoginView, logout_view, UserDeleteView, UserUpdateView

urlpatterns = [
    path("users/<int:pk>/delete/", UserDeleteView.as_view(), name="user-delete"),
    path("users/<int:pk>/update/", UserUpdateView.as_view(), name="user-update"),
    path("users/", UsersListView.as_view(), name='users'),
    path("users/create/", UserCreateView.as_view(), name="user-create"),
    path("login/", UserLoginView.as_view(template_name="login.html"), name='login'),
    path('logout/', logout_view, name='logout'),
]
