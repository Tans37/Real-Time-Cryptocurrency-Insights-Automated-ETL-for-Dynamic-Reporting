from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, expr
from sentiment_analysis.sentiment_udf import get_sentiment
from database.write_to_postgres import write_to_postgres

spark = SparkSession.builder.appName("CryptoNewsETL").getOrCreate()

# Register UDF
spark.udf.register("get_sentiment", get_sentiment)

# Read from Kafka topic 'crypto_news'
news_df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "crypto_news") \
    .load()

# Parse Kafka JSON value
parsed_news = news_df.selectExpr("CAST(value AS STRING)") \
    .withColumn("json", from_json("value", "text STRING, published_at STRING, id STRING")) \
    .select("json.*") \
    .withColumn("sentiment", expr("get_sentiment(text)"))

# Write to PostgreSQL table 'crypto_news'
write_to_postgres(parsed_news, "crypto_news")
