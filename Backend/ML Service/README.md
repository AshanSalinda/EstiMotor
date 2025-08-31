# EstiMotor ML Service

This project is the Machine Learning (ML) Service for the EstiMotor platform. It provides vehicle price estimation and related ML-powered features via a RESTful API.

## Features
- Vehicle price prediction using a trained ML model
- REST API endpoints for prediction and data management
- Modular architecture with clear separation of concerns
- Logging and configuration utilities

## Project Structure
```
ML Service/
├── requirements.txt           # Python dependencies
├── app/
│   ├── main.py                # Application entry point
│   ├── api/
│   │   └── routes.py          # API route definitions
│   ├── db/
│   │   ├── database.py        # Database connection logic
│   │   └── vehicle_data_repository.py # Data access layer
│   ├── schema/
│   │   └── schema.py          # Pydantic models/schemas
│   ├── service/
│   │   ├── model.py           # ML model loading and prediction
│   │   └── vehicle_price_model.pkl # Trained ML model
│   └── utils/
│       └── logger.py          # Logging utility
└── .env                       # Environment variables
```

## Environment Variables
Create a `.env` file in the project root with the following variables:
```env
MONGO_URI=""
DATABASE_NAME=""
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

## API Endpoints
- `POST /predict` — Predict vehicle price 
- `POST /train` — Fetch the dataset and train the ML model
- Additional endpoints for data management may be available
- API documentation is available at `/docs` when the service is running
