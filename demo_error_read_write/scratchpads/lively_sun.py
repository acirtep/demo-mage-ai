import os
from demo_error_read_write.data_setup.utils import get_delta_spark_session
from pathlib import Path
from pyspark.sql.types import StructType,StructField, StringType, IntegerType


filepath = os.getenv('DATA_OUTPUT_LANDING_ZONE')
filename_in= f"{filepath}/customers.txt"
filename_out = f"{filepath}/delta/orders/schema"

spark_session = get_delta_spark_session()

df = spark_session.read.format('delta').load(filename_out)

df.printSchema()

df.select('id').show()