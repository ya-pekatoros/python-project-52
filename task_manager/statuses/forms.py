from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Status


class StatusUpdateCreateForm(forms.ModelForm):

    class Meta:
        model = Status
        fields = ['name']

        labels = {
            'name': _('Name')
        }

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        if(
            Status.objects.filter(name=name).exists()
            and self.instance.name != name
        ):
            self.add_error('name', _('A status with that name already exists.'))
        return cleaned_data
