from django.db import models

from django.contrib.auth.models import User

class Device(models.Model):
    device_id = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="user_device", on_delete=models.CASCADE, blank=True, null=True)
    online = models.BooleanField(default=False)
    app_version = models.CharField(max_length=255, blank=True, null=True)

    device_name = models.CharField(max_length=255, blank=True, null=True)
    device_year_class = models.CharField(max_length=255, blank=True, null=True)
    device_expo_version = models.CharField(max_length=255, blank=True, null=True)
    platform = models.JSONField(default=list, blank=True, null=True)

    native_app_version = models.CharField(max_length=255, blank=True, null=True)
    native_build_version = models.CharField(max_length=255, blank=True, null=True)

    push_token = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'devices'
        ordering = ['updated_at']
        verbose_name = 'Device'
        verbose_name_plural = "Devices"

    def __str__(self) -> str:
        return str(self.device_id)
