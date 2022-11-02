from pandas import DataFrame
from sqlalchemy import create_engine
import json
import pandas as pd
import os 


if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data(df, **kwargs):
    """
    Exports data to some source

    Args:
        df (DataFrame): Data frame to export to

    Output (optional):
        Optionally return any object and it'll be logged and
        displayed when inspecting the block run.
    """

    conn = create_engine("postgresql://postgres:postgres@postgres_db:5432/postgres")
    conn = conn.connect()
    cut_off_date = kwargs["cut_off_date"]
    
    conn.execute(f"delete from raw_customer where cut_off_date='{cut_off_date}'")
    
    df[['id', 'email_address', 'first_name', 'last_name', 'cut_off_date']].to_sql(
        'raw_customer', schema='public',con=conn, if_exists='append', index=False)
