from django_filters import FilterSet, BooleanFilter
from django.forms import CheckboxInput
from django.utils.translation import gettext_lazy as _
from .models import Task


class TaskFilter(FilterSet):

    my_tasks = BooleanFilter(
        label=_('Only my tasks'),
        method='filter_my_tasks',
        widget=CheckboxInput()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['status'].label = _("Status")
        self.filters['executor'].label = _("Executor")
        self.filters['labels'].label = _("Label")

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']

    def filter_my_tasks(self, queryset, _, value):
        if value:
            return queryset.filter(author=self.request.user)
        else:
            return queryset
