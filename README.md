# 💰 Personal Finance Microservices App

A modular, Dockerized web application to help users track income, expenses, generate reports, receive notifications, and export data — all powered by independent microservices.

## 📦 Features

- **Income Service** – Track various income sources.
- **Expense Service** – Log and categorize expenses.
- **Report Service** – Generate financial summaries.
- **Notification Service** – Get alerts when data changes.
- **Export Service** – Export records to CSV.
- **Authentication (Optional)** – Secure user access.

## 🧱 Architecture

Each feature is implemented as a separate microservice:

```text
[Income Service]    ┐
[Expense Service]   ┤──> [Notification Service]
                    │
                    └──> [Report Service]
                          └──> [Export Service]
Communication: RESTful API (HTTP)

Containerization: Docker & Docker Compose

Frontend: Simple web UI (React or HTML/CSS/JS)

Database: SQLite or PostgreSQL (per service)

🛠️ Tech Stack
Backend: Python (FastAPI / Flask)

Frontend: React or plain HTML/CSS/JS

Database: SQLite (dev) / PostgreSQL (prod)

Containerization: Docker

API Testing: Postman / curl

🚀 Getting Started
Prerequisites
Docker

Docker Compose

Run the App
# Clone the repo
git clone https://github.com/your-username/personal-finance-app.git
cd personal-finance-app

# Build and start all services
docker-compose up --build

Access
Frontend UI: http://localhost:3000

Income API: http://localhost:8001

Expense API: http://localhost:8002

Report API: http://localhost:8003

Notification API: http://localhost:8004

Export API: http://localhost:8005

Ports may vary based on your configuration.

🧪 Testing
You can test individual microservices using tools like curl, Postman, or built-in Swagger docs:
personal-finance-app/
├── income-service/
├── expense-service/
├── report-service/
├── notification-service/
├── export-service/
├── frontend/
├── docker-compose.yml
└── README.md
✍️ Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

📄 License
MIT License. See LICENSE for details.
