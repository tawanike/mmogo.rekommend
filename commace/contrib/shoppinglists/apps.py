from django.apps import AppConfig


class ShoppinglistsConfig(AppConfig):
    name = 'commace.contrib.shoppinglists'

    def ready(self):
        import commace.contrib.shoppinglists.signals  # noqa