from twisted.internet import reactor
from twisted.internet.defer import ensureDeferred

from app.utils.logger import info
from app.steps.step_1.driver import Driver as AdsCollecting
from app.steps.step_2.driver import Driver as DetailsExtraction
from app.steps.step_3.driver import Driver as DataCleaning
from app.steps.step_4.driver import Driver as ModelTraining


class StepsManager:
    def __init__(self):
        self.is_running = False
        self.steps = [
            AdsCollecting(),
            DetailsExtraction(),
            DataCleaning(),
            ModelTraining()
        ]


    async def run(self):
        info("Running all steps...")
        self.is_running = True

        try:
            for step in self.steps:
                await step.start()
            info("Finished all steps...")
        except Exception as e:
            info(f"Error occurred")
            raise e
        finally:
            self.is_running = False


    def start(self):
        """Run steps inside the Twisted reactor thread."""

        def deferred_run():
            # Convert the async function to a twisted deferred
            return ensureDeferred(self.run())

        if not reactor.running:
            reactor.callWhenRunning(deferred_run)
        else:
            reactor.callFromThread(deferred_run)


stepsManager = StepsManager()
