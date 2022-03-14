from django.apps import AppConfig


class OrdersConfig(AppConfig):
    name = 'commace.contrib.orders'

    def ready(self):
        import commace.contrib.orders.signals  # noqa
