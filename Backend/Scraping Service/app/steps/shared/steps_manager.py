from datetime import datetime
from twisted.internet import reactor
from twisted.internet.defer import ensureDeferred

from app.utils.email_sender import send_training_completion_email
from app.utils.logger import info, err
from app.steps.step_1.driver import Driver as AdsCollecting
from app.steps.step_2.driver import Driver as DetailsExtraction
from app.steps.step_3.driver import Driver as DataCleaning
from app.steps.step_4.driver import Driver as ModelTraining
from app.utils.message_queue import MessageQueue
from app.steps.shared.step_execution_error import StepExecutionError


class StepsManager:
    def __init__(self):
        self.is_running = False
        self.current_step = 1
        self.steps = [
            AdsCollecting(),
            DetailsExtraction(),
            DataCleaning(),
            ModelTraining()
        ]


    def start(self):
        """Run steps inside the Twisted reactor thread."""

        def deferred_run():
            # Convert the async function to a twisted deferred
            d = ensureDeferred(self.run())
            d.addErrback(self.handle_global_error)
            return d

        if not reactor.running:
            reactor.callWhenRunning(deferred_run)
        else:
            reactor.callFromThread(deferred_run)


    async def run(self):
        info("Running all steps...")
        start_time = datetime.now()
        self.is_running = True
        errors = []

        try:
            for step in self.steps:
                step_errors = await step.start()
                if isinstance(step_errors, list):
                    errors.extend(step_errors)
                self.current_step += 1

            info("Finished all steps...")
            duration = str(datetime.now() - start_time).split('.')[0]
            send_training_completion_email(
                training_duration=duration,
                total_records=len(errors),
                mae=23.5,  # Placeholder value
                mape=12.3,  # Placeholder value
                r2_score=25.6,  # Placeholder value
                errors=errors,
            )

        except StepExecutionError as e:
            self.handle_step_error(e)
        except Exception as e:
            se = StepExecutionError(e, '00:00:00')
            self.handle_step_error(se)
        finally:
            self.is_running = False
            self.current_step = 1


    def handle_step_error(self, step_error: StepExecutionError):
        """Emit an error message to the queue."""
        step_no = self.current_step
        step_name = self.steps[step_no - 1].step_name if 0 < step_no <= len(self.steps) else "Unknown"
        err(f"Step: {step_no} [{step_name}] failed after {step_error.duration}")
        print(step_error.original_exception)

        MessageQueue.enqueue({
            'stats': {
                'Status': 'Failed',
                'Duration': step_error.duration,
            },
            'control': 'failed'
        })


    def handle_global_error(self, failure):
        """Handle any unexpected global errors."""
        err("Unexpected error in StepsManager")
        print(failure)

        MessageQueue.enqueue({
            'stats': {
                'Status': 'Failed',
                'Duration': '00:00:00',
            },
            'control': 'failed'
        })

        self.is_running = False
        self.current_step = 1


stepsManager = StepsManager()
