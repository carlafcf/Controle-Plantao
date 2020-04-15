from django.db import models

from django.contrib import auth


class User(auth.models.User, auth.models.PermissionsMixin):

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    class Meta:
        ordering = ['first_name', 'last_name']
