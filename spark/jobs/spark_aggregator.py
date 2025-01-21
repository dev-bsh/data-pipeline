from pyspark.sql import DataFrame
from pyspark.sql.functions import (
    window, col, when, approx_count_distinct, sum as spark_sum
)

def anchored_window():
    """
    10초 단위(정각) 윈도우를 정의.
    매 00~10s, 10~20s, ... 구간으로 끊기 위해:
      window(timeCol, windowDuration, slideDuration, startTime)
    """
    return window(col("timestamp"), "10 seconds", "10 seconds", "0 second").alias("time_window")

def aggregate_unique_users(df: DataFrame) -> DataFrame:
    """
    10초 단위 고유 사용자 수
    """
    w = anchored_window()
    grouped = df.groupBy(w)

    df_agg = grouped.agg(approx_count_distinct("user_id").alias("unique_users"))
    df_agg_result = df_agg.select(
        col("time_window.start").alias("window_start"),
        col("time_window.end").alias("window_end"),
        "unique_users"
    )

    return df_agg_result

def aggregate_avg_purchase_amount(df: DataFrame) -> DataFrame:
    """
    10초 단위 전체(전역) 구매 횟수 및 금액 합계
    """
    w = anchored_window()
    grouped = df.groupBy(w)

    total_purchase_amount = spark_sum(when(col("event_type") == "purchase", col("product_price")).otherwise(0)).alias("total_purchase_amount")
    purchase_count = spark_sum(when(col("event_type") == "purchase", 1).otherwise(0)).alias("purchase_count")

    df_agg = grouped.agg(total_purchase_amount, purchase_count)

    df_agg_result = df_agg.select(
        col("time_window.start").alias("window_start"),
        col("time_window.end").alias("window_end"),
        "total_purchase_amount",
        "purchase_count"
    )

    return df_agg_result

def aggregate_product_views(df: DataFrame) -> DataFrame:
    """
    10초 단위 '상품별' 조회수 집계
    """
    w = anchored_window()
    grouped = df.groupBy(w, "product_id", "product_name")

    view_count = spark_sum(when(col("event_type") == "view", 1).otherwise(0)).alias("view_count")

    df_agg = grouped.agg(view_count)
    df_agg_result = df_agg.select(
        col("time_window.start").alias("window_start"),
        col("time_window.end").alias("window_end"),
        "product_id",
        "product_name",
        "view_count"
    )

    return df_agg_result

def aggregate_purchase_conversion(df: DataFrame) -> DataFrame:
    """
    10초 단위 '상품별' 구매 전환율
    conversion_rate = purchase_count / view_count
    """
    w = anchored_window()
    grouped = df.groupBy(w, "product_id", "product_name")

    view_count = spark_sum(when(col("event_type") == "view", 1).otherwise(0)).alias("view_count")
    purchase_count = spark_sum(when(col("event_type") == "purchase", 1).otherwise(0)).alias("purchase_count")

    df_agg = grouped.agg(view_count, purchase_count)
    df_agg_result = df_agg.select(
        col("time_window.start").alias("window_start"),
        col("time_window.end").alias("window_end"),
        "product_id",
        "product_name",
        "view_count",
        "purchase_count",
        when(col("view_count") > 0, col("purchase_count") / col("view_count")).otherwise(0).alias("purchase_conversion_rate")
    )

    return df_agg_result
