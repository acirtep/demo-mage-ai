from pandas import DataFrame
from sqlalchemy import create_engine
import json
import pandas as pd
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

    conn = create_engine("postgresql://postgres:postgres@postgres_db:5432/postgres")
    conn = conn.connect()
    filepath = os.getenv('DATA_OUTPUT_LANDING_ZONE')
    filepath = f"{filepath}/customers.txt"
    
    df = pd.read_csv(filepath, sep='\t')
    
    conn.execute("drop table if exists raw_customers_managed")
    
    conn.execute("""create table raw_customers_managed(
        id integer primary key,
        email_address varchar(320) not null unique,
        first_name varchar(100),     
        last_name varchar(100),
        inserted_datetime timestamp not null default current_timestamp 
    )
    """)
    
    df[['id', 'email_address', 'first_name', 'last_name']].to_sql('raw_customers_managed', con=conn, if_exists='append', index=False)
