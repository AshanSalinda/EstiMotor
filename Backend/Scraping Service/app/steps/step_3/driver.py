from app.steps.shared.base_step import Step
from app.steps.step_3.cleaner import clean_vehicle_data
from app.db.repository.cleaned_vehicle_data_repository import cleaned_vehicles_data_repo
from app.db.repository.scraped_vehicle_data_repository import scraped_vehicles_data_repo


class Driver(Step):
    """Class that manages the scraping process."""

    def __init__(self):
        super().__init__(step_name="Data Cleaning")
        self.batch_size = 50  # Number of vehicles to process in each batch

    async def run(self):
        """Start the data cleaning process."""
        while True:
            # Fetch a paginated list of vehicle data to be cleaned
            vehicles = scraped_vehicles_data_repo.get_paginated(page_size=self.batch_size)

            if not vehicles:
                # Drop the collection after cleaning is done
                scraped_vehicles_data_repo.drop()
                break

            cleaned_vehicles = []
            processed_ids = []

            # Perform data cleaning on the fetched vehicles
            for vehicle in vehicles:
                vehicle_id = vehicle.pop('_id', None)
                if vehicle_id:
                    processed_ids.append(vehicle_id)
                cleaned_vehicle = clean_vehicle_data(vehicle)
                cleaned_vehicles.append(cleaned_vehicle)

            cleaned_vehicles_data_repo.save(cleaned_vehicles)  # Save the cleaned vehicle data
            scraped_vehicles_data_repo.delete_by_ids(processed_ids)  # Delete the original raw vehicle data
