from demo_error_read_write.data_setup.utils import get_delta_spark_session
from pandas import DataFrame
from pathlib import Path
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
    filename_in= f"{filepath}/orders.txt"
    filename_out = f"{filepath}/delta/orders/auto"
    
    spark_session = get_delta_spark_session()
    
    df_in = spark_session.read.option(
            'delimiter', '\t').option(
            'header', 'true').option('inferschema', 'true').csv(filename_in)

    df_in.write.mode("overwrite").format("delta").save(filename_out) 
