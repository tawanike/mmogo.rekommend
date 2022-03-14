from admin.celery import app
from celery.utils.log import get_task_logger

from .models import SMS
from .utils import send_sms

logger = get_task_logger(__name__)

@app.task(bind=True)
def task_send_smses(*args):
    try:
      messages = SMS.objects.filter(status=False)

      for sms in messages:
        # sent = send_sms(
        #     sms.recipient,
        #     sms.body
        # )
        sms.status = True
        # sms.service_sms_id = sent.get('sid')
        sms.save()
        # return sent
    except Exception as error:
      print(error)