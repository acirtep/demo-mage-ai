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

    filepath = os.getenv('DATA_OUTPUT_LANDING_ZONE')
    filepath = f"{filepath}/orders.txt"
    
    df = pd.read_csv(filepath, sep='\t')
    conn = create_engine("postgresql://postgres:postgres@postgres_db:5432/postgres")
    conn = conn.connect()
    
    conn.execute("drop table if exists raw_orders_managed")
    
    conn.execute("""create table raw_orders_managed(
        id integer primary key,
        order_timestamp timestamp not null,
        customer_id integer not null,
        order_status varchar(10) not null,
        order_amount decimal(10,2) not null,
        order_currency varchar(3) not null,
        products jsonb,
        inserted_datetime timestamp not null default current_timestamp 
    )
    """)
    
    df['products'] = df['products'].apply(json.dumps)
    
    df[['id', 'order_timestamp', 'customer_id', 'order_status', 'order_amount', 'order_currency', 'products']].to_sql('raw_orders_managed', con=conn, if_exists='append', index=False)