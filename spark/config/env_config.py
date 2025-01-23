import os
from dotenv import load_dotenv

load_dotenv()

# Kafka 설정정
KAFKA_BROKER = os.getenv("KAFKA_BROKER")
KAFKA_CDC_TOPIC = os.getenv("KAFKA_CDC_TOPIC")

# Spark 설정
SPARK_APP_NAME = os.getenv("SPARK_APP_NAME")
SPARK_MASTER = os.getenv("SPARK_MASTER")

# Elasticsearch 공통 옵션
ES_COMMON_OPTIONS = {
    "es.nodes": os.getenv("ES_NODES"),
    "es.port": os.getenv("ES_PORT"),
    "es.net.ssl": os.getenv("ES_SSL"),
    "es.net.http.auth.user": os.getenv("ES_USER", ""),
    "es.net.http.auth.pass": os.getenv("ES_PASSWORD", ""),
    "es.nodes.wan.only": os.getenv("ES_WAN_ONLY"),
}