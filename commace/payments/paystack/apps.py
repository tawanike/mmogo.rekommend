from django.apps import AppConfig


class PaystackConfig(AppConfig):
    name = 'commace.payments.paystack'

    def ready(self):
        import commace.payments.paystack.signals  # noqa