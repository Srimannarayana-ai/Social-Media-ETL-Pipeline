# Level 3 Upgrade Plan: Orchestration (Apache Airflow)

With our data quality checks in place, the pipeline is officially stable enough to be orchestrated.

## Goal
Introduce Apache Airflow to orchestrate the ETL pipeline. We will create a Directed Acyclic Graph (DAG) that acts as the "manager" of the pipeline, triggering it to run automatically on a set schedule.

## Proposed Changes

### [NEW] The Airflow Environment

#### [MODIFY] `docker-compose.yml`
We will introduce Airflow into our multi-container setup. 
* Add a new `airflow` service using the official Apache Airflow image.
* Configure it to run the `airflow standalone` command for local development environments.
* Mount a new `./dags` folder to the container.

#### [NEW] `requirements-airflow.txt`
* Dedicated requirements file for the Airflow container to prevent dependency conflicts with our ETL script.

### [NEW] The DAG

#### [NEW] `dags/social_media_dag.py`
* Define a logical DAG named `social_media_sentiment_etl`.
* Set a schedule interval (e.g., `@daily` to run every night at midnight).
* We will use a `BashOperator` task that executes our `src/etl_pipeline.py` script automatically.
