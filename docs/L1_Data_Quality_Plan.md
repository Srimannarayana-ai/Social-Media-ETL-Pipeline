# Level 1 Upgrade Plan: Data Quality & Logging

Implementing Data Quality (Level 1) before introducing Orchestration (Level 3) is a core Data Engineering best practice. Airflow is only as good as the pipeline it runs.

## Goal
Implement a robust logging framework to replace standard print statements, and introduce a quarantine pattern to catch and isolate "bad data" instead of blindly deleting it.

## Proposed Changes

### [MODIFY] Database Schema

#### [MODIFY] `sql/create_tables.sql`
* **[NEW]** Add `DROP TABLE IF EXISTS quarantine_tweets;`
* **[NEW]** Add `CREATE TABLE quarantine_tweets (...)` to store rows that fail data quality checks, along with a `quarantine_reason` text column and a `quarantine_timestamp`.

### [MODIFY] Python Pipeline

#### [MODIFY] `src/etl_pipeline.py`
* **Logging Setup:** Import Python's built-in `logging` module. Replace all `print()` statements. Logs will output to the terminal and a `logs/pipeline.log` file.
* **Bug Fix:** Remove `df = df.drop(columns=['tweet_id'])` from the transform function. We will preserve it so the DB structure accepts it properly.
* **Quarantine Framework:** 
  * Identify missing or corrupt data (e.g., missing text or missing sentiment) instead of aggressive `.dropna`.
  * Split the dataset into `valid_df` and `quarantine_df`.
  * Add standard Quarantine metadata columns: `quarantine_reason` and `quarantine_timestamp`.
  * Load the `quarantine_df` into the new `quarantine_tweets` PostgreSQL table.
