import json
from datetime import datetime
from typing import Literal
from twisted.internet import reactor
from app.utils.logger import info, warn
from app.utils.message_queue import MessageQueue


class ProgressManager:
    """Manages progress updates and completion status for step 3."""

    def __init__(self, total_ads: int = 0, job_interval: int = 1):
        """
        Initialize the ProgressManager with counters set to zero,
        record the start time, and start the scheduled emitting task.
        """
        self.total_ads = total_ads
        self.total_makes = 0
        self.job_interval = job_interval  # seconds
        self.start_time = datetime.now()
        self.percentage = 0
        self.dropped_count = 0
        self.modified_count = 0
        self.logs = []

        # Start emitting progress updates
        self.is_progress_emitting = True
        reactor.callLater(self.job_interval, self._emit_progress)

    def _emit_progress(self):
        """Emits a progress update message to the queue."""
        if self.is_progress_emitting:
            MessageQueue.enqueue(self._get_payload())
            reactor.callLater(self.job_interval, self._emit_progress)

    def _get_payload(self, is_completed: bool = False) -> dict:
        """Construct the payload with current stats and logs."""
        duration = str(datetime.now() - self.start_time).split('.')[0] if self.start_time is not None else "00:00:00"
        logs = self.logs.copy()
        self.logs = []

        stats = {
            'Duration': duration,
            'Total Ads': self.total_ads,
            'Modified Count': self.modified_count,
            'Dropped Count': self.dropped_count,
        }

        if is_completed:
            stats['Status'] = 'Completed'
            stats['Dataset Size'] = stats['Total Ads'] - stats['Dropped Count'] or 0
            return {
                'stats': stats,
                'log': logs,
                'progress': 100,
                'control': 'completed',
            }

        stats['Status'] = 'Running'
        return {
            'stats': stats,
            'log': logs,
            'progress': round(self.percentage, 2) if self.percentage > 0 else -1
        }

    def log(self, log: dict | str) -> None:
        """Log a message and store it for sending."""
        if isinstance(log, dict):
            warn(f"{log['action']} {log['message']} for {log['url']}")
            self.logs.append(f"{log['action']}: {log['message']} for {log['url']}")
        else:
            info(log)
            self.logs.append(log)

    def set_total_makes(self, count: int) -> None:
        """Set the total number of unique makes."""
        self.total_makes = count

    def add_modified(self, count: int = 1) -> None:
        """Increment the count of modified items."""
        self.modified_count += count

    def add_dropped(self, count: int = 1) -> None:
        """Increment the count of dropped items."""
        self.dropped_count += count

    def add_processed(self, count: int, stage: Literal["normalize", "canonicalize", "finalize"]) -> None:
        """Update the progress percentage based on the stage and count of processed items."""
        try:
            if stage == "canonicalize":
                # 20% for canonicalization
                self.percentage += (count / self.total_makes) * 20
            else:
                # 40% for normalization and finalization each
                self.percentage += (count / self.total_ads) * 40
        except ZeroDivisionError:
            pass

    def complete(self) -> None:
        """
        Mark the process as complete, stop emitting updates,
        and send a final payload with summary statistics.
        """
        self.is_progress_emitting = False
        payload = self._get_payload(is_completed=True)
        print(json.dumps(payload.get('stats', {}), indent=2))
        MessageQueue.enqueue(payload)
