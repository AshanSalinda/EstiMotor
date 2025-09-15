# EstiMotor Frontend

![Home Page](public/screenshot-1.png)

EstiMotor is a modern web application for used vehicle price valuation, built with React and Vite. This frontend provides a fast, responsive, and user-friendly interface for users and administrators to estimate vehicle prices and manage model training.

## 🚗 Features

- **User Authentication:** Secure login and session management.
- **Vehicle Valuation:** Input vehicle details and receive price estimates.
- **Admin Management:** Add, update, and delete admin accounts.
- **Model Training:** Trigger and monitor model training for price prediction.
- **Progress Tracking:** Real-time progress bars and status updates.
- **Responsive Design:** Optimized for desktop and mobile devices.
- **PWA Support:** Installable as a Progressive Web App.

## 📦 Tech Stack

- **React** (with hooks and context)
- **Vite** (fast development and build)
- **Tailwind CSS** (utility-first styling)
- **PostCSS** (CSS processing)
- **Workbox** (service worker for PWA)
- **Custom Hooks & Contexts** (for state management)
- **REST API Integration** (via custom API modules)

## 🛠️ Getting Started

### Prerequisites

- Node.js (v16+ recommended)
- npm

### Installation

1. Clone the repository:
2. Install dependencies:
   ```bash
    npm install
   ```

3. Start the development server:
   ```bash
    npm run dev
   ```

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

## 📁 Project Structure

```
Frontend
├── dev-dist                # Development build output
├── public                  # Static assets (images)
└── src                     # Main source code
│   ├── index.css           # Global styles
│   ├── main.jsx            # Entry point
│   ├── api                 # API modules
│   ├── components          # Reusable UI components
│   ├── context             # React context providers
│   ├── data                # Static data files
│   ├── hooks               # Custom React hooks
│   ├── pages               # Application pages
│   ├── routes              # Route definitions and protection
│   ├── sections            # Page sections and layouts
│   └── theme               # Theme configuration
├── index.html              # HTML template
├── package.json            # Project metadata and scripts
├── postcss.config.js       # PostCSS configuration
├── tailwind.config.js      # Tailwind CSS configuration
├── vite.config.js          # Vite configuration
└── .env                    # Environment variables
```

## 🔒 Environment Variables

Create a `.env` file in the root directory for API endpoints and secrets:

```
VITE_API_BASE_URL=https://your-api-url.com
```
