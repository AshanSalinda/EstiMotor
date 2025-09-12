# EstiMotor Coordinator Service

## Overview

The Coordinator Service is a core backend component of the EstiMotor project. It is responsible for service routing, authentication, and admin management. This service acts as a gateway, coordinating requests between various microservices such as machine learning, scraping, and websocket proxies.

## Features

- **Service Routing:** Directs requests to appropriate microservices (ML, scraping, websocket).
- **Authentication:** Handles user authentication and session management.
- **Admin Management:** Provides endpoints for admin operations.
- **Proxy Integration:** Communicates with ML, scraping, and websocket services via dedicated proxies.

## Directory Structure

```
Coordinator Service/
├── package.json
└── src/
    ├── index.js                # Entry point
    ├── config/
    │   └── db.js               # Database configuration
    ├── controller/
    │   └── admin.js            # Admin controller logic
    ├── middleware/
    │   └── auth.js             # Authentication middleware
    ├── models/
    │   └── Admin.js            # Admin data model
    ├── proxies/
    │   ├── mlProxy.js          # ML service proxy
    │   ├── scrapingProxy.js    # Scraping service proxy
    │   └── wsProxy.js          # Websocket service proxy
    ├── routes/
    │   └── admin.js            # Admin routes
    └── utils/
        ├── hash.js             # Password hashing utilities
        └── setCookies.js       # Cookie utilities
```

## Setup & Installation

1. **Clone the repository:**
2. **Install dependencies:**
   ```bash
   npm install
   ```
3. **Configure environment variables:**
   - Create a `.env` file in the root directory.
   - Add required variables (see Environment Configuration below).
4. **Start the service:**
   ```bash
   npm start
   ```

## Environment Configuration

Create a `.env` file with the following variables:

```
PORT=8000
FRONTEND_URL=""
SCRAPING_SERVICE_URL=""
ML_SERVICE_URL=""
JWT_SECRET=""
MONGO_URI=""
DATABASE_NAME=""
```

## Usage

- The service runs on the configured port (default: `8000`).
- Interacts with other EstiMotor microservices via HTTP and WebSocket proxies.

## API Endpoints

### Authentication
- `POST /api/admin/login` — Login as admin

### Admin Management
- `GET /api/admin` — Get admin details
- `POST /api/admin` — Create new admin
- `PUT /api/admin/:id` — Update admin
- `DELETE /api/admin/:id` — Delete admin

### Proxy Endpoints
- `/api/ml/*` — Routes to ML service
- `/api/scraping/*` — Routes to scraping service
- `/api/ws/*` — Routes to websocket service
