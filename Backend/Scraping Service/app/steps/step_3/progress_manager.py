import json
from datetime import datetime
from app.utils.logger import info, warn
from app.utils.message_queue import MessageQueue


class ProgressManager:
    """
    Manages progress tracking for scraping tasks.

    Tracks the number of requests, responses, successes, failures,
    and calculates success rate and elapsed time. Can periodically
    send stats via MessageQueue.
    """

    def __init__(self, total: int = 0):
        """
        Initialize the ProgressManager with counters set to zero
        and record the start time.
        """
        self.start_time = datetime.now()
        self.total_count = total * 2 # Normalization + Imputation
        self.processed_so_far = 0
        self.dropped_count = 0
        self.modified_count = 0
        self.logs = []

    def log(self, log: dict | str) -> None:
        self.logs.append(log)

        if isinstance(log, dict):
            warn(f"{log['action']} {log['message']} for {log['url']}")
            # MessageQueue.enqueue({'log': log})
            MessageQueue.enqueue({'log': f"{log['action']}: {log['message']} for {log['url']}"})
        else:
            info(log)
            MessageQueue.enqueue({'log': log})

    def add_modified(self, count: int = 1) -> None:
        self.modified_count += count

    def add_dropped(self, count: int = 1) -> None:
        self.dropped_count += count

    def emit_progress(self, processed_count: int = 0, completed: bool = False):
        """Emit progress update."""
        self.processed_so_far += processed_count
        progress = round((self.processed_so_far / self.total_count) * 100, 2) if self.total_count > 0 else -1
        time_taken = str(datetime.now() - self.start_time).split('.')[0] if self.start_time else 0

        stats = {
            'Status': 'Running' if not completed else 'Completed',
            'Duration': time_taken,
            'Total Count': self.total_count,
            'Modified Count': self.modified_count,
            'Dropped Count': self.dropped_count,
        }

        if completed:
            MessageQueue.enqueue({
                'stats': stats,
                'progress': progress,
                'control': 'completed',
            })

            print(json.dumps(stats, indent=2))

        else:
            MessageQueue.enqueue({
                'stats': stats,
                'progress': progress,
            })
