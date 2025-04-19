import pandas as pd
import numpy as np
import psycopg2
import sys
from tensorflow.keras.models import load_model
from datetime import datetime

SEQ_LENGTH = 24
COIN_ID = sys.argv[1] if len(sys.argv) > 1 else "bitcoin"

DB_PARAMS = {
    'dbname': "crypto_db",
    'user': "your_username",
    'password': "your_password",
    'host': "localhost"
}

def fetch_recent_data():
    conn = psycopg2.connect(**DB_PARAMS)
    query = f"""
        SELECT timestamp, current_price, SMA_7, SMA_14, RSI_14
        FROM crypto_prices
        WHERE id = '{COIN_ID}'
        ORDER BY timestamp DESC LIMIT {SEQ_LENGTH}
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df.sort_values("timestamp")

def prepare_input(df):
    df = df.drop(columns=['timestamp'])
    X = df.values
    X = (X - X.mean(axis=0)) / (X.std(axis=0) + 1e-6)
    return np.expand_dims(X, axis=0)

def predict_next_hour(model_path, X):
    model = load_model(model_path)
    y_pred = model.predict(X)
    return y_pred[0][-1]

def save_prediction(price):
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO crypto_predictions (id, prediction_time, predicted_price) VALUES (%s, %s, %s)",
        (COIN_ID, datetime.utcnow(), float(price))
    )
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    df = fetch_recent_data()
    if len(df) >= SEQ_LENGTH:
        X = prepare_input(df)
        pred_price = predict_next_hour(f"./models/{COIN_ID}_lstm.h5", X)
        print(f"[{COIN_ID}] Predicted next-hour price: ${pred_price:.2f}")
        save_prediction(pred_price)
