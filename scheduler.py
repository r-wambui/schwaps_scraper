import logging
import os
import subprocess

from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

def calendar():
    subprocess.call('./scrape.sh', shell=True)
    logging.debug("Finished daily run")

sched.add_job(calendar, 'cron', day_of_week='mon-fri', hour=12, minute=55)
    
sched.start()