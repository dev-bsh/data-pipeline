# 데이터 집계 및 모니터링 파이프라인

## 목차

- [프로젝트 개요](#프로젝트-개요)
- [기술 스택](#기술-스택)
- [아키텍처 다이어그램](#아키텍처-다이어그램)
- [사전 준비](#사전-준비)
- [설치 및 실행 방법](#설치-및-실행-방법)
    1. [Repository Clone](#1-repository-clone)
    2. [Kafka, Zookeeper, Debezium 실행](#2-kafka-zookeeper-debezium-실행)
    3. [MySQL 데이터베이스 설정](#3-mysql-데이터베이스-설정)
    4. [Debezium 커넥터 설정](#4-debezium-커넥터-설정)
    5. [Spark Driver 설정](#5-spark-driver-설정)
    6. [Elasticsearch, Spark, Kibana 실행](#6-elasticsearch-spark-kibana-실행)
    7. [Elasticsearch Index 생성](#7-elasticsearch-index-생성)
    8. [더미 데이터 삽입 및 검증](#8-더미-데이터-삽입-및-검증)
- [모니터링 및 시각화](#모니터링-및-시각화)
- [디렉터리 구조](#디렉토리-구조)

---

## 프로젝트 개요

**데이터 집계 및 모니터링 파이프라인**은 MySQL, Kafka, Spark, Elasticsearch, Kibana를 통합하여 **실시간 로그 데이터의 집계 및 시각화**를 제공합니다.

**주요 목표**
- MySQL의 변경 데이터를 실시간으로 추적 및 스트리밍.
- Kafka를 통해 데이터를 Spark로 전달.
- Spark에서 데이터를 처리 및 집계.
- Elasticsearch에 집계 데이터를 저장하고, Kibana로 시각화.
---

## 기술 스택
- **데이터베이스**: MySQL
- **CDC(Change Data Capture)**: Debezium
- **메시징 플랫폼**: Kafka
- **데이터 처리**: Apache Spark, PySpark, Python
- **데이터 저장**: Elasticsearch
- **데이터 시각화**: Kibana
- **컨테이너 환경**: Docker & Docker Compose

---

## 아키텍처 다이어그램
![Image](https://github.com/user-attachments/assets/a7e5ee9c-3ef5-4ac1-af90-2b1414a7b988)
> **데이터 흐름**
    ``
    MySQL → Debezium → Kafka → Spark → Elasticsearch → Kibana
    ``
---

## 사전 준비
프로젝트를 설정하기 전에 다음 도구들이 설치되어 있어야 합니다
- **Docker** 및 **Docker Compose**
- **Python**
- **Git**
---

## 설치 및 실행 방법

### 1. Repository Clone
```bash
git clone https://github.com/dev-bsh/data-pipeline.git
cd data-pipeline/
```

### 2. Kafka, Zookeeper, Debezium 실행
```bash
docker-compose up -d zookeeper kafka debezium
```
> **옵션** Kafka-UI를 사용하고 싶다면 다음과 같이 실행할 수 있습니다.
```bash
docker-compose up -d zookeeper kafka debezium akhq
```

### 3. MySQL 데이터베이스 설정
- ``db/schema.sql`` 파일을 기반으로 테이블을 생성합니다.
- Debezium은 MySQL의 Binlog를 사용하므로 MySQL 서버에 Binlog가 활성화되어 있어야 합니다.
    ```SQL 
    SHOW VARIABLES LIKE 'log_bin';
    ```
- time_zone이 SYSTEM인 경우 명시적으로 변경이 필요합니다.
    ```SQL
    -- time_zone 확인
    SELECT @@global.time_zone, @@session.time_zone;
    -- time_zone 설정
    SET GLOBAL time_zone = '+09:00';
    -- my.cnf 파일 설정
    [mysqld]
    default-time-zone='+09:00'
    ```
- 필요시 DB User 생성 및 권한 설정
    ```SQL
    -- 권한 부여
    GRANT SELECT, RELOAD, SHOW DATABASES, REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'username'@'%';
    -- 변경 사항 적용
    FLUSH PRIVILEGES;
    ```

### 4. Debezium 커넥터 설정
- ``debezium/.env.example`` 파일의 환경변수를 설정하여 ``./debezium/.env``파일 생성
- kafka에 등록하기 위해 mysql-connector 요청 스크립트 실행
  ```bash
  cd /debezium
  python debezium_connect.py
  ```

### 5. Spark Driver 설정
- ``spark/config/.env.example`` 파일의 환경변수를 설정하여 ``spark/config/.env`` 파일 생성
- docker compose로 spark-driver 이미지 실행 시 자동 빌드

### 6. Elasticsearch, Spark, Kibana 실행
```bash
docker-compose up -d spark-master spark-worker spark-driver elasticsearch kibana
```

### 7. Elasticsearch Index 생성
``/elasticsearch/index-config.txt`` 파일의 내용에 따라 Kibana에서 Index 생성 요청 실행


### 8. 더미 데이터 삽입 및 검증
더미 데이터를 삽입하여 Kibana에서 데이터를 확인합니다.
```bash
cd db
python insert_dummy_data.py
```

- MySQL 데이터 적재 확인
- Kafka 메세지 등록 확인
- Spark Driver에서 프로세싱 로그 확인
- Kibana에서 Index 데이터 모니터링


## 모니터링 및 시각화
![Image](https://github.com/user-attachments/assets/86892430-57b0-4bc6-8f73-0760c8b1b419)
1. Kibana에 접속: http://localhost:5601
2. **New Visualization** 클릭.
3. Lens를 선택하고 다음 인덱스를 연결:
    - 고유 사용자: ``unique_users_index``를 선택하고 ``unique_users`` 필드 시각화.
    - 구매 통계: ``purchase_count_index``를 선택하고 ``total_purchase_amount`` 및 ``purchase_count`` 필드 시각화.
    - 상품별 지표: ``product_metrics_index``를 선택하고 ``view_count`` 및 ``purchase_count`` 필드 시각화.
4. 시각화된 데이터를 대시보드에 추가

---
## 디렉토리 구조

````plaintext
data-pipeline/
├── db/
│   ├── .env
│   ├── schema.sql                    # 테스트 데이터 테이블 스키마
│   └── insert_dummy_data.py          # 더미 데이터 insert script
├── debezium/
│   ├── .env
│   └── debezium_connect.py           # Debezium connector 요청 script
├── elasticsearch/
│   └── index_config.txt              # Elasticsearch 인덱스 설정
├── spark/
│   ├── configs/
│   │   ├── __init__.py
│   │   ├── .env
│   │   ├── env_config.py             # Env 설정 Load
│   │   └── schema.py                 # Kafka 메시지 스키마 관리
│   ├── jobs/
│   │   ├── __init__.py
│   │   ├── kafka_consumer.py         # Kafka 메시지 소비 모듈
│   │   ├── spark_aggregator.py       # Spark 집계 로직 정의
│   │   └── elasticsearch_writer.py   # Elasticsearch 저장 모듈
│   └── app.py                        # Spark Driver Main Application
├── docker-compose.yml
├── requirements.txt                  # 스크립트 실행 시 필요한 종속성
└── README.md