from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from task_manager.utils import RedirectToLoginMixin

from .models import Task
from .forms import TaskCreateUpdateForm
from .mixins import RestrictToNonAuthorMixin


class TaskListView(RedirectToLoginMixin, ListView):
    model = Task

    template_name = 'task_manager/tasks/task_list.html'


class TaskCreateView(RedirectToLoginMixin, SuccessMessageMixin, CreateView):
    model = Task

    form_class = TaskCreateUpdateForm

    success_url = reverse_lazy('tasks')
    success_message = _('Task has been created successfully!')

    template_name = 'task_manager/tasks/task_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        response.status_code = 400
        return response

class TaskDeleteView(RedirectToLoginMixin, RestrictToNonAuthorMixin, SuccessMessageMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('tasks')
    success_message = _('Task has been deleted successfully!')
    template_name = 'task_manager/tasks/task_delete.html'
    restrict_message = _('Only author of the task can delete it!')


class TaskUpdateView(RedirectToLoginMixin, RestrictToNonAuthorMixin, SuccessMessageMixin, UpdateView):
    model = Task

    fields = ['name', 'description', 'status', 'executor']

    success_url = reverse_lazy('tasks')
    success_message = _('Task has been updated successfully!')

    template_name = 'task_manager/tasks/task_update.html'

    restrict_message = _('Only author of the task can edit it!')


class TaskDetailView(RedirectToLoginMixin, DetailView):
    model = Task

    fields = ['name', 'description', 'status', 'author', 'created_at', 'executor']

    template_name = 'task_manager/tasks/task_detail.html'
