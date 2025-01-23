from pyspark.sql import SparkSession
from config.env_config import SPARK_APP_NAME, SPARK_MASTER
from jobs.kafka_consumer import read_from_kafka, parse_kafka_data
from jobs.spark_aggregator import *
from jobs.elasticsearch_writer import write_to_elasticsearch

def main():
    # SparkSession 생성
    spark = (SparkSession.builder
             .appName(SPARK_APP_NAME)
             .master(SPARK_MASTER)
             .config("spark.jars.packages", "org.elasticsearch:elasticsearch-spark-30_2.12:8.13.4,org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.4")
             .getOrCreate()
    )
    
    spark.sparkContext.setLogLevel("WARN")

    # Kafka 메세지 수집
    df_raw = read_from_kafka(spark)
    df_json = parse_kafka_data(df_raw).withWatermark("timestamp", "10 seconds")
    
    # Spark 집계 생성
    df_unique_users = aggregate_unique_users(df_json)
    df_purchase_count = aggregate_purchase_count(df_json)
    df_product_metrics = aggregate_product_metrics(df_json)

    # Elasticsearch 저장
    write_to_elasticsearch(df_unique_users, "unique_users_index", "append")
    write_to_elasticsearch(df_purchase_count, "purchase_count_index", "append")
    write_to_elasticsearch(df_product_metrics, "product_metrics_index", "append")

    spark.streams.awaitAnyTermination()

if __name__ == "__main__":
    main()
