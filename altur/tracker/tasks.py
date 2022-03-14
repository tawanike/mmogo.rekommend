import time
from django.core.mail import send_mail
from admin.celery import app
from celery.utils.log import get_task_logger

from .models import Tracker

logger = get_task_logger(__name__)


@app.task(bind=True)
def task_update_stats(*args):
    try:
      emails = Tracker.objects.filter(status=False)

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
