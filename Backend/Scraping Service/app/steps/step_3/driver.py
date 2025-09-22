from twisted.internet.defer import ensureDeferred
from twisted.internet.threads import deferToThread

from app.config import settings
from app.db.repository.cleaned_vehicle_data_repository import cleaned_vehicles_data_repo
from app.db.repository.imputation_stats_repository import imputation_stats_repo
from app.db.repository.make_model_mapping_repository import make_model_mapping_repo
from app.db.repository.scraped_vehicle_data_repository import scraped_vehicles_data_repo
from app.db.repository.normalized_vehicle_data_repository import normalized_vehicle_data_repo
from app.steps.shared.base_step import Step
from app.steps.step_3.canonicalize_models import build_canonical_map
from app.steps.step_3.progress_manager import ProgressManager
from app.steps.step_3.impute import impute_missing_fields
from app.steps.step_3.normalizer import Normalizer


class Driver(Step):
    """Class that manages the cleaning process."""

    def __init__(self):
        super().__init__(step_name="Data Cleaning")
        self.batch_size: int = settings.PROCESSING_BATCH_SIZE  # Number of vehicles to process in each batch
        self.progress_manager: ProgressManager | None = None
        self.normalizer: Normalizer | None = None
        self.model_canonical_map: dict = {}

    async def run(self):
        """Start the data cleaning process."""

        try:
            total_count = scraped_vehicles_data_repo.get_total_ad_count()
            self.progress_manager = ProgressManager(total_count)
            self.normalizer = Normalizer(self.progress_manager)

            # Offload blocking methods
            await ensureDeferred(deferToThread(self.normalize_vehicles))
            await ensureDeferred(deferToThread(self.generate_imputation_stats))
            await ensureDeferred(deferToThread(self.generate_model_canonical_map))
            await ensureDeferred(deferToThread(self.finalize_cleaned_vehicles))
            await ensureDeferred(deferToThread(self.generate_make_model_category_mapping))

            self.progress_manager.complete()
            self.execution_report.make_model_map = self.model_canonical_map
            self.execution_report.dataset_size = total_count - self.progress_manager.dropped_count or 0

        except Exception as e:
            raise e  # propagate to StepsManager


    @staticmethod
    def generate_imputation_stats():
        """Generate the imputation stats."""
        imputation_stats_repo.drop()
        imputation_stats = normalized_vehicle_data_repo.get_stats()
        imputation_stats_repo.save(imputation_stats)


    def generate_model_canonical_map(self):
        """Canonicalize vehicle models per make."""
        # Get make-wise models with frequencies
        make_model_freqs = normalized_vehicle_data_repo.get_make_model_frequencies()
        self.progress_manager.set_total_makes(len(make_model_freqs.keys()))

        # Build canonical map per make
        for make, models_freq_list in make_model_freqs.items():
            self.progress_manager.add_processed(1, "canonicalize")
            self.progress_manager.log(f"Identifying canonical models for make: {make}")
            # extract model names and frequency dict
            model_list = [entry['model'] for entry in models_freq_list]
            freq_dict = {entry['model']: entry['frequency'] for entry in models_freq_list}

            # build canonical clusters for this make
            clusters = build_canonical_map(model_list, freqs=freq_dict)

            # store mapping: variant -> canonical
            self.model_canonical_map[make] = {}
            for cluster in clusters:
                canonical = cluster["canonical"]
                for variant in cluster["variants"]:
                    self.model_canonical_map[make][variant] = canonical

            # log summary
            print(f"{make}: {len(model_list)} variants mapped to {len(clusters)} canonical model(s)")


    def normalize_vehicles(self):
        """Normalize raw vehicle data."""
        normalized_vehicle_data_repo.drop()

        while True:
            vehicles = scraped_vehicles_data_repo.get_paginated(page_size=self.batch_size)

            if not vehicles:
                # Drop the collection after cleaning is done
                scraped_vehicles_data_repo.drop()
                break

            normalized_vehicles = []
            processed_ids = []

            for vehicle in vehicles:
                vehicle_id = vehicle.pop('_id', None)
                if vehicle_id:
                    processed_ids.append(vehicle_id)
                normalized_vehicle = self.normalizer.normalize_vehicle_data(vehicle)
                normalized_vehicles.append(normalized_vehicle)

            self.progress_manager.add_processed(len(vehicles), "normalize")
            normalized_vehicle_data_repo.save(normalized_vehicles)  # Save the standardized vehicle data
            scraped_vehicles_data_repo.delete_by_ids(processed_ids)  # Delete the original raw vehicle data

    def finalize_cleaned_vehicles(self):
        """Canonicalize models, impute missing fields, and finalize cleaned vehicles."""
        imputation_stats = imputation_stats_repo.get_stats()
        cleaned_vehicles_data_repo.drop()

        while True:
            vehicles = normalized_vehicle_data_repo.get_paginated(page_size=self.batch_size)

            if not vehicles:
                # Drop the collection after cleaning is done
                normalized_vehicle_data_repo.drop()
                imputation_stats_repo.drop()
                break

            # Canonicalize model names
            for vehicle in vehicles:
                make = vehicle.get("make")
                model = vehicle.get("model")
                if make in self.model_canonical_map and model in self.model_canonical_map[make]:
                    vehicle["model"] = self.model_canonical_map[make][model]

            # Missing fields Imputation
            imputed_vehicles = impute_missing_fields(vehicles, imputation_stats, self.progress_manager)

            # Final cleanup: remove or fill null/empty fields
            cleaned_vehicles = self.normalizer.null_cleanup(imputed_vehicles)

            processed_ids = [vehicle.pop('_id') for vehicle in vehicles if '_id' in vehicle]

            self.progress_manager.add_processed(len(vehicles), "finalize")
            cleaned_vehicles_data_repo.save(cleaned_vehicles)  # Save the cleaned vehicle data
            normalized_vehicle_data_repo.delete_by_ids(processed_ids)  # Delete the original raw vehicle data


    @staticmethod
    def generate_make_model_category_mapping():
        """Generate the make-model-category mapping."""
        mappings = cleaned_vehicles_data_repo.get_make_model_category_map()
        make_model_mapping_repo.drop()
        make_model_mapping_repo.save(mappings)
