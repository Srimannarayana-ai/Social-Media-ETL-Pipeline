# Level 2 Upgrade: Containerization Complete 🚢

We successfully containerized the entire ETL pipeline setup utilizing Docker!

## What Happened

### 1. Robust Environment Portability 
- A new **`requirements.txt`** explicitly locks the Python libraries.
- A **`Dockerfile`** installs these dependencies into an isolated `python:3.9-slim` environment.

### 2. Single-Command Orchestration
We introduced a **`docker-compose.yml`** file to handle multiple services at once. 
- Docker Compose uses `postgres:14` to launch the database immediately.
- Mapped the `sql/create_tables.sql` file natively so **the database creates its own tables automatically** upon boot.

### 3. Pipeline Dynamic Connectivity
The `src/etl_pipeline.py` script was upgraded from hardcoded paths to dynamic references:
- **Paths:** It now searches for the `data/` folder dynamically.
- **Database Connection:** We introduced a fallback `DB_HOST` variable. When operating in Docker, it automatically connects to the `postgres` internal network container.

## Verification Summary
Both containers built and started successfully. The `social_media_db` correctly initialized the tables. After that, the `social_media_etl` python script waited for the database to become healthy before executing and loading data successfully.
