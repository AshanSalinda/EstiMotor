# Scraping Service

A modular Python backend service for scraping, processing, and managing vehicle data for EstiMotor, a used vehicle price prediction system. This service collects vehicle details from configured online public vehicle listing websites, processes, cleans, and prepares the dataset, and finally triggers the ML service to retrain with newly collected data.

## Features
- Multi-step scraping pipeline for vehicle data
- Modular architecture (steps, shared utilities, repositories)
- REST API and WebSocket support
- Data cleaning, normalization, and imputation
- Progress tracking and logging
- Configurable via environment and settings files

## Environment Variables
Create a `.env` file in the project root with the following variables:
```env
MONGO_URI=""
DATABASE_NAME=""
MODAL_TRAINING_URL=""
SCRAPING_BATCH_SIZE=100
PROCESSING_BATCH_SIZE=1000
EMAIL_SENDER_ADDRESS=""
EMAIL_SENDER_PASSWORD=""
```
- `MONGO_URI`: MongoDB connection string for storing and retrieving vehicle data.
- `DATABASE_NAME`: Name of the MongoDB database.
- `MODAL_TRAINING_URL`: URL of the ML service endpoint to trigger model retraining.
- `SCRAPING_BATCH_SIZE`: Number of vehicle ads to scrape per batch.
- `PROCESSING_BATCH_SIZE`: Number of records to process per batch during cleaning and preparation.
- `EMAIL_SENDER_ADDRESS`: Email address used for sending notifications.
- `EMAIL_SENDER_PASSWORD`: Password for the email sender address.

## Configuration
Configuration is managed through several files and modules:
- `app/config.py`: Main configuration logic, loads environment variables and service settings.
- `data/site_data.py`: Contains site-specific configurations and settings for scraping.
- `data/parameters.py`: Defines scraping and processing parameters for different sites and steps.
- `steps/step_*/settings.py`: Step-specific settings for each pipeline stage.

Edit these files to customize scraping sources, parameters, and service behavior for your deployment.

## Folder Structure
```
Scraping Service/
├── app/                # Main application logic
│   ├── api/            # API routes and WebSocket handlers
│   ├── data/           # Data models, site configurations, and parameters
│   ├── db/             # Database and repository modules
│   ├── steps/          # Stepwise scraping pipeline
│   │   ├── shared/     # Shared step logic and middleware
│   │   ├── step_1/     # Step 1: Initial scraping
│   │   ├── step_2/     # Step 2: Data extraction
│   │   ├── step_3/     # Step 3: Imputation & normalization
│   │   └── step_4/     # Step 4: Model retraining trigger
│   ├── utils/          # Logging, message queue, progress manager
│   ├── config.py       # Configuration settings
│   └── main.py         # Entry point
├── requirements.txt    # Python dependencies
├── readme.md           # Project documentation
└── .env                # Environment variables
```

## Setup
1. **Clone the repository**
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the service**
   ```bash
   uvicorn app.main:app --port <port>
   ```

## API Usage
- REST endpoints are defined in `app/api/routes.py`
- WebSocket support in `app/api/websocket.py`

## Data Pipeline
- **Step 1:** Scrape ad links and initial data
- **Step 2:** Extract detailed vehicle data
- **Step 3:** Normalize data, impute missing values
- **Step 4:** Trigger ML service for retraining

