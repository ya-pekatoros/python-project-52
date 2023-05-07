from django.contrib import auth


def __str__(self):
    if self.first_name == "" and self.last_name == "":
        return self.username
    return f"{self.first_name} {self.last_name}"


auth.models.User.add_to_class('__str__', __str__)
