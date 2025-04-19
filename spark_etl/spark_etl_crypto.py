from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, to_timestamp
from technical_analysis import add_technical_indicators
from database.write_to_postgres import write_to_postgres

spark = SparkSession.builder.appName("CryptoETL").getOrCreate()

crypto_df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "crypto_prices") \
    .load()

parsed_df = crypto_df.selectExpr("CAST(value AS STRING)")
# Assume schema defined elsewhere, or use spark.read.json(parsed_df.rdd.map(lambda r: r[0])).printSchema()
schema = "id STRING, current_price DOUBLE, last_updated STRING"

parsed_df = parsed_df.withColumn("json", from_json("value", schema)) \
    .select("json.*") \
    .withColumn("timestamp", to_timestamp("last_updated"))

parsed_df = add_technical_indicators(parsed_df)
write_to_postgres(parsed_df, "crypto_prices")
