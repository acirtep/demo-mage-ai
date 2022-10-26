from sqlalchemy import create_engine
import pandas as pd 
import json

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

df_pg_catalog = pd.read_sql("select column_name, is_nullable, data_type, character_maximum_length, character_octet_length, numeric_precision, numeric_scale \
    from information_schema.columns where table_name='raw_customers_managed' order by ordinal_position", con=conn.connect())

df_pg_size = pd.read_sql("select pg_total_relation_size(quote_ident(table_name)) as table_size \
    from information_schema.tables where table_name = 'raw_customers_managed'", con=conn.connect())
print("              ")
print(f"Customers As saved in the db : {df_pg_size['table_size'].values[0]} bytes")
df_pg_catalog