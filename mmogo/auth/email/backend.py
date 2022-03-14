from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User


class EmailAuthBacked(object):
  def authenticate(self, request, email=None, password=None):
    try:
      user = User.objects.get(email=email)
      is_valid = check_password(password, user.password)
      if is_valid:
        return user
      else:
        return None
    except User.DoesNotExist:
      # TODO Handle user does not exist
      return None


  def has_perm(self, perm, obj=None):
    "Does the user have a specific permission?"
    # Simplest possible answer: Yes, always
    return True