from django.conf import settings
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


def update_profile():
  pass