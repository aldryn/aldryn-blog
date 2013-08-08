from django.db import models
from django.contrib.auth.models import User


class UsersWithPermsManyToManyField(models.ManyToManyField):

    def __init__(self, perms, **kwargs):

        (super(UsersWithPermsManyToManyField, self)
         .__init__(User, limit_choices_to=self.get_limit_choices_to(perms),
                   **kwargs))

    def get_limit_choices_to(self, perms):
        return (models.Q(user_permissions__codename__in=perms)
                | models.Q(groups__permissions__codename__in=perms)
                | models.Q(is_superuser=True))
