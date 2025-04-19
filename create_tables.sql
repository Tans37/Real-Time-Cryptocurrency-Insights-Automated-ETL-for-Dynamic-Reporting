-- Table: crypto_prices
CREATE TABLE IF NOT EXISTS crypto_prices (
    id TEXT,                               -- Coin ID (e.g., 'bitcoin', 'ethereum')
    timestamp TIMESTAMP,                  -- Time of the price observation
    current_price DOUBLE PRECISION,       -- Current price in USD
    SMA_7 DOUBLE PRECISION,               -- 7-period Simple Moving Average
    SMA_14 DOUBLE PRECISION,              -- 14-period Simple Moving Average
    RSI_14 DOUBLE PRECISION               -- 14-period Relative Strength Index
);

-- Table: crypto_news
CREATE TABLE IF NOT EXISTS crypto_news (
    id TEXT,                               -- Coin ID or 'global'
    text TEXT,                             -- News headline text
    published_at TIMESTAMP,               -- When the news was published
    sentiment DOUBLE PRECISION            -- Sentiment score from TextBlob (-1 to +1)
);

-- Table: crypto_predictions
CREATE TABLE IF NOT EXISTS crypto_predictions (
    id TEXT,                               -- Coin ID
    prediction_time TIMESTAMP,            -- Time of forecast generation
    predicted_price DOUBLE PRECISION      -- Forecasted price for the next hour
);
