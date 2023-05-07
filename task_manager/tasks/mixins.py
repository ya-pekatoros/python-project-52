from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse


class RestrictToNonAuthorMixin:
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user.is_authenticated:
            if (
                not request.user == self.object.author
                and not request.user.is_superuser
            ):
                messages.add_message(request, messages.ERROR, self.restrict_message)
                return HttpResponseRedirect(reverse("tasks"))
        return super().dispatch(request, *args, **kwargs)
