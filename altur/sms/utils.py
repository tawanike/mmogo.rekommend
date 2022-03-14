import random

from django.conf import settings
from sentry_sdk import capture_exception

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

def send_sms(number, message, service='twilio'):
  if service == 'twilio':
    try:
      message = client.messages.create(to=number, from_=settings.TWILIO_FROM_NUMBER, body=message)
      print(message)
      return message
    except TwilioRestException as e:
      print(e)
  else:
    pass

def format_mobile(number):
  strip_zero = number[1:]
  return f"+27{strip_zero}"

def generate_mobile_code():
  return random.sample(range(0, 9), 6)


