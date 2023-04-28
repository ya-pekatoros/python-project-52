class InvalidUpdateCreateMixin():
    def form_invalid(self, form):
        form['password1'].value = None
        form['password2'].value = None
        if form['password2'].errors:
            for error in form.errors['password2']:
                form.add_error('password1', error)
        form.errors.pop('password2', None)
        form.add_error('password2', 'Re-enter the password above and enter it again')
        response = super().form_invalid(form)
        response.status_code = 400
        return response
