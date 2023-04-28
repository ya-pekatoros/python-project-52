from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from task_manager.utils import RedirectToLoginMixin

from .models import Status


class StatusListView(RedirectToLoginMixin, ListView):
    model = Status

    template_name = 'task_manager/statuses/status_list.html'


class StatusCreateView(RedirectToLoginMixin, SuccessMessageMixin, CreateView):
    model = Status

    fields = ['name']

    success_url = reverse_lazy('statuses')
    success_message = _('Status created successfully!')

    template_name = 'task_manager/statuses/status_create.html'


class StatusDeleteView(RedirectToLoginMixin, SuccessMessageMixin, DeleteView):
    model = Status
    success_url = reverse_lazy('statuses')
    success_message = _('Status deleted successfully!')
    template_name = 'task_manager/statuses/status_delete.html'

    def post(self, request, *args, **kwargs):
        # проверка на то, что у статуса нет связанных задач!
        return super().post(request, *args, **kwargs)


class StatusUpdateView(RedirectToLoginMixin, SuccessMessageMixin, UpdateView):
    model = Status

    fields = ['name']

    success_url = reverse_lazy('statuses')
    success_message = _('Status updated successfully!')

    template_name = 'task_manager/statuses/status_update.html'
