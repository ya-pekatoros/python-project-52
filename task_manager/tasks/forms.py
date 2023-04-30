from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

from .models import Task
from task_manager.statuses.models import Status


class TaskCreateUpdateForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor']

    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )

    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        required=True,  
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        if Task.objects.filter(name=name).exists():
            self.add_error('name', _('A task with that name already exists.'))
        return cleaned_data
