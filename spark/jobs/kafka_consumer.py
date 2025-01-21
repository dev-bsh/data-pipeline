from pyspark.sql.functions import from_json, col
from config.schema import debezium_cdc_schema
from config.env_config import KAFKA_BROKER, KAFKA_CDC_TOPIC

def read_from_kafka(spark):
    return (spark.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", KAFKA_BROKER)
        .option("subscribe", KAFKA_CDC_TOPIC)
        .option("startingOffsets", "latest")
        .load())

def parse_kafka_data(df):
    return (df.selectExpr("CAST(value AS STRING)")
            .select(from_json(col("value"), debezium_cdc_schema).alias("data"))
            .select("data.payload.after.*")
            # Spark에서 timestamp를 초 단위로 처리해서 ms단위 변환 진행
            .withColumn("timestamp", (col("timestamp") / 1000).cast("timestamp"))) 
