import os
from demo_error_read_write.data_setup.utils import get_delta_spark_session
from pathlib import Path

filepath = os.getenv('DATA_OUTPUT_LANDING_ZONE')
filename_in= f"{filepath}/customers.txt"
filename_out = f"{filepath}/delta/customers/auto"

spark_session = get_delta_spark_session()

df_in = spark_session.read.option(
        'delimiter', '\t').option(
        'header', 'true').option('inferschema', 'true').csv(filename_in)

df_in.printSchema()

df_in.write.mode("overwrite").format("delta").save(filename_out)
df_out = spark_session.read.format('delta').load(filename_out)

df_out.printSchema()

print(f"Size {sum(file.stat().st_size for file in Path(filename_out).rglob('*'))} bytes")