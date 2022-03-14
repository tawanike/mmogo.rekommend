import requests, json, os, pprint
from django.db.models.signals import post_save
from django.dispatch import receiver

from commace.payments.models import Payment


@receiver(post_save, sender=Payment)
def verify_payment(sender, instance, created, **kwargs):
  if created:
    sec_key = os.environ.get("PAYSTACK_SECRET_KEY")
    payment = Payment.objects.get(id=instance.id)

    url = 'https://api.paystack.co/transaction/verify/{payment.reference}'
    try:
        headers = {'Authorization': 'Bearer ' + sec_key, 'Content-Type': 'application/json'}
        request = requests.get(url=url, headers=headers)
        response = request.json()
        response = request.data['data']
        
        payment.amount = response['amount']
        payment.fees = response['fees']
        payment.currency = response['currency']
        payment.ip_address = response['ip_address']
        payment.log = response['log']
        payment.domain = response['domain']
        payment.gateway_response = response['gateway_response']
        payment.reference = response['reference']
        payment.customer = response['customer']
        payment.service = 'PAYSTACK'
        payment.authorization = {
            'channel': response['authorization']['channel'],
            'last4': response['authorization']['last4'],
            'exp_month': response['authorization']['exp_month'],
            'exp_year': response['authorization']['exp_year'],
            'card_type': response['authorization']['card_type'],
            'bank': response['authorization']['bank'],
            'country_code': response['authorization']['country_code'],
            'brand': response['authorization']['brand']
        }
        payment.status = Payment.SUCCESS if response['status'] == 'success' else Payment.PENDING
        payment.save()
    except Exception as error:
        print(error)
