from django.db import models
from django.db.models.query import QuerySet
from django.contrib.auth.models import User

class PushNotificationManager(models.Manager):
    def pending(self):
        """ Filter out all emails that have not been sent yet. """
        return self.filter(status=False)

class PushNotification(models.Model):
    to =  models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField()

    data = models.CharField(max_length=255, blank=True, null=True)
    ttl = models.CharField(max_length=255, blank=True, null=True)
    expiration = models.CharField(max_length=255, blank=True, null=True)
    priority = models.CharField(max_length=255, blank=True, null=True)

    sound = models.CharField(max_length=255, blank=True, null=True)
    badge = models.IntegerField(max_length=255, blank=True, null=True)
    channelId = models.CharField(max_length=255, blank=True, null=True)

    categoryId = models.CharField(max_length=255, blank=True, null=True)
    mutableContent = models.BooleanField(default=False)

    service = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    send_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    response = models.JSONField(blank=True, null=True)
    service_push_id = models.CharField(max_length=255, blank=True, null=True)


    objects = PushNotificationManager()

    class Meta:
        db_table = 'push_notifications'
        verbose_name = 'Push Notification'
        verbose_name_plural = 'Push Notifications'

    def __str__(self) -> str:
        return f"{self.title} to {self.to}"

class PushToken(models.Model):
    user = models.ForeignKey(User, related_name="user_push_token", on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'push_tokens'
        verbose_name = 'Push Token'
        verbose_name_plural = 'Push Tokens'

    def __str__(self) -> str:
        return f"{self.user}"