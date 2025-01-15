import random
import time
import pymysql
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="./.env")

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT")),
}

# 행동 유형 리스트
EVENT_TYPE = [
    "view", "add_to_cart", "purchase"
]

def insert_dummy_data():
    """
    MySQL 데이터베이스에 랜덤 더미 데이터를 지속적으로 삽입하는 함수

    - 랜덤한 유저 ID, 상품 ID, 이벤트 타입, 현재 시간을 생성
    - 생성된 데이터를 1초 간격으로 DB에 삽입
    """
    try:
        connection =pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()

        while True:
            user_id = random.randint(101, 200)
            event_type = random.choice(EVENT_TYPE)
            product_id = random.randint(1001, 1020)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            query = """
                INSERT INTO user_activity_log(user_id, event_type, product_id, timestamp)
                VALUES (%s, %s, %s, %s)
            """
            
            cursor.execute(query, (user_id, event_type, product_id, timestamp))
            connection.commit()

            print(f"Inserted: user_id={user_id}, event_type={event_type}, product_id={product_id}, timetamp={timestamp}")
            
            # 1초 대기
            time.sleep(1)

    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    insert_dummy_data()