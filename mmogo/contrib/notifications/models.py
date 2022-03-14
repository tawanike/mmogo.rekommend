from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    DELIVERED = 0
    SEEN = 1
    READ = 2

    NOTIFICATION_STATUS_CHOICES = (
        (DELIVERED, 'Delivered'),
        (SEEN, 'Seen'),
        (READ, 'Read')
    )

    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.IntegerField(default=DELIVERED, choices=NOTIFICATION_STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='notifications/', blank=True, null=True)
    user = models.ForeignKey(User, related_name='user_notifications', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='user_notifications_sender', on_delete=models.CASCADE)
    extra_context = models.JSONField(blank=True, null=True)
    
    def __str__(self):
        return str(self.title)
    
    class Meta:
        db_table = 'notifications'
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'

    @property
    def status_display(self):
        return self.NOTIFICATION_STATUS_CHOICES[self.status][1]
