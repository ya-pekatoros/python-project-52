from django_filters import FilterSet, BooleanFilter
from django.forms import CheckboxInput
from .models import Task


class TaskFilter(FilterSet):

    my_tasks = BooleanFilter(
        label='Only my tasks',
        method='filter_my_tasks',
        widget=CheckboxInput()
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']

    def filter_my_tasks(self, queryset, _, value):
        if value:
            return queryset.filter(author=self.request.user)
        else:
            return queryset