-- user_activity_log 테이블: 사용자 행동 로그
CREATE TABLE user_activity_log (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,    -- 기본 키
    user_id BIGINT NOT NULL,                 -- 사용자 ID
    product_id BIGINT NOT NULL,              -- 상품 ID
    product_name VARCHAR(255) NOT NULL,      -- 상품 이름
    product_price FLOAT NOT NULL,            -- 상품 가격
    event_type VARCHAR(50) NOT NULL,         -- 행동 유형
    timestamp DATETIME NOT NULL              -- 행동 시간
);