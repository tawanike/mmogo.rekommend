import time
from django.core.mail import send_mail
from admin.celery import app
from celery.utils.log import get_task_logger

from .models import Email

logger = get_task_logger(__name__)


@app.task(bind=True)
def task_send_emails(self, *args):
    try:
      emails = Email.objects.pending()

      for email in emails:
        sent = send_mail(
            email.subject,
            email.body,
            email.from_address,
            [email.recipient],
            fail_silently=False,
        )
        print(sent)
        email.status = True
        email.service_email_id = email.id
        email.save()

        print(self)
        return sent
    except Exception as error:
      print(error)