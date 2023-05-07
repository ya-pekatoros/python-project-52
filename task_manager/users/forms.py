from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User


class ResistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


class UserUpdateForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

    def clean_username(self):
        """Reject usernames that differ only in case."""
        username = self.cleaned_data.get("username")
        if (
            username
            and self.instance.username != username
            and self._meta.model.objects.filter(username__iexact=username).exists()
        ):
            self._update_errors(
                ValidationError(
                    {
                        "username": self.instance.unique_error_message(
                            self._meta.model, ["username"]
                        )
                    }
                )
            )
        else:
            return username
