from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Label


class LabelUpdateCreateForm(forms.ModelForm):

    class Meta:
        model = Label
        fields = ['name']

        labels = {
            'name': _('Name')
        }

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        if(
            Label.objects.filter(name=name).exists()
            and self.instance.name != name
        ):
            self.add_error('name', _('A label with that name already exists.'))
        return cleaned_data
