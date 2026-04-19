import pandas as pd
import os
import logging
from sqlalchemy import create_engine
from dotenv import load_dotenv
from urllib.parse import quote_plus
from datetime import datetime

# --- Logging Configuration ---
log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'pipeline.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def extract_data(file_name):
    """Reads data from a CSV file located in the 'data' directory."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, 'data', file_name)
    try:
        df = pd.read_csv(file_path, encoding='latin1', header=None)
        logger.info(f"✅ Data extracted successfully! ({len(df)} rows)")
        return df
    except FileNotFoundError:
        logger.error(f"❌ Error: The file {file_name} was not found in the 'data' directory.")
        return None

def transform_data(df):
    """Cleans and transforms the raw DataFrame. Splits bad data into quarantine."""
    if df is None:
        return None, None
    
    df.columns = ['tweet_id', 'entity', 'sentiment', 'tweet_content']
    
    # Identify valid vs invalid data
    quarantine_mask = df['tweet_content'].isna()
    
    quarantine_df = df[quarantine_mask].copy()
    valid_df = df[~quarantine_mask].copy()
    
    # Add quarantine metadata
    if not quarantine_df.empty:
        quarantine_df['quarantine_reason'] = "Missing tweet_content component"
        quarantine_df['quarantine_timestamp'] = datetime.now()

    logger.info(f"✅ Data transformed successfully! Valid rows: {len(valid_df)}. Quarantined rows: {len(quarantine_df)}.")
    return valid_df, quarantine_df

def load_to_db(df, table_name='tweets'):
    """Loads a DataFrame into the specified PostgreSQL table."""
    if df is None or df.empty:
        logger.info(f"⚠️ No data to insert into {table_name}.")
        return

    load_dotenv()
    db_password = os.getenv("DB_PASSWORD")
    if not db_password:
        logger.error("❌ Error: DB_PASSWORD not found in .env file.")
        return

    # URL-encode the password to handle special characters
    encoded_password = quote_plus(db_password)
    
    # Retrieve DB_HOST from environment, default to localhost
    db_host = os.getenv("DB_HOST", "localhost")
    
    # Create database connection string and engine with the encoded password
    db_url = f'postgresql+psycopg2://postgres:{encoded_password}@{db_host}:5432/social_media_db'
    engine = create_engine(db_url)

    try:
        df.to_sql(table_name, engine, if_exists='append', index=False)
        logger.info(f"✅ {len(df)} rows successfully loaded into the '{table_name}' table!")
    except Exception as e:
        logger.error(f"❌ Error loading data to table '{table_name}': {e}")


# --- Main execution ---
if __name__ == "__main__":
    logger.info("🚀 Starting Social Media ETL Pipeline...")
    raw_df = extract_data('twitter_training.csv')
    
    valid_df, quarantine_df = transform_data(raw_df)
    
    if valid_df is not None:
        load_to_db(valid_df, table_name='tweets')
        
    if quarantine_df is not None and not quarantine_df.empty:
        load_to_db(quarantine_df, table_name='quarantine_tweets')

    logger.info("🏁 Pipeline execution finished.")