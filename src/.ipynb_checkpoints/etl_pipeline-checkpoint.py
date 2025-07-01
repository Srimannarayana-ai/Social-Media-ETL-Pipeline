import pandas as pd
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from urllib.parse import quote_plus # <-- IMPORT THE FIX

def extract_data(file_name):
    """Reads data from a CSV file located in the 'data' directory."""
    file_path = os.path.join(os.getcwd(), '..', 'data', file_name)
    try:
        df = pd.read_csv(file_path, encoding='latin1', header=None)
        print("✅ Data extracted successfully!")
        return df
    except FileNotFoundError:
        print(f"❌ Error: The file {file_name} was not found in the 'data' directory.")
        return None

def transform_data(df):
    """Cleans and transforms the raw DataFrame."""
    if df is None:
        return None
    
    df.columns = ['tweet_id', 'entity', 'sentiment', 'tweet_content']
    df = df.drop(columns=['tweet_id'])
    df.dropna(subset=['tweet_content'], inplace=True)

    print("✅ Data transformed successfully!")
    return df

def load_to_db(df):
    """Loads the transformed DataFrame into the PostgreSQL database."""
    if df is None:
        return

    load_dotenv()
    db_password = os.getenv("DB_PASSWORD")
    if not db_password:
        print("❌ Error: DB_PASSWORD not found in .env file.")
        return

    # --- THE FIX IS HERE ---
    # URL-encode the password to handle special characters
    encoded_password = quote_plus(db_password)
    
    # Create database connection string and engine with the encoded password
    db_url = f'postgresql+psycopg2://postgres:{encoded_password}@localhost:5432/social_media_db'
    engine = create_engine(db_url)

    try:
        df.to_sql('tweets', engine, if_exists='append', index=False)
        print("✅ Data loaded successfully into the PostgreSQL database!")
    except Exception as e:
        print(f"❌ Error loading data to database: {e}")


# --- Main execution ---
if __name__ == "__main__":
    raw_df = extract_data('twitter_training.csv')
    transformed_df = transform_data(raw_df)
    
    if transformed_df is not None:
        print("First 5 rows of transformed data:")
        print(transformed_df.head())
        load_to_db(transformed_df)