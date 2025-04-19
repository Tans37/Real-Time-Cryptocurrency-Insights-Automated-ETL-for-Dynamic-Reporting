from kafka import KafkaProducer
import requests
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def fetch_news_data():
    url = 'https://cryptopanic.com/api/v1/posts/?auth_token=demo&public=true'
    response = requests.get(url)
    if response.status_code == 200:
        news_data = response.json()['results']
        for news in news_data:
            producer.send('crypto_news', value=news)

if __name__ == "__main__":
    fetch_news_data()
    producer.flush()
    producer.close()        