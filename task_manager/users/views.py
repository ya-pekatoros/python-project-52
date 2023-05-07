from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView
from django.db.models.deletion import ProtectedError
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from task_manager.utils import RedirectToLoginMixin
from .forms import ResistrationForm, UserUpdateForm
from .mixins import InvalidUpdateCreateMixin


class UserListView(ListView):
    model = User

    template_name = 'task_manager/users/user_list.html'


class UserCreateView(SuccessMessageMixin, InvalidUpdateCreateMixin, CreateView):
    model = User

    form_class = ResistrationForm

    success_url = reverse_lazy('login')
    success_message = _('User has been registered successfully!')

    template_name = 'task_manager/users/user_create.html'


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'task_manager/users/login.html'

    success_message = _('Login successful!')

    def get_success_url(self):
        return reverse_lazy('index')

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, _('Invalid username or password!'))
        form.add_error('username', '')
        form.add_error('password', '')
        response = super().form_invalid(form)
        response.status_code = 400
        return response


def logout_view(request):
    logout(request)
    messages.add_message(request, messages.INFO, _('Logout successful!'))
    return HttpResponseRedirect(reverse("index"))


class UserDeleteView(SuccessMessageMixin, RedirectToLoginMixin, DeleteView):
    model = User
    success_url = reverse_lazy('users')
    template_name = 'task_manager/users/user_delete.html'
    success_message = _('User has been deleted successfully!')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user == self.object:
            messages.add_message(request, messages.ERROR, _('You can not delete yourself!'))
            return HttpResponseRedirect(reverse("users"))
        if not request.user.is_superuser:
            messages.add_message(
                request,
                messages.ERROR,
                _('You have no permission to delete users!')
            )
            return HttpResponseRedirect(reverse("users"))
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ProtectedError:
            messages.error(
                self.request,
                _('You can not delete the user who is connected to the task!')
            )
            return redirect(reverse_lazy('users'))


class UserUpdateView(
    SuccessMessageMixin,
    RedirectToLoginMixin,
    InvalidUpdateCreateMixin,
    UpdateView
):
    model = User

    form_class = UserUpdateForm

    success_url = reverse_lazy('users')
    success_message = _('User has been updated successfully!')

    template_name = 'task_manager/users/user_update.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.is_superuser and request.user != self.get_object():
            messages.add_message(
                request,
                messages.ERROR,
                _('You have no permission to edit users!')
            )
            return HttpResponseRedirect(reverse("users"))
        return super().dispatch(request, *args, **kwargs)
