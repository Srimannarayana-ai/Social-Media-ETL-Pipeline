-- Deletes the tables if they exist to start fresh each time
DROP TABLE IF EXISTS tweets;
DROP TABLE IF EXISTS quarantine_tweets;

-- Creates the tweets table
CREATE TABLE tweets (
    id SERIAL PRIMARY KEY,
    tweet_id BIGINT,
    entity VARCHAR(255),
    sentiment VARCHAR(50),
    tweet_content TEXT
);

-- Creates the quarantine_tweets table
CREATE TABLE quarantine_tweets (
    id SERIAL PRIMARY KEY,
    tweet_id BIGINT,
    entity VARCHAR(255),
    sentiment VARCHAR(50),
    tweet_content TEXT,
    quarantine_reason TEXT,
    quarantine_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);