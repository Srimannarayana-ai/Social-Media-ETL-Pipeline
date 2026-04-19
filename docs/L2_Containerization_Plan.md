# Social Media ETL Pipeline - Level 2 Upgrade Plan

This implementation plan focuses on elevating the project via **Containerization (Docker)**. This will ensure that the Python pipeline and PostgreSQL database can operate in an isolated, identical environment on any machine, which is a core expectation for Data Engineers.

## Goal

Dockerize the Social Media ETL Pipeline to enable a single-command setup (`docker-compose up`) that handles spinning up the PostgreSQL database and running the Python ETL script.

## Proposed Changes

### [NEW] Docker Configuration

#### [NEW] `Dockerfile`
* Use a lightweight Python base image (e.g., `python:3.9-slim`).
* Install requires packages from `requirements.txt`.
* Copy the `src` and `data` directories into the container.
* Set the entrypoint to run `python src/etl_pipeline.py`.

#### [NEW] `docker-compose.yml`
* **Service 1: `postgres`**
  * Image: `postgres:14`
  * Use an environment file (`.env`) to load database setup credentials.
  * Initialize the database schema by mapping `sql/create_tables.sql` into `/docker-entrypoint-initdb.d/`.
* **Service 2: `etl_pipeline`**
  * Built using the new `Dockerfile`.
  * Waits for the `postgres` service to be healthy before starting.
  * Connects to the database using the Docker internal network.

### [MODIFY] Python Script

#### [MODIFY] `src/etl_pipeline.py`
* Update line 46 to read the database host from environment variables (e.g., `os.getenv("DB_HOST", "localhost")`). 
* Update the file path logic to ensure it dynamically finds the `data` folder regardless of container context.
