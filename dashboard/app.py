import streamlit as st
import pandas as pd
import psycopg2
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("📊 Real-Time Crypto Insights")

crypto_options = {
    "Bitcoin": "bitcoin",
    "Ethereum": "ethereum",
    "Dogecoin": "dogecoin",
    "Ripple": "ripple",
    "Solana": "solana"
}
selected = st.selectbox("Select Cryptocurrency", options=list(crypto_options.keys()))
selected_id = crypto_options[selected]

@st.cache_data
def load_data(coin_id):
    conn = psycopg2.connect(dbname="crypto_db", user="your_username", password="your_password", host="localhost")
    price_df = pd.read_sql(
        f"SELECT * FROM crypto_prices WHERE id = '{coin_id}' ORDER BY timestamp DESC LIMIT 500", conn)
    pred_df = pd.read_sql(
        f"SELECT * FROM crypto_predictions WHERE id = '{coin_id}' ORDER BY prediction_time DESC LIMIT 1", conn)
    conn.close()
    return price_df.sort_values("timestamp"), pred_df

price_df, pred_df = load_data(selected_id)

# ---------------------- Candlestick Chart ----------------------
st.subheader(f"🕯️ {selected} Candlestick (Hourly Aggregated)")

# Convert timestamp to hourly bins
price_df['hour'] = price_df['timestamp'].dt.floor('H')
ohlc = price_df.groupby('hour').agg({
    'current_price': ['first', 'max', 'min', 'last']
}).reset_index()

ohlc.columns = ['hour', 'open', 'high', 'low', 'close']

fig = go.Figure(data=[go.Candlestick(
    x=ohlc['hour'],
    open=ohlc['open'],
    high=ohlc['high'],
    low=ohlc['low'],
    close=ohlc['close']
)])
fig.update_layout(xaxis_title="Time", yaxis_title="Price (USD)", height=500)
st.plotly_chart(fig, use_container_width=True)

# ---------------------- Price + SMA Chart ----------------------
st.subheader(f" {selected} Price + Moving Averages")
st.line_chart(price_df.set_index("timestamp")[["current_price", "SMA_7", "SMA_14"]])

# ---------------------- RSI ----------------------
st.subheader("RSI Momentum")
st.line_chart(price_df.set_index("timestamp")[["RSI_14"]])

# ---------------------- Prediction ----------------------
st.subheader("🧠 Next Hour Forecast")
if not pred_df.empty:
    st.metric("Predicted Price", f"${pred_df['predicted_price'].iloc[0]:.2f}")
else:
    st.warning("No prediction available yet.")

# ---------------------- Sentiment ----------------------
st.subheader("🗣️ Current Sentiment")

if not news_df.empty and 'sentiment' in news_df.columns:
    avg_sentiment = news_df['sentiment'].mean()
    if avg_sentiment > 0.05:
        sentiment_label = "Positive"
        sentiment_color = "🟢"
    elif avg_sentiment < -0.05:
        sentiment_label = "Negative"
        sentiment_color = "🔴"
    else:
        sentiment_label = "Neutral"
        sentiment_color = "⚪"

    st.metric("Sentiment (last 50 headlines)", f"{sentiment_color} {sentiment_label}")
else:
    st.warning("No recent sentiment data available.")
