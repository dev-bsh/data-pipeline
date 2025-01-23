from pyspark.sql import DataFrame
from pyspark.sql.streaming import DataStreamWriter
from config.env_config import ES_COMMON_OPTIONS

def write_to_elasticsearch(df: DataFrame, index_name: str, output_mode: str) -> DataStreamWriter:
    """
    DataFrame을 Elasticsearch에 스트리밍으로 저장하는 함수

    Args:
        df (DataFrame): 저장할 데이터프레임
        index_name (str): Elasticsearch 인덱스 이름
        output_mode (str): 출력 모드 ('append', 'update', 'complete')
    """

    checkpoint_path = "/tmp/checkpoints/" + index_name

    return (df.writeStream
        .outputMode(output_mode)
        .format("org.elasticsearch.spark.sql")
        .options(**ES_COMMON_OPTIONS)
        .option("es.resource", index_name)
        .option("checkpointLocation", checkpoint_path)
        .start())
