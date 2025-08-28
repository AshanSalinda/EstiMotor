from app.db.repository.cleaned_vehicle_data_repository import cleaned_vehicles_data_repo
from app.db.repository.imputation_stats_repository import imputation_stats_repo
from app.db.repository.scraped_vehicle_data_repository import scraped_vehicles_data_repo as sp
from app.db.repository.scraped_vehicle_data_repository1 import scraped_vehicles_data_repo
from app.db.repository.standardized_vehicle_data_repository import standardized_vehicle_data_repo
from app.steps.shared.base_step import Step
from app.steps.step_3.impute import impute_missing_fields
from app.steps.step_3.standardize import standardize_vehicle_data, final_cleanup


class Driver(Step):
    """Class that manages the cleaning process."""

    def __init__(self):
        super().__init__(step_name="Data Cleaning")
        self.batch_size = 100  # Number of vehicles to process in each batch

    async def run(self):
        """Start the data cleaning process."""

        scraped_vehicles_data_repo.drop()
        vehicles = sp.get_all()
        scraped_vehicles_data_repo.save(vehicles)

        self.standardize_vehicles()
        self.generate_imputation_stats()
        self.impute_vehicles()

    @staticmethod
    def generate_imputation_stats():
        """Generate the imputation stats."""
        imputation_stats = standardized_vehicle_data_repo.get_stats()
        imputation_stats_repo.save(imputation_stats)

    def standardize_vehicles(self):
        while True:
            vehicles = scraped_vehicles_data_repo.get_paginated(page_size=self.batch_size)

            if not vehicles:
                # Drop the collection after cleaning is done
                scraped_vehicles_data_repo.drop()
                break

            standardized_vehicles = []
            processed_ids = []

            for vehicle in vehicles:
                vehicle_id = vehicle.pop('_id', None)
                if vehicle_id:
                    processed_ids.append(vehicle_id)
                standardized_vehicle = standardize_vehicle_data(vehicle)
                standardized_vehicles.append(standardized_vehicle)

            standardized_vehicle_data_repo.save(standardized_vehicles)  # Save the standardized vehicle data
            scraped_vehicles_data_repo.delete_by_ids(processed_ids)  # Delete the original raw vehicle data


    def impute_vehicles(self):
        imputation_stats = imputation_stats_repo.get_stats()

        while True:
            vehicles = standardized_vehicle_data_repo.get_paginated(page_size=self.batch_size)

            if not vehicles:
                # Drop the collection after cleaning is done
                standardized_vehicle_data_repo.drop()
                break

            # Missing fields Imputation
            imputed_vehicles = impute_missing_fields(vehicles, imputation_stats)
            cleaned_vehicles = final_cleanup(imputed_vehicles)

            processed_ids = [vehicle.pop('_id') for vehicle in vehicles if '_id' in vehicle]

            cleaned_vehicles_data_repo.save(cleaned_vehicles)  # Save the cleaned vehicle data
            standardized_vehicle_data_repo.delete_by_ids(processed_ids)  # Delete the original raw vehicle data


