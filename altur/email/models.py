from django.db import models

class EmailManager(models.Manager):
    def pending(self):
        """ Filter out all emails that have not been sent yet. """
        return self.filter(status=False)

class Email(models.Model):
    subject = models.CharField(max_length=255)
    from_address = models.CharField(max_length=255)
    recipient = models.CharField(max_length=255)
    body = models.TextField()
    service = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    send_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    response = models.JSONField(blank=True, null=True)
    service_email_id = models.CharField(max_length=255)

    objects = EmailManager()

    class Meta:
        db_table = 'email'
        verbose_name = 'Email'
        verbose_name_plural = 'Emails'

    def __str__(self) -> str:
        return f"{self.subject} to {self.recipient}"
