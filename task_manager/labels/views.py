from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.deletion import ProtectedError
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from task_manager.utils import RedirectToLoginMixin

from .models import Label
from .forms import LabelUpdateCreateForm


class LabelListView(RedirectToLoginMixin, ListView):
    model = Label

    template_name = 'task_manager/labels/label_list.html'


class LabelCreateView(RedirectToLoginMixin, SuccessMessageMixin, CreateView):
    model = Label

    form_class = LabelUpdateCreateForm

    success_url = reverse_lazy('labels')
    success_message = _('Label has been created successfully!')

    template_name = 'task_manager/labels/label_create.html'

    def form_invalid(self, form):
        response = super().form_invalid(form)
        response.status_code = 400
        return response


class LabelDeleteView(RedirectToLoginMixin, SuccessMessageMixin, DeleteView):
    model = Label
    success_url = reverse_lazy('labels')
    success_message = _('Label has been deleted successfully!')
    template_name = 'task_manager/labels/label_delete.html'


    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ProtectedError:
            messages.error(self.request, _('You can not delete the Label that is assigned to the task!'))
            return redirect(reverse_lazy('labels'))

class LabelUpdateView(RedirectToLoginMixin, SuccessMessageMixin, UpdateView):
    model = Label

    form_class = LabelUpdateCreateForm

    success_url = reverse_lazy('labels')
    success_message = _('Label has been updated successfully!')

    template_name = 'task_manager/labels/label_update.html'
