from admin.celery import app
from celery.utils.log import get_task_logger

from commace.contrib.shoppinglists.models import ShoppingList, Reserved
# Check for products in shopping lists that are now on special 
# Send email to user to notify them that a product on their list is now on special

logger = get_task_logger(__name__)

@app.task(bind=True)
def task_check_update_shoppinglists(*args):
    try:
      shoppinglists = Reserved.objects.filter(is_expired=False)
      for shoppinglist in shoppinglists:
        print(shoppinglist.expires_at)
    except Exception as error:
      print(error)


@app.task(bind=True)
def task_find_specials_on_lists(*args):
    try:
      pass
    except Exception as error:
      print(error)