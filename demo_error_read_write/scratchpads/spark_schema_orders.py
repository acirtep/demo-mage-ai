import os
from demo_error_read_write.data_setup.utils import get_delta_spark_session
from pathlib import Path
from pyspark.sql.types import StructType,StructField, StringType, IntegerType, DecimalType, TimestampType, ArrayType
from pyspark.sql.functions import array, col, explode, split, from_json


filepath = os.getenv('DATA_OUTPUT_LANDING_ZONE')
filename_in= f"{filepath}/orders.txt"
filename_out = f"{filepath}/delta/orders/schema"

spark_session = get_delta_spark_session()

jsobn_type = ArrayType(StructType(
    [
        StructField("product_id", IntegerType()),
        StructField("amount", IntegerType())
    ]
))


schema = StructType([ \
    StructField("id",IntegerType(),True), \
    StructField("order_timestamp",TimestampType(),True), \
    StructField("customer_id",IntegerType(),True), \
    StructField("order_status", StringType(), True), \
    StructField("order_amount", DecimalType(), True), \
    StructField("order_currency", StringType(), True), \
    StructField("products", StringType(), True)
  ])

df_in = spark_session.read.option(
        'delimiter', '\t').option(
        'header', 'true').schema(schema).csv(filename_in)

df2 = df_in.withColumn("products", from_json(col("products"), schema=jsobn_type))

df2.printSchema()


df.write.mode("overwrite").format("delta").save(filename_out)
df_out = spark_session.read.format('delta').load(filename_out)

df_out.printSchema()
print(f"Size {sum(file.stat().st_size for file in Path(filename_out).rglob('*'))} bytes")