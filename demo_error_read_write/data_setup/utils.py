from sqlalchemy import create_engine
from pyspark.sql import SparkSession


def get_pg_conn():
    conn_string = f'postgresql://postgres:postgres@postgres_db:5432/postgres'
    db = create_engine(conn_string)
    return db.connect()


def get_delta_spark_session():
    spark_session = SparkSession.builder.appName('delta').config(
        'spark.ui.enabled', 'false').config(
        'spark.jars.packages', 'io.delta:delta-core_2.12:2.1.0').config(
        'spark.sql.extensions', 'io.delta.sql.DeltaSparkSessionExtension').config(
        'spark.sql.catalog.spark_catalog', 'org.apache.spark.sql.delta.catalog.DeltaCatalog').getOrCreate()
    spark_session.sparkContext.setLogLevel('ERROR')
    return spark_session
