class StepExecutionError(Exception):
    """
    Custom exception for errors occurring during a step.

    Attributes:
        original_exception (Exception): The actual error that was raised.
        duration (str): The duration of the step until failure.
    """

    def __init__(self, original_exception: Exception, duration: str):
        self.original_exception = original_exception
        self.duration = duration
        super().__init__(f"Step failed after {duration}: {original_exception}")

    def __str__(self):
        return f"[StepExecutionError] {self.original_exception} (Duration: {self.duration})"

    def __repr__(self):
        return f"<StepExecutionError original_exception={self.original_exception!r} duration={self.duration!r}>"
