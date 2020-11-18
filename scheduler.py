import logging
import os
import subprocess

from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

def calendar():
    subprocess.call('bash scrape.sh', shell=True)
    logging.debug("Finished daily run")

sched.add_job(calendar, 'cron', day_of_week='mon-fri', hour=15, minute=17)
    
sched.start()