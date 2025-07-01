-- Deletes the table if it exists to start fresh each time
DROP TABLE IF EXISTS tweets;

-- Creates the tweets table
CREATE TABLE tweets (
    id SERIAL PRIMARY KEY,
    tweet_id BIGINT,
    entity VARCHAR(255),
    sentiment VARCHAR(50),
    tweet_content TEXT
);