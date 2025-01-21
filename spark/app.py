from pyspark.sql import SparkSession
from config.env_config import SPARK_APP_NAME, SPARK_MASTER
from jobs.kafka_consumer import read_from_kafka, parse_kafka_data
from jobs.spark_aggregator import *

def main():
    # SparkSession 생성
    spark = (SparkSession.builder
             .appName(SPARK_APP_NAME)
             .master(SPARK_MASTER)
             .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.4")
             .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")

    # Kafka 메세지 변환
    df_raw = read_from_kafka(spark)
    df_json = parse_kafka_data(df_raw) 

    # Aggregators
    df_users = aggregate_unique_users(df_json)
    df_avg_purchase = aggregate_avg_purchase_amount(df_json)
    df_prod_views = aggregate_product_views(df_json)
    df_prod_conversion = aggregate_purchase_conversion(df_json)


    q1 = (
        df_users.writeStream
        .outputMode("complete")
        .format("console")
        .option("truncate", "false")
        .option("checkpointLocation", "/tmp/checkpoints/unique_users")
        .start()
    )

    q2 = (
        df_avg_purchase.writeStream
        .outputMode("complete")
        .format("console")
        .option("truncate", "false")
        .option("checkpointLocation", "/tmp/checkpoints/avg_purchase")
        .start()
    )

    q3 = (
        df_prod_views.writeStream
        .outputMode("complete")
        .format("console")
        .option("truncate", "false")
        .option("checkpointLocation", "/tmp/checkpoints/product_views")
        .start()
    )

    q4 = (
        df_prod_conversion.writeStream
        .outputMode("complete")
        .format("console")
        .option("truncate", "false")
        .option("checkpointLocation", "/tmp/checkpoints/purchase_conversion")
        .start()
    )

    spark.streams.awaitAnyTermination()

if __name__ == "__main__":
    main()
