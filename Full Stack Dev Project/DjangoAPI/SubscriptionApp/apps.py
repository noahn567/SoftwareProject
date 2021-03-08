from django.apps import AppConfig


class SubscriptionappConfig(AppConfig):
    name = 'SubscriptionApp'

    # Start Scheduler when app is ready
    def ready(self):
        from .SubscriptionScheduler import Scheduler
        Scheduler.start()