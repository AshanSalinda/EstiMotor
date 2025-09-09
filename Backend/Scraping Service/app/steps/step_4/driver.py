import requests
from twisted.internet import threads
from app.config import settings
from app.steps.shared.base_step import Step
from app.steps.step_4.progress_manager import ProgressManager
from app.utils.logger import info


class Driver(Step):
    def __init__(self):
        super().__init__(step_name="Model Training")

    async def run(self):
        progress_manager = ProgressManager()

        try:
            info("Starting model training process...")
            progress_manager.start_progress_emitter()

            # Run blocking request in a thread
            response = await threads.deferToThread(
                requests.post,
                settings.MODAL_TRAINING_API
            )

            progress_manager.stop_progress_emitter()
            progress_manager.complete(response)

        except Exception as e:
            progress_manager.stop_progress_emitter()
            raise e  # propagate to StepsManager
