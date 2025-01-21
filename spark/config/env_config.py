import os
from dotenv import load_dotenv

load_dotenv()

KAFKA_BROKER = os.getenv("KAFKA_BROKER")
KAFKA_CDC_TOPIC = os.getenv("KAFKA_CDC_TOPIC")
SPARK_APP_NAME = os.getenv("SPARK_APP_NAME")
SPARK_MASTER = os.getenv("SPARK_MASTER")
