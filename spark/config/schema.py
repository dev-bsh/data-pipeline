from pyspark.sql.types import StructType, StructField, StringType, LongType, FloatType, TimestampType

user_activity_after_schema = StructType([
    StructField("id", LongType()),
    StructField("user_id", LongType()),
    StructField("product_id", LongType()),
    StructField("product_name", StringType()),
    StructField("product_price", FloatType()),
    StructField("event_type", StringType()),
    StructField("timestamp", LongType()),
])

debezium_cdc_schema = StructType([
    StructField("payload", StructType([
        StructField("after", user_activity_after_schema),
    ]))
])
