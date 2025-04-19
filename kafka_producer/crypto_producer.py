from kafka import KafkaProducer
import requests
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

TRACKED_COINS = ['bitcoin', 'ethereum', 'dogecoin', 'ripple', 'solana']

def fetch_crypto_data():
    url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for coin in data:
            if coin['id'] in TRACKED_COINS:
                producer.send('crypto_prices', value=coin)

if __name__ == "__main__":
    fetch_crypto_data()
    producer.flush()
    producer.close()