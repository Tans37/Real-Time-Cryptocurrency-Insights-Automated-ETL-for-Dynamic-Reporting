# 📊 Real-Time Cryptocurrency Insights: Automated ETL for Dynamic Reporting

A real-time crypto analytics platform that streams, analyzes, and forecasts cryptocurrency trends using Kafka, Spark, LSTM, and Streamlit.

A modular pipeline that collects real-time cryptocurrency prices and news, processes them using Apache Spark, performs technical and sentiment analysis, predicts future prices using LSTM models, and visualizes everything through an interactive Streamlit dashboard.

---
![Dashboard ss](https://github.com/user-attachments/assets/5f74378f-6d7e-4ccd-8945-badf58bd3228)


## 🚀 Features

- **Real-time ETL** with Apache Kafka and Spark
- **Technical Indicators**: SMA (7, 14), RSI (14)
- **Sentiment Analysis** on news headlines using TextBlob
- **LSTM-based Price Forecasting** (per coin, hourly)
- **Interactive Streamlit Dashboard** with:
  - Dropdown for BTC, ETH, DOGE, XRP, SOL
  - Candlestick charts
  - Technical charts (Price, SMA, RSI)
  - Predicted price for next hour
  - Current sentiment summary

---

## ⚙️ Tech Stack

- **Kafka**: Real-time producers for crypto prices and news
- **Apache Spark**: Streaming ETL, technical analysis, sentiment scoring
- **PostgreSQL**: Central data store for prices, news, and predictions
- **LSTM Model (Keras/TensorFlow)**: Hourly price forecasting
- **Streamlit + Plotly**: Dashboard with charts & metrics
- **TextBlob**: News sentiment polarity scoring

---

## 🔌 APIs Used

- **[CoinGecko API](https://www.coingecko.com/en/api)**: Provides real-time market data for cryptocurrencies including price, volume, and market cap.
- **[CryptoPanic API](https://cryptopanic.com/developers/api/)**: Streams crypto-related news headlines for sentiment analysis.

---

## 📂 Folder Structure

```
├── kafka_producer/
│   ├── crypto_producer.py
│   └── news_producer.py
├── spark_etl/
│   ├── spark_etl_crypto.py
│   ├── spark_etl_news.py
│   └── technical_analysis.py
├── sentiment_analysis/
│   └── sentiment_udf.py
├── database/
│   └── write_to_postgres.py
├── dashboard/
│   └── app.py
├── models/
│   └── bitcoin_lstm.h5 (etc.)
├── run_hourly_forecast.py
├── create_tables.sql
├── requirements.txt
└── README.md
```

## 🔧 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Tans37/Real-Time-Cryptocurrency-Insights-Automated-ETL-for-Dynamic-Reporting.git
cd Real-Time-Cryptocurrency-Insights-Automated-ETL-for-Dynamic-Reporting
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Start Kafka + Zookeeper
(Use Docker Compose or your local Kafka install)

### 4. Run Producers
```bash
python kafka_producer/crypto_producer.py
python kafka_producer/news_producer.py
```

### 5. Run Spark Streaming Jobs
```bash
spark-submit spark_etl/spark_etl_crypto.py
spark-submit spark_etl/spark_etl_news.py
```

### 6. Run LSTM Forecast Hourly
```bash
python run_hourly_forecast.py bitcoin
```
(Schedule with cron or Airflow for hourly runs)

### 7. Launch Dashboard
```bash
streamlit run dashboard/app.py
```
PS: You would also need to insert your api keys to fetch data.
---

## 🧠 Prediction Example

```json
{
  "id": "bitcoin",
  "prediction_time": "2025-04-18T10:00:00Z",
  "predicted_price": 65471.12
}
```

---

## 📌 Notes

- Trained LSTM models should be stored in `models/` folder as `<coin>_lstm.h5`
- You can customize the forecast logic in `run_hourly_forecast.py`
- PostgreSQL table schemas can be created using `create_tables.sql`

---

## 📬 Contact

**Tanishq Sharma**  
[LinkedIn](https://www.linkedin.com/in/tanishq-sharma-ts)

---

