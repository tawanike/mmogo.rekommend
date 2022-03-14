import uuid
from .models import Order


def create_tracking_code():
    new_code = uuid.uuid4().hex[:6].upper()
    try:
        Order.objects.get(tracking_code=new_code)
        return create_tracking_code()
    except Order.DoesNotExist:
        return new_code