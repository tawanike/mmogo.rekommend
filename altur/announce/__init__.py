import requests
from libgravatar import Gravatar
from django.conf import settings
from sentry_sdk import capture_exception


class Announce:

    def announce(self, payload):
        try:
            requests.post(settings.SLACK_WEBHOOK, json={
                "text": payload['title'],
                "blocks": [{
                    "type": "section",
                    "block_id": "user_profile",
                    "text": {
                        "type": "mrkdwn",
                        "text": payload['text']
                    }
                }]})

        except Exception as error:
            capture_exception(error)

    def new_user(self, payload):
        try:
            # Push this to happen in the background
            gravatar = Gravatar(payload['email'])
            requests.post(settings.SLACK_WEBHOOK, json={
                "text": "New user signed up!",
                "blocks": [{
                    "type": "section",
                    "block_id": "user_profile",
                    "text": {
                        "type": "mrkdwn",
                        "text": "#New user signed up! \n <https://www.ebutler.co.za/dashboard/crm/users/{id}|{first_name} {last_name}> \n {email} \n {mobile}".format_map(payload)
                    },
                    "accessory": {
                        "type": "image",
                        "image_url": gravatar.get_image(),
                        "alt_text": "New User"
                    }
                }, ]
            })
        except Exception as error:
            capture_exception(error)

    def payment(self, payload):
        try:
            requests.post(settings.SLACK_WEBHOOK, json={
                "text": payload['title'],
                "blocks": [{
                    "type": "section",
                    "block_id": "payment_notification",
                    "text": {
                        "type": "mrkdwn",
                        "text": "{title} \n <https://www.ebutler.co.za/dashboard/orders/{order}|{first_name} {last_name}> \n Amount: {amount}".format_map(payload)
                    }
                }]})
        except Exception as error:
            capture_exception(error)
