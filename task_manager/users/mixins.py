from django.utils.translation import gettext_lazy as _


class InvalidUpdateCreateMixin():
    def form_invalid(self, form):
        if form['password2'].errors:
            for error in form.errors['password2']:
                form.add_error('password1', error)
        form.errors.pop('password2', None)
        form.add_error('password2', _('Re-enter the password above and enter it again'))
        response = super().form_invalid(form)
        response.status_code = 400
        return response
