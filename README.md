# EstiMotor | Used Vehicle Price Prediction System 🚗💨

EstiMotor is a comprehensive system designed to bring transparency and fairness to the used vehicle market in Sri Lanka. By leveraging a microservices architecture and machine learning, it provides accurate, data-driven price predictions for second-hand vehicles, helping both buyers and sellers make informed decisions. 🤝

## Features 🌟

  - **AI-Powered Vehicle Valuation** 🤖: Get instant and accurate price predictions for used vehicles based on make, model, year, mileage, and other features.
  - **Web Scraping & Data Aggregation** 🕸️: Automatically collects vehicle data from multiple popular Sri Lankan automobile listing websites like Ikman.lk, Patpat.lk, and Riyasewana.com.
  - **Automated Data Processing Pipeline** 🔄: A multi-step process that includes data extraction, cleaning, normalization, imputation of missing values, and canonicalization of model names.
  - **Admin Dashboard** 👨‍💻: A secure area for administrators to manage the system, monitor the data processing pipeline, and trigger model retraining.
  - **User & Team Management** 👥: Super admins can create, update, and delete other admin accounts and manage access levels.
  - **Real-Time Progress Tracking** 📊: A WebSocket-based interface allows admins to monitor the status of scraping and model training in real-time.
  - **RESTful API** 🔗: A central Coordinator Service manages authentication and routes requests to the appropriate backend microservices.
  - **Progressive Web App (PWA)** 📱: The frontend is installable on both desktop and mobile devices for a native-app-like experience.

## System Architecture 🏗️

The project is built on a microservices architecture, with each service handling a specific business capability.

  - **Frontend** 🎨: A responsive web application built with React and Vite that serves as the user interface for both public users and administrators.
  - **Coordinator Service** 🚦: A Node.js (Express) application that acts as the central API gateway. It handles user authentication, admin management, and proxies requests to the other backend services.
  - **Scraping Service** 🕷️: A Python application built with Scrapy and FastAPI. It manages the multi-step pipeline for collecting, cleaning, and preparing vehicle data before triggering the ML service to retrain the model.
  - **ML Service** 🧠: A Python API built with FastAPI that serves the trained machine learning model for price prediction and handles model retraining requests.

All services are designed to be containerized and deployed independently.

## Tech Stack 💻

The project utilizes a modern and robust tech stack for both frontend and backend development.

#### **Frontend**

  - **Framework**: React, Vite
  - **Styling**: Tailwind CSS, PostCSS
  - **UI Components**: Material-UI (MUI)
  - **API Communication**: Axios
  - **PWA**: Vite PWA plugin

#### **Backend**

  - **Coordinator Service**: Node.js, Express.js, Mongoose, JWT
  - **Scraping Service**: Python, FastAPI, Scrapy, Twisted
  - **ML Service**: Python, FastAPI, Scikit-learn, Pandas, Joblib
  - **Database**: MongoDB

## Getting Started 🚀

To get the full EstiMotor system running locally, you will need to set up each service.

### Prerequisites

  - Node.js and npm
  - Python and pip
  - MongoDB instance

### Installation & Setup

1.  **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd EstiMotor
    ```

2.  **Configure Environment Variables:**
    Each service (`Coordinator Service`, `Scraping Service`, `ML Service`) requires its own `.env` file. Refer to the individual `README.md` files in each service's directory for the required variables. At a minimum, you will need to configure:

      - `MONGO_URI` and `DATABASE_NAME`
      - `JWT_SECRET` for the Coordinator Service
      - URLs for inter-service communication (e.g., `SCRAPING_SERVICE_URL`, `ML_SERVICE_URL`)
      - `EMAIL_SENDER_ADDRESS` and `EMAIL_SENDER_PASSWORD` for the Scraping Service to send completion reports.

3.  **Install Dependencies and Run Each Service:**

      - **Coordinator Service:**

        ```bash
        cd Backend/Coordinator\ Service
        npm install
        npm start
        ```

      - **ML Service:**

        ```bash
        cd Backend/ML\ Service
        pip install -r requirements.txt
        uvicorn app.main:app --reload
        ```

      - **Scraping Service:**

        ```bash
        cd Backend/Scraping\ Service
        pip install -r requirements.txt
        uvicorn app.main:app --reload
        ```

      - **Frontend:**

        ```bash
        cd Frontend
        npm install
        npm run dev
        ```

Once all services are running, the application will be accessible at the URL provided by the Vite development server (usually `http://localhost:3000`).

## Project Structure 📁

The repository is organized as a monorepo with separate directories for the frontend and each backend microservice.

```
├── Backend/
│   ├── Coordinator Service/    # Node.js API Gateway & Auth
│   ├── ML Service/             # Python ML Model Serving & Training
│   └── Scraping Service/       # Python Data Scraping & Processing Pipeline
├── Frontend/                   # React (Vite) User Interface
└── README.md                   # This file
```

For more detailed information about a specific service, please refer to the `README.md` file within its directory.
