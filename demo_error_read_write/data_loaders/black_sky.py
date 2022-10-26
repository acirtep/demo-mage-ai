from demo_error_read_write.data_setup.utils import get_delta_spark_session
from pandas import DataFrame
from pathlib import Path
import os


if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data(**kwargs) -> DataFrame:
    """
    Template code for loading data from any source.

    Returns:
        DataFrame: Returned pandas data frame.
    """
    # Specify your data loading logic here

    filepath = os.getenv('DATA_OUTPUT_LANDING_ZONE')
    filename_in= f"{filepath}/orders.txt"
    filename_out = f"{filepath}/delta/orders/auto"
    
    spark_session = get_delta_spark_session()
    
    df_in = spark_session.read.option(
            'delimiter', '\t').option(
            'header', 'true').csv(filename_in)
    
    df_in.printSchema()
    
    df_in.write.mode("overwrite").format("delta").save(filename_out)
    df_out = spark_session.read.format('delta').load(filename_out)
    
    df_out.printSchema()
    return print(f"Size {sum(file.stat().st_size for file in Path(filename_out).rglob('*'))} bytes")


@test
def test_output(df) -> None:
    """
    Template code for testing the output of the block.
    """
    assert df is not None, 'The output is undefined'