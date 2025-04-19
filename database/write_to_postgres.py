
def write_to_postgres(df, table_name):
    df.write.format("jdbc") \
        .option("url", "jdbc:postgresql://localhost:5432/crypto_db") \
        .option("dbtable", table_name) \
        .option("user", "your_username") \
        .option("password", "your_password") \
        .option("driver", "org.postgresql.Driver") \
        .mode("append") \
        .save()
