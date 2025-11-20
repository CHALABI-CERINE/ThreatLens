"""from apscheduler.schedulers.background import BackgroundScheduler
from .collectors_nvd import fetch_nvd, store_alerts
from .db import init_db

sched = BackgroundScheduler()


def scheduled_fetch():
    print('Running scheduled fetch from NVD...')
    items = fetch_nvd(max_results=50)
    added = store_alerts(items)
    print(f'Fetched {len(items)} and added {added} new alerts')


def start_scheduler():
    init_db()
    sched.add_job(scheduled_fetch, 'interval', minutes=60, id='nvd_fetch_job', replace_existing=True)
    sched.start()
    print('Scheduler started')

if __name__ == '__main__':
    start_scheduler()
    import time
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        sched.shutdown()
"""