from django.db import models
from django.contrib.auth.models import User

# TODO Use generic content type to link invite to the app user is invited to. e.g. Pregnancy, Baby, Registry


class Invite(models.Model):
    user = models.ForeignKey(User, related_name='invitee', on_delete=models.CASCADE)
    email = models.EmailField(max_length=100)
    is_accepted = models.BooleanField(default=False)
    token = models.CharField(max_length=255)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name)

    class Meta:
        db_table = 'invitations'
        verbose_name = 'Invite'
        verbose_name_plural = 'Invites'
