import os
from demo_error_read_write.data_setup.utils import get_delta_spark_session
from pathlib import Path
from pyspark.sql.types import StructType,StructField, StringType, IntegerType


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

df_in.printSchema()

df_in.write.mode("overwrite").format("delta").save(filename_out)
df_out = spark_session.read.format('delta').load(filename_out)

df_out.printSchema()
print(f"Size {sum(file.stat().st_size for file in Path(filename_out).rglob('*'))} bytes")