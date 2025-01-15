-- product_info 테이블: 상품 정보 저장
CREATE TABLE product_info (
    product_id BIGINT PRIMARY KEY,           -- 상품 ID
    category_id SMALLINT NOT NULL,           -- 상품 카테고리 ID
    product_name VARCHAR(255) NOT NULL,      -- 상품 이름
    price FLOAT NOT NULL                     -- 상품 가격
);

-- user_activity_log 테이블: 사용자 행동 로그
CREATE TABLE user_activity_log (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,    -- 기본 키
    user_id BIGINT NOT NULL,                 -- 사용자 ID
    event_type VARCHAR(50) NOT NULL,         -- 행동 유형
    product_id BIGINT NOT NULL,              -- 상품 ID
    timestamp DATETIME NOT NULL,             -- 행동 시간
    FOREIGN KEY (product_id) REFERENCES product_info(product_id)
);