FROM python:3.9-slim

# jdk 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-17-jre-headless \
    wget curl ca-certificates \
  && rm -rf /var/lib/apt/lists/*

# 라이브러리 설치
RUN pip install pyspark==3.4.4 python-dotenv

WORKDIR /app
COPY spark/ /app/