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

# 상품 더미 데이터
PRODUCT_LIST = [
    (1001, 'Wireless Mouse', 25.99),
    (1002, 'Mechanical Keyboard', 79.99),
    (1003, 'USB-C Hub', 39.99),
    (1004, 'Webcam', 49.99),
    (1005, 'Gaming Chair', 199.99),
    (1006, 'Standing Desk', 299.99),
    (1007, 'Monitor Arm', 89.99),
    (1008, 'Noise Cancelling Headphones', 129.99),
    (1009, 'Portable Speaker', 59.99),
    (1010, 'Smartwatch', 199.99),
    (1011, 'Laptop Stand', 39.99),
    (1012, 'External SSD', 129.99),
    (1013, 'Bluetooth Adapter', 19.99),
    (1014, 'Gaming Mouse Pad', 15.99),
    (1015, 'RGB Light Strip', 29.99),
    (1016, 'Microphone', 99.99),
    (1017, 'Capture Card', 149.99),
    (1018, 'Fitness Tracker', 49.99),
    (1019, 'Resistance Bands', 19.99),
    (1020, 'Yoga Mat', 29.99)
]

def insert_dummy_data():
    """
    MySQL 데이터베이스에 랜덤 더미 데이터를 지속적으로 삽입하는 함수

    - 랜덤한 사용자 ID, 상품 ID, 상품 이름, 상품 가격, 이벤트 타입, 현재 시각을 생성
    - 생성된 데이터를 1초 간격으로 DB에 삽입
    """
    try:
        connection =pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()

        while True:
            user_id = random.randint(101, 200)
            product = random.choice(PRODUCT_LIST)
            product_id = product[0]
            product_name = product[1]
            produc_price = product[2]
            event_type = random.choice(EVENT_TYPE)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            query = """
                INSERT INTO user_activity_log(user_id, product_id, product_name, product_price, event_type, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(query, (user_id, product_id, product_name, produc_price, event_type,  timestamp))
            connection.commit()

            print(f"Inserted: user_id={user_id}, product={product} event_type={event_type}, timetamp={timestamp}")
            
            # 1초 대기
            time.sleep(1)

    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    insert_dummy_data()