import logging
import os
import subprocess

from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=12, minute=10)

def scheduled_job():
    subprocess.call('./scrape.sh', shell=True)
    logging.debug("Finished daily run")
    
sched.start()