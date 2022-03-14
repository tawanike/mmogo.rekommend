from django.db import models

class Messenger(models.Model):
    from_number =  models.CharField(max_length=255)
    recipient = models.CharField(max_length=255)
    body = models.TextField()
    service = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    send_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    response = models.JSONField(blank=True, null=True)
    service_email_id = models.CharField(max_length=255)

    class Meta:
        db_table = 'altur_messenger'
        verbose_name = 'Messenger'
        verbose_name_plural = 'Messenger'

    def __str__(self) -> str:
        return f"{self.body} to {self.recipient}"