import requests
from mmogo.users.models import User

url = "https://api.sendgrid.com/v3/marketing/contacts"
payload = {
    "list_ids": [
        "18e76217-5b34-4f8b-ad04-db79335c214b"
    ],
    "contacts": [{
        "city": "string (optional)",
        "country": "string (optional)",
        "email": "string (required)",
        "first_name": "string (optional)",
        "last_name": "string (optional)",
        "postal_code": "string (optional)",
        "state_province_region": "string (optional)",
        "custom_fields": {
                "is_activated": ""
        }
    }]
}

headers = {
    'authorization': "Bearer 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",
    'content-type': "application/json"
}

try:
        users = User.objects.all()
        for user in users:
            if user.justgroceries:
                justgroceries = user.justgroceries
            else:
                'None'
            response = requests.request("PUT", url, json={
                "list_ids": [
                    "18e76217-5b34-4f8b-ad04-db79335c214b"
                ],
                "contacts": [{
                    "country": "South Africa",
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "custom_fields": {
                        "e1_T": str(user.is_active),
                        "e2_T": justgroceries
                    }
                }]
            }, headers=headers)

            print(response.text)
            time.sleep(3)
