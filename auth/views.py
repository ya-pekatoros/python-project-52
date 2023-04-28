from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _

from .forms import ResistrationForm, UserUpdateForm
from .mixins import InvalidUpdateCreateMixin


class UsersListView(ListView):
    model = User

    template_name = 'user_list.html'


class UserCreateView(InvalidUpdateCreateMixin, CreateView):
    model = User

    form_class = ResistrationForm

    success_url = reverse_lazy('login')

    template_name = 'user_create.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.add_message(self.request, messages.SUCCESS, _('User registered successfully!'))
        return response


class UserLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('index')

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, _('Invalid username or password!'))
        form.add_error('username', '')
        form.add_error('password', '')
        response = super().form_invalid(form)
        response.status_code = 400
        return response

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(
            self.request,
            username=username,
            password=password
        )
        if user is not None:
            login(self.request, user)
            messages.add_message(self.request, messages.SUCCESS, _('Login successful!'))
            return super().form_valid(form)
        else:
            self.form_invalid(self, form)

def logout_view(request):
    logout(request)
    messages.add_message(request, messages.INFO, _('Logout successful!'))
    return HttpResponseRedirect(reverse("index"))


class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('users')
    template_name = 'user_delete.html'
    
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request, messages.ERROR, _('You are not authorized, please log in!'))
            return HttpResponseRedirect(reverse("login"))
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user == self.object:
            messages.add_message(request, messages.ERROR, _('You cannot delete yourself!'))
            return HttpResponseRedirect(reverse("users"))
        if not request.user.is_superuser:
            messages.add_message(request, messages.ERROR, _('You have no permission to delete users!'))
            return HttpResponseRedirect(reverse("users"))
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('User deleted successfully!'))
        return response


class UserUpdateView(InvalidUpdateCreateMixin, UpdateView):
    model = User

    form_class = UserUpdateForm

    success_url = reverse_lazy('users')

    template_name = 'user_update.html'

    def check_permission(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request, messages.ERROR, _('You are not authorized, please log in!'))
            return HttpResponseRedirect(reverse("login"))
        if not request.user.is_superuser and request.user != self.get_object():
            messages.add_message(request, messages.ERROR, _('You have no permission to edit users!'))
            return HttpResponseRedirect(reverse("users"))
        if request.method == "POST":
            return super().post(request, *args, **kwargs)
        if request.method == "GET":
            return super().get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.check_permission(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.check_permission(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('User updated successfully!'))
        return response
