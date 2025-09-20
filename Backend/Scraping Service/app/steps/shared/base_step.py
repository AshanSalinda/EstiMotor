from datetime import datetime

from app.utils.execution_report import ExecutionReport
from app.utils.logger import info
from app.steps.shared.step_execution_error import StepExecutionError


class Step:
    """Base class for all steps."""

    def __init__(self, **kwargs):
        # Indicates if the step is currently running
        self.is_running = kwargs.get('is_running', False)
        # Stores the start time of the step
        self.start_time = kwargs.get('start_time', 0)
        # Name of the step, defaults to the class name
        self.step_name = kwargs.get('step_name', self.__class__.__name__)
        # Holds the execution report for the step
        self.execution_report: ExecutionReport | None = None

    async def start(self, execution_report: ExecutionReport):
        """Starts the step execution."""
        # Prevents starting the step if it's already running
        if self.is_running:
            e = Exception(f"Step: '{self.step_name}' is already running.")
            raise StepExecutionError(e, '00:00:00')

        info(f"Starting Step: '{self.step_name}'...")
        self.is_running = True
        self.start_time = datetime.now()
        self.execution_report = execution_report

        try:
            # Run the step's main logic
            await self.run()
            info(f"Finished Step: '{self.step_name}'")
        except StepExecutionError as e:
            # Handles custom step execution errors
            raise e
        except Exception as e:
            # Handles generic errors and logs duration
            duration = str(datetime.now() - self.start_time).split('.')[0]
            raise StepExecutionError(e, duration)
        finally:
            # Ensures the running flag is reset
            self.is_running = False

    async def run(self):
        # Method to be implemented by subclasses
        raise NotImplementedError(f"{self.__class__.__name__} must implement run() method")
