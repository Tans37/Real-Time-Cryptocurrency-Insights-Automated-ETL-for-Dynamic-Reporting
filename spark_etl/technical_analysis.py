from pyspark.sql.functions import col, lag, avg, when
from pyspark.sql.window import Window

def add_technical_indicators(df):
    window_spec = Window.partitionBy("id").orderBy("timestamp").rowsBetween(-14, 0)

    df = df.withColumn("SMA_7", avg("current_price").over(window_spec.rowsBetween(-6, 0)))
    df = df.withColumn("SMA_14", avg("current_price").over(window_spec))

    df = df.withColumn("price_diff", col("current_price") - lag("current_price", 1).over(window_spec))
    df = df.withColumn("gain", when(col("price_diff") > 0, col("price_diff")).otherwise(0))
    df = df.withColumn("loss", when(col("price_diff") < 0, -col("price_diff")).otherwise(0))
    df = df.withColumn("avg_gain", avg("gain").over(window_spec))
    df = df.withColumn("avg_loss", avg("loss").over(window_spec))
    df = df.withColumn("rs", col("avg_gain") / (col("avg_loss") + 1e-6))
    df = df.withColumn("RSI_14", 100 - (100 / (1 + col("rs"))))
    return df
