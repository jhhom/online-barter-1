from django.apps import AppConfig


class MarketConfig(AppConfig):
    name = 'market'
    
    def ready(self):
        import market.signals