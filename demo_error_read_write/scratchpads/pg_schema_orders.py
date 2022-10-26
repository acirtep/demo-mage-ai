from sqlalchemy import create_engine
import pandas as pd 
import json


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

df_pg_catalog = pd.read_sql("select column_name, is_nullable, data_type, character_maximum_length, character_octet_length, numeric_precision, numeric_scale \
    from information_schema.columns where table_name='raw_orders_managed' order by ordinal_position", con=conn.connect())

df_pg_size = pd.read_sql("select pg_total_relation_size(quote_ident(table_name)) as table_size \
    from information_schema.tables where table_name = 'raw_orders_managed'", con=conn.connect())
print("              ")
print(f"Orders As saved in the db : {df_pg_size['table_size'].values[0]} bytes")
df_pg_catalog