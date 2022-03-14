from django.conf import settings

import requests



class Expo:
  def __init__(self):
    self.url = 'https://exp.host/--/api/v2/push/send'


  def send(self, token, title, message):
    headers = {'Authorization': 'Bearer {}'.format(settings.EXPO_ACCESS_TOKEN)}
    payload = {
      "to": token,
      "title":title,
      "body": message
    }

    response = requests.post(self.url, json=payload, headers=headers)
    data = response.json().get('data')
    if data.get('status') == 'ok':
      return data.get('id')
    