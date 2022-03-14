import requests
from twilio.rest import Client
from sentry_sdk import capture_exception
from altur.announce import Announce
from mmogo.utils import format_mobile_number


class Altur:
    def __init__(self):
        self.slack = Announce()

    def send_email(self, template, payload):
        try:
            url = "https://api.sendgrid.com/v3/mail/send"
            headers = {
                "authorization": "Bearer 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",
                "content-type": "application/json"
            }

            r = requests.request("POST", url, json={
                "personalizations": [
                    {
                        "to": [
                            {
                                "email": payload.get("email"), 
                                "name": "{} {}".format(payload.get("first_name"), payload.get("last_name"))
                            }
                        ],
                        "dynamic_template_data": {
                            "subject": payload.get("subject"),
                            "customer_name": "{} {}".format(payload.get("first_name"), payload.get("last_name")),
                            "customer_email": payload.get("email"),
                            "tracking_code": payload.get("order"),
                            "products": [
                                {
                                    "title": "Product Title One",
                                    "price": "R23.50",
                                    "quantity": 2
                                },
                                {
                                    "title": "Product Title Two",
                                    "price": "R65.50",
                                    "quantity": 3
                                },
                                {
                                    "title": "Product Title Three",
                                    "price": "R23.50",
                                    "quantity": 2
                                },
                                {
                                    "title": "Product Title Four",
                                    "price": "R65.50",
                                    "quantity": 3
                                } 
                            ],
                            "total": "R1398.87"
                        },
                        "subject": payload.get("subject")
                    }
                    ],
                    "template_id": template,
                    "from": {"email": "jerry@ebutler.co.za", "name": "Jerry from eButler"},
                }, headers=headers)

            print(r.json())
        except Exception as error:
            print(error)

    def new_user(self, payload):
        return self.slack.new_user(payload)

    def payment(self, payload):
        return self.slack.payment(payload)

    def send_otp(self, payload):
        try:
            account_sid = "ACad442ee610c20131f8b58e05bfaae6f1"
            auth_token = "f07a5dab03628c732c97a2bf127c34ed"
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                body=payload['message'],
                messaging_service_sid='MGf6e7ea5eed9d274a6f4973ea0cc61e70',
                to=format_mobile_number(payload['number'])
            )
            # https://api.altur.ga/v1/conversations/rest/whatsapp/ebutler
            # https://api.altur.ga/v1/conversations/rest/websockets/ebutler
            # r = requests.post(
            #     'https://api.altur.ga/v1/conversations/rest/sms/ebutler', data=payload)
        except Exception as error:
            capture_exception(error)

    def send_receipt(self, template, payload):
        # TODO use this instead  self.send_email(template, payload)
        try:
            url = "https://api.sendgrid.com/v3/mail/send"
            headers = {
                "authorization": "Bearer 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",
                "content-type": "application/json"
            }

            r = requests.request("POST", url, json={
                "personalizations": [
                    {
                        "to": [
                            {
                                "email": payload.get("email"), 
                                "name": "{} {}".format(payload.get("first_name"), payload.get("last_name"))
                            }
                        ],
                        "dynamic_template_data": {
                            "subject": payload.get("subject"),
                            "customer_name": "{} {}".format(payload.get("first_name"), payload.get("last_name")),
                            "customer_email": payload.get("email"),
                            "tracking_code": payload.get("order"),
                            "products": payload.get("cart").get("products"),
                            "total": payload.get("cart").get("club_total"),
                            "savings": payload.get("cart").get("savings"),
                            "service_fee": payload.get("service_fee"),
                        },
                        "subject": payload.get("subject")
                    }
                    ],
                    "template_id": template,
                    "from": {"email": "jerry@ebutler.co.za", "name": "Jerry from eButler"},
                }, headers=headers)

            print(r.json())
        except Exception as error:
            print(error)

    def send_sms(self, template, payload):
        pass