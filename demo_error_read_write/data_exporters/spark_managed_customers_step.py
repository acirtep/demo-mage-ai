from demo_error_read_write.data_setup.utils import get_delta_spark_session
from pandas import DataFrame
from pathlib import Path
from pyspark.sql.types import StructType,StructField, StringType, IntegerType
import os


if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data(**kwargs):
    """
    Exports data to some source

    Args:
        df (DataFrame): Data frame to export to

    Output (optional):
        Optionally return any object and it'll be logged and
        displayed when inspecting the block run.
    """    
    
    filepath = os.getenv('DATA_OUTPUT_LANDING_ZONE')
    filename_in= f"{filepath}/customers.txt"
    filename_out = f"{filepath}/delta/customers/schema"
    
    spark_session = get_delta_spark_session()
    
    schema = StructType([ \
        StructField("id",IntegerType(),True), \
        StructField("email_address",StringType(),True), \
        StructField("first_name",StringType(),True), \
        StructField("last_name", StringType(), True)
      ])
    
    df_in = spark_session.read.option(
            'delimiter', '\t').option(
            'header', 'true').schema(schema).csv(filename_in)
    
    df_in.write.mode("overwrite").format("delta").save(filename_out)
