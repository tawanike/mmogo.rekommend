from django.conf import settings

from altur.push.expo import Expo

def send_push_notification(token, title, message):
    if settings.PUSH_NOTIFICATION_SERVICE == 'expo':
        expo = Expo()
        response = expo.send(token, title, message)
    return response