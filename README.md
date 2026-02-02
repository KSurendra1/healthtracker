# Health & Fitness Tracker (IoT Ready)

A Django-based Health & Fitness Tracker designed for integrating wearable data (Fitbit, Google Fit) and IoT device streams.

## Features

-   **Integrations**:
    -   **Fitbit**: OAuth2 client with automatic token refreshing (`apps/integrations/fitbit`).
    -   **Google Fit**: Structure in place for Google Fit integration.
-   **Architecture**:
    -   **Backend**: Django & Django REST Framework.
    -   **Database**: PostgreSQL.
    -   **Caching/Queues**: Redis.
    -   **IoT/Real-time**: Eclipse Mosquitto (MQTT Broker).
-   **Containerization**: Fully Dockerized setup.

## Quick Start

### Prerequisites
-   Docker & Docker Compose

### Setup

1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd healthtracker
    ```

2.  **Environment Variables**:
    Copy the example environment file:
    ```bash
    cp .env.example .env
    ```
    *Note: The default `.env` is pre-configured for local Docker development.*

3.  **Run with Docker**:
    Build and start the services:
    ```bash
    docker-compose up --build -d
    ```

4.  **Setup Database**:
    Apply migrations to set up the schema:
    ```bash
    docker-compose exec web python manage.py migrate
    ```

5.  **Access the Application**:
    -   **Web App**: [http://localhost:8000](http://localhost:8000)
    -   **Admin Panel**: [http://localhost:8000/admin](http://localhost:8000/admin)
        -   **Username**: `admin`
        -   **Password**: `admin`

## Development

### Running Tests
Run the unit tests within the Docker container:
```bash
docker-compose exec web python manage.py test
```

*Note: Ensure `apps/__init__.py` and `apps/integrations/__init__.py` exist for test discovery.*

To run specifically the Fitbit integration tests:
```bash
docker-compose exec web python manage.py test apps.integrations.tests.test_fitbit_client_impl
```

### Directory Structure
-   `apps/`: Django apps (features, integrations, tracker).
-   `healthtracker_project/`: Main project configuration.
-   `docs/`: Additional documentation.

## Services
The `docker-compose.yml` defines the following services:
-   `web`: The Django application server (Gunicorn).
-   `db`: PostgreSQL 15 database.
-   `redis`: Redis for caching and Celery broker.
-   `mqtt`: Mosquitto MQTT broker for IoT data ingestion.
