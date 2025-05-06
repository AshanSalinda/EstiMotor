from app.utils.logger import info


class Step:
    """Base class for all steps."""

    def __init__(self, **kwargs):
        self.is_running = kwargs.get('is_running', False)
        self.step_name = kwargs.get('step_name', self.__class__.__name__)

    async def start(self):
        if self.is_running:
            raise Exception(f"Step: {self.step_name} is already running.")

        info(f"Starting Step: {self.step_name}...")
        self.is_running = True
        await self.run()
        self.is_running = False
        info(f"Finished Step: {self.step_name}...")

    def run(self):
        raise NotImplementedError(f"{self.__class__.__name__} must implement run() method")
