from twisted.internet import reactor
from twisted.internet.defer import ensureDeferred
from app.utils.logger import info, warn, err
from app.steps.step_1.driver import ads_collecting
from app.steps.step_2.driver import details_extraction


class StepsManager:
    def __init__(self):
        self.steps = [ads_collecting, details_extraction]
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


steps_manager = StepsManager()
