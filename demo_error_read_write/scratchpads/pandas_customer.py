import pandas as pd
import os
from sqlalchemy import create_engine

filepath = os.getenv('DATA_OUTPUT_LANDING_ZONE')
filepath = f"{filepath}/customers.txt"

df = pd.read_csv(filepath, sep='\t')

print('Pandas dataframe')
print(' ')
df.info(verbose=True)

conn = create_engine("postgresql://postgres:postgres@postgres_db:5432/postgres")

df_pg_catalog = pd.read_sql("select column_name, is_nullable, data_type, character_maximum_length, character_octet_length, numeric_precision, numeric_scale \
    from information_schema.columns where table_name='raw_customers_pandas'", con=conn.connect())

df_pg_size = pd.read_sql("select pg_total_relation_size(quote_ident(table_name)) as table_size \
    from information_schema.tables where table_name = 'raw_customers_pandas'", con=conn.connect())
print("              ")
print(f"As saved in the db : {df_pg_size['table_size'].values[0]} bytes")
df_pg_catalog