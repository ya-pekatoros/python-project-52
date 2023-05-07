from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from .models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label


class TaskUpdateCreateForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']

        labels = {
            'name': _('Name')
        }

    description = forms.CharField(
        widget=forms.Textarea(),
        label=_('Description')
    )

    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        required=True,
        widget=forms.Select(),
        label=_('Status')
    )

    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=True,
        widget=forms.Select(),
        label=_('Executor')
    )

    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        required=False,
        widget=forms.SelectMultiple(),
        label=_('Labels')
    )

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        if (
            Task.objects.filter(name=name).exists()
            and self.instance.name != name
        ):
            self.add_error('name', _('A task with that name already exists.'))
        return cleaned_data
