from apscheduler.schedulers.background import BackgroundScheduler
from SubscriptionApp.views import allSubscriptionsSendUpdate

# Create and Start Scheduler to send SMS periodicly to all Subscriptions
def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(allSubscriptionsSendUpdate,"cron",hour="9-17", day_of_week='mon-fri',id="SubscriptionUpdater_001",replace_existing=True)
    scheduler.start()