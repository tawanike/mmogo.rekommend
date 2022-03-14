from django.test import TestCase


class SignUpTestCase(TestCase):

  def setUp(self):
    self.first_name = 'John'
    self.last_name = 'Doe'
    self.email = 'john@doe.com'
    self.password = 'qwerty'


  def test_create_user(self):
    pass

  def test_create_user_with_password(self):
    pass

  def test_create_user_with_existing_email(self):
    pass

class SignInTestCase(TestCase):
  pass

class ActivateAccountTestCase(TestCase):
  pass

class ForgotPasswordTestCase(TestCase):
  pass

class CreatePasswordTestCase(TestCase):
  pass



