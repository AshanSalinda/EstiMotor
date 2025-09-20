import pytz
from threading import Thread
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.steps.shared.steps_manager import stepsManager
from app.utils.logger import err, info


class Scheduler:
    def __init__(self):
        # Use Sri Lanka timezone
        self.timezone = pytz.timezone("Asia/Colombo")
        self.scheduler = BackgroundScheduler(timezone=self.timezone)
        self.job = None

    @staticmethod
    def _run_task():
        """Wrapper to run stepsManager in background thread safely."""
        if stepsManager.is_running:
            err("Scheduled task skipped: already running.")
            return

        info("Starting scheduled task...")
        Thread(target=stepsManager.start).start()

    def start(self):
        """Start the scheduler and schedule the monthly job."""
        if self.job is None:
            # Use CronTrigger for 1st day of every month at 00:00 SLST
            trigger = CronTrigger(day=1, hour=0, minute=0, timezone=self.timezone)
            self.job = self.scheduler.add_job(
                self._run_task,
                trigger=trigger,
                id="monthly_model_training_job",
                replace_existing=True
            )
            self.scheduler.start()
            info(f"Scheduler started with: {self.job.id} in {self.timezone}")


scheduler = Scheduler()
