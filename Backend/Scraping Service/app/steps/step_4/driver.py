import json
import requests
from app.config import settings
from app.steps.shared.base_step import Step
from app.utils.logger import err, info


class Driver(Step):
    """Class that manages the Model Training."""

    def __init__(self):
        super().__init__(step_name="Model Training")

    def run(self):
        """Start the model training process."""
        try:
            info("Starting model training process...")
            evaluation_metrics = requests.post(settings.MODEL_TRAINING_URL)
            info("Model training completed successfully.")
            print(json.dumps(evaluation_metrics, indent=2))

        except Exception as e:
            err(f"❌ Model training failed. Error: {e}")


Driver().run()
