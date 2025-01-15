import os
import json
import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")

# 데이터 원천 DB 환경변수
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

# debezium 관련 환경변수
kafka_bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
kafka_connect_host = os.getenv("KAFKA_CONNECT_HOST")
connector_name = os.getenv("CONNECTOR_NAME")
db_server_name = os.getenv("DB_SERVER_NAME")
db_server_id = os.getenv("DB_SERVER_ID")
table_include_list = os.getenv("TABLE_INCLUDE_LIST")

# Kafka Connect REST API URL
kafka_connect_url = f"{kafka_connect_host}/connectors"

# Debezium 커넥터 설정
connector_config = {
    "name": connector_name,
    "config": {
        "connector.class": "io.debezium.connector.mysql.MySqlConnector",
        "tasks.max": "1",
        "database.hostname": db_host,
        "database.port": db_port,
        "database.user": db_user,
        "database.password": db_password,
        "database.server.id": db_server_id,
        "database.server.name": db_server_name,
        "database.include.list": db_name,
        "table.include.list": table_include_list,
        "database.history.kafka.bootstrap.servers": kafka_bootstrap_servers,
        "database.history.kafka.topic": f"schema-changes.{db_name}",
        "topic.prefix": db_name,
        "schema.history.internal.kafka.topic": f"schema-history.{db_name}",
        "schema.history.internal.kafka.bootstrap.servers": kafka_bootstrap_servers
    }
}

# Kafka Connect로 요청
response = requests.post(
    kafka_connect_url,
    headers={"Content-Type": "application/json"},
    data=json.dumps(connector_config)
)

if response.status_code == 201:
    print(f"'{connector_name}' 커넥터 등록 성공")
else:
    print(f"커넥터 등록 실패, Status code: {response.status_code}")
    print("Response:", response.text)