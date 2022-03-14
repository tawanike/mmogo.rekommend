from admin.celery import app
from celery.utils.log import get_task_logger

from altur.push.models import PushNotification

from .utils import send_push_notification

logger = get_task_logger(__name__)


@app.task(bind=True)
def task_send_push_notifications(self, *args):
    try:
      notifications = PushNotification.objects.pending()
      for notification in notifications:
        sent = send_push_notification(notification.to, notification.title, notification.body)
        notification.status = True
        notification.service_push_id = sent
        notification.save()

    except Exception as error:
      print(error)