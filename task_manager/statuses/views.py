from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.deletion import ProtectedError
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from task_manager.utils import RedirectToLoginMixin

from .models import Status
from .forms import StatusUpdateCreateForm


class StatusListView(RedirectToLoginMixin, ListView):
    model = Status

    template_name = 'task_manager/statuses/status_list.html'


class StatusCreateView(RedirectToLoginMixin, SuccessMessageMixin, CreateView):
    model = Status

    form_class = StatusUpdateCreateForm

    success_url = reverse_lazy('statuses')
    success_message = _('Status has been created successfully!')

    template_name = 'task_manager/statuses/status_create.html'

    def form_invalid(self, form):
        response = super().form_invalid(form)
        response.status_code = 400
        return response

class StatusDeleteView(RedirectToLoginMixin, SuccessMessageMixin, DeleteView):
    model = Status
    success_url = reverse_lazy('statuses')
    success_message = _('Status has been deleted successfully!')
    template_name = 'task_manager/statuses/status_delete.html'


    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ProtectedError:
            messages.error(self.request, _('You can not delete the status that is assigned to the task!'))
            return redirect(reverse_lazy('statuses'))

class StatusUpdateView(RedirectToLoginMixin, SuccessMessageMixin, UpdateView):
    model = Status

    form_class = StatusUpdateCreateForm

    success_url = reverse_lazy('statuses')
    success_message = _('Status has been updated successfully!')

    template_name = 'task_manager/statuses/status_update.html'

    def form_invalid(self, form):
        response = super().form_invalid(form)
        response.status_code = 400
        return response
