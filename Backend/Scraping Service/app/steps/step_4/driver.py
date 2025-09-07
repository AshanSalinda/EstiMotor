import json

import requests
from datetime import datetime
from twisted.internet import reactor, threads
from app.config import settings
from app.steps.shared.base_step import Step
from app.utils.logger import err, info
from app.utils.message_queue import MessageQueue


class Driver(Step):
    def __init__(self):
        super().__init__(step_name="Model Training")
        self.start_time = None
        self.is_progress_emitting = False

    async def run(self):
        info("Starting model training process...")
        self.start_time = datetime.now()
        self.start_progress()

        # Run blocking request in a thread
        d = threads.deferToThread(requests.post, settings.MODAL_TRAINING_API)
        d.addCallback(self.on_success)
        d.addErrback(self.on_failure)

    def on_success(self, response):
        self.stop_progress()
        info("Model training completed successfully.")

        result = response.json()
        metrics = result.get("evaluation_metrics", {})
        stats = {
            'Status': 'Completed',
            'Duration': str(datetime.now() - self.start_time).split('.')[0],
            'MAE': metrics.get("MAE", "N/A"),
            'MAPE': metrics.get("MAPE", "N/A"),
            'R2': metrics.get("R2", "N/A"),
        }

        print(json.dumps(stats, indent=2))

        MessageQueue.enqueue({
            'stats': stats,
            'control': 'completed'
        })

    def on_failure(self, failure):
        self.stop_progress()
        err(f"❌ Model training failed. Error: {failure}")

    def start_progress(self):
        MessageQueue.set_enqueue_access(True)
        if not self.is_progress_emitting:
            self.is_progress_emitting = True
            self.emit_progress_task()

    def stop_progress(self):
        self.is_progress_emitting = False

    def emit_progress_task(self):
        if self.is_progress_emitting:
            MessageQueue.enqueue({
                'stats': {
                    'Status': 'Running',
                    'Duration': str(datetime.now() - self.start_time).split('.')[0] if self.start_time else "0",
                },
                'progress': -1
            })
            reactor.callLater(1, self.emit_progress_task)
