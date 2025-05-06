from twisted.internet import reactor
from twisted.internet.defer import ensureDeferred

from app.utils.logger import info
from app.steps.step_1.driver import Driver as AdsCollecting
from app.steps.step_2.driver import Driver as DetailsExtraction
from app.steps.step_3.driver import Driver as DataCleaning


class StepsManager:
    def __init__(self):
        self.steps = [AdsCollecting(), DetailsExtraction(), DataCleaning()]
        self.current_step = 0

    async def run(self):
        info("Running all steps...")

        for index, step in enumerate(self.steps):
            await step.start()
            self.current_step = (index + 1) % len(self.steps)

        info("Finished all steps...")

    def start(self):
        """Run steps inside the Twisted reactor thread."""

        def deferred_run():
            # Convert the async function to a twisted deferred
            return ensureDeferred(self.run())

        if not reactor.running:
            reactor.callWhenRunning(deferred_run)
        else:
            reactor.callFromThread(deferred_run)
