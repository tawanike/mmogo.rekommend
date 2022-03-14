import time
from django.core.mail import send_mail
from admin.celery import app
from celery.utils.log import get_task_logger

from .models import Email, SMS
from .utils import send_sms

logger = get_task_logger(__name__)


@app.task(bind=True)
def task_send_emails(*args):
    try:
      emails = Email.objects.filter(status=False)

      for email in emails:
        sent = send_mail(
            email.subject,
            email.body,
            email.from_address,
            [email.recipient],
            fail_silently=False,
        )
        email.status = True
        email.service_email_id = email.id
        email.save()
    except Exception as error:
      print(error)

@app.task(bind=True)
def task_send_sms(*args):
    try:
      messages = SMS.objects.filter(status=False)

      for sms in messages:
        sent = send_sms(
            sms.subject,
            sms.body,
            sms.from_address,
            [sms.recipient],
            fail_silently=False,
        )
        sms.status = True
        sms.service_email_id = sms.id
        sms.save()
    except Exception as error:
      print(error)