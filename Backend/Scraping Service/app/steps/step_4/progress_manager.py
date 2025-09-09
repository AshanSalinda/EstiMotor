import json
from datetime import datetime
from twisted.internet import reactor
from app.utils.logger import info
from app.utils.message_queue import MessageQueue


class ProgressManager:
    """Manages progress updates and completion status for the step 4."""

    def __init__(self, job_interval: int = 1):
        """Initializes the ProgressManager with a job interval."""
        self.job_interval = job_interval  # seconds
        self.start_time = None
        self.is_progress_emitting = False


    def start_progress_emitter(self):
        """Starts emitting progress updates at regular intervals."""
        if not self.is_progress_emitting:
            self.is_progress_emitting = True
            self.start_time = datetime.now()
            MessageQueue.set_enqueue_access(True)
            reactor.callLater(self.job_interval, self._emit_progress)


    def stop_progress_emitter(self):
        """Stops emitting progress updates."""
        self.is_progress_emitting = False


    def _get_duration(self):
        """Returns the duration since the progress emitter started."""
        if self.start_time:
            return str(datetime.now() - self.start_time).split('.')[0]
        return "00:00:00"


    def _emit_progress(self):
        """Emits a progress update message to the queue."""
        if self.is_progress_emitting:
            MessageQueue.enqueue({
                'stats': {
                    'Status': 'Running',
                    'Duration': self._get_duration(),
                },
                'progress': -1
            })
            reactor.callLater(self.job_interval, self._emit_progress)


    def complete(self, response):
        """Handles completion of the process and emits final stats."""
        info("Model training completed successfully.")

        result = response.json()
        metrics = result.get("evaluation_metrics", {})
        stats = {
            'Status': 'Completed',
            'Duration': self._get_duration(),
            'MAE': metrics.get("MAE", "N/A"),
            'MAPE': metrics.get("MAPE", "N/A"),
            'R2': metrics.get("R2", "N/A"),
        }

        print(json.dumps(stats, indent=2))

        MessageQueue.enqueue({
            'stats': stats,
            'control': 'completed'
        })
