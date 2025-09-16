import json

from datetime import datetime
from twisted.internet import reactor
from twisted.internet.defer import DeferredLock
from app.utils.message_queue import MessageQueue


class ProgressManager:
    """
    Manages progress tracking for scraping tasks.

    Tracks the number of requests, responses, successes, failures,
    and calculates success rate and elapsed time. Can periodically
    send stats via MessageQueue.
    """

    def __init__(self, target: int = 0, job_interval: int = 1):
        """
        Initialize the ProgressManager with counters set to zero
        and record the start time.
        """
        self.start_time = datetime.now()
        self.target = target
        self.request_count = 0
        self.response_count = 0
        self.success_count = 0
        self.failed_requests = []

        self.is_progress_emitting = False
        self.job_interval = job_interval

        # lock for thread-safety when multiple spiders update at the same time
        self.lock = DeferredLock()


    def start_progress_emitter(self):
        """Start a repeating scheduled task to send stats every second."""
        if not self.is_progress_emitting:
            self.is_progress_emitting = True
            reactor.callLater(self.job_interval, self._emit_progress)


    def stop_progress_emitter(self):
        """Stops emitting progress updates."""
        self.is_progress_emitting = False


    def _emit_progress(self):
        """Periodically Sends the stats to MessageQueue and schedules itself again if still active."""
        if self.is_progress_emitting:
            stats = self.calculate_stats()
            MessageQueue.enqueue({'stats': {
                'Status': 'Running',
                **stats,
                'Failure count': len(self.failed_requests),
            }})

            # Schedule next call
            reactor.callLater(self.job_interval, self._emit_progress)


    def calculate_stats(self):
        """
        Calculate current statistics of the scraping process.

        Returns:
            dict: Contains elapsed time, success rate, total requests, and successes.
        """

        # Avoid errors if start time is None
        if not self.start_time:
            return None

        current_time = datetime.now()
        duration = str(current_time - self.start_time).split('.')[0]

        try:
            success_rate = str(int((self.success_count * 100) / self.request_count)) + '%'
        except ZeroDivisionError:
            success_rate = '0%'

        return {
            'Duration': duration,
            'Success Rate': success_rate,
            'Request Count': self.request_count,
            'Success Count': self.success_count
        }


    def add_request(self):
        """Increment request counter safely."""

        def _inc():
            self.request_count += 1

        return self.lock.run(_inc)


    def add_response(self, url: str, error: dict | None = None):
        """
        Increment response counter and track result safely.

        Args:
            url (str): URL of the processed request.
            error (dict | None): Optional error information if request failed.
        """

        def _update():
            if error:
                self.failed_requests.append(error)
            else:
                self.success_count += 1

            try:
                percentage = round((self.response_count * 100) / self.target, 2)
            except ZeroDivisionError:
                percentage = -1

            self.response_count += 1
            MessageQueue.enqueue({'progress': percentage, 'log': url})

        return self.lock.run(_update)


    def complete(self):
        """
        Finalize the progress tracking.

        Sends a "Completed" message via MessageQueue, resets counters,
        and prints final stats including failed requests.
        """
        stats = self.calculate_stats()

        try:
            percentage = round((self.response_count * 100) / self.target, 2)
        except ZeroDivisionError:
            percentage = 100

        MessageQueue.enqueue({
            'stats': {
                'Status': 'Completed',
                **stats,
                'Failure count': len(self.failed_requests),
            },
            'control': 'completed',
            'progress': percentage
        })

        print(json.dumps({
            **stats,
            'Failed Requests': self.failed_requests,
        }, indent=2))

        self.is_progress_emitting = False
        self.start_time = None
        self.target = 0
        self.request_count = 0
        self.response_count = 0
        self.success_count = 0
        self.failed_requests = []
