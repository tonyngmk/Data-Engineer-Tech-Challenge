from dateutil.relativedelta import relativedelta
import datetime

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StringType, ByteType
from pyspark.sql.functions import length, regexp_extract, when, sha2, substring, regexp_extract, trim, lit, date_format, to_date, coalesce


def init_spark():
    spark = SparkSession.builder.appName('govtech_challenge').getOrCreate()
    return spark

def read(upstream_dir):
    """
    read folder that specifically contains data of
    membership applications of e-commerce platform
    """
    spark = init_spark()
    defined_schema = StructType() \
    .add("name", StringType(), True) \
    .add("email", StringType(), True) \
    .add("date_of_birth", StringType(), True) \
    .add("mobile_no", StringType(), True)

    sdf = spark.read.format("csv").load(upstream_dir, header=True, schema=defined_schema)
    sdf = sdf.withColumn('is_successful', lit(1).cast(ByteType())) # add new col
    return sdf

def process_mobile_no(input_sdf):
    sdf = input_sdf.withColumn("mobile_no", regexp_extract(input_sdf.mobile_no, r'\d+', 0).alias('mobile_no'))
    condition = length(sdf.mobile_no) == 8
    sdf = sdf.withColumn("condition", when(condition, 1).otherwise(0))
    sdf = sdf.withColumn("is_successful", sdf.is_successful.bitwiseAND(sdf.condition).alias('is_successful'))
    sdf = sdf.drop('condition')
    return sdf

def parse_date(date_col):
    """
    parse all date formats from str to date type
    """
    date_formats = ["yyyy-MM-dd",
                    "yyyy MM dd",
                    "MM/dd/yyyy",
                    "yyyy/MM/dd",
                    "dd-MM-yyyy"]
    return coalesce(*[to_date(date_col, format) for format in date_formats])

def process_dob(input_sdf):
    sdf = input_sdf.withColumn("date_of_birth", parse_date(input_sdf.date_of_birth).alias('date_of_birth'))

    acceptable_date_from = (datetime.date(2022, 1, 1) - relativedelta(years=18)).strftime('%Y-%m-%d')
    condition = sdf.date_of_birth < (lit(acceptable_date_from))
    sdf = sdf.withColumn("condition", when(condition, 1).otherwise(0))
    sdf = sdf.withColumn("is_successful", sdf.is_successful.bitwiseAND(sdf.condition).alias('is_successful'))
    sdf = sdf.drop('condition')
    sdf = sdf.withColumn("date_of_birth", date_format(sdf.date_of_birth, "yyyyMMdd").alias('date_of_birth'))
    sdf = sdf.withColumn('sha256_dob', substring(sha2(sdf.date_of_birth, 256).alias('sha256_dob'), 0, 5))
    return sdf

def process_email(sdf):
    email_regex_pattern = r'^[-_A-Za-z0-9]+@[-_A-Za-z0-9]+\.(?:com|net)$'
    condition = sdf.email.rlike(email_regex_pattern)
    sdf = sdf.withColumn("condition", when(condition, 1).otherwise(0))
    sdf = sdf.withColumn("is_successful", sdf.is_successful.bitwiseAND(sdf.condition).alias('is_successful'))
    sdf = sdf.drop('condition')
    return sdf

def process_name(input_sdf):
    first_last_name_regex = r'([A-Za-z]+)\s+([A-Za-z]+)'

    sdf = input_sdf\
    .withColumn("first_name", regexp_extract(input_sdf.name, first_last_name_regex, 1).alias('first_name'))\
    .withColumn("last_name", regexp_extract(input_sdf.name, first_last_name_regex, 2).alias('last_name'))

    condition = trim(sdf.name) != ''
    sdf = sdf.withColumn("condition", when(condition, 1).otherwise(0))
    sdf = sdf.withColumn("is_successful", sdf.is_successful.bitwiseAND(sdf.condition).alias('is_successful'))
    sdf = sdf.drop('condition')
    return sdf

def process_all(sdf):
    sdf = process_mobile_no(sdf)
    sdf = process_dob(sdf)
    sdf = process_email(sdf)
    sdf = process_name(sdf)
    return sdf


def output_file(sdf_output):
    sdf_output_success = sdf_output.filter('is_successful=1').coalesce(1)
    sdf_output_failed = sdf_output.filter('is_successful=0').coalesce(1)

    current_datehour = datetime.datetime.now().strftime('%Y-%m-%d-%H')
    output_dir = "/Users/tonyngmk/repo/Data-Engineer-Tech-Challenge/1-data-pipelines/data/output"
    success_output_dir = f"{output_dir}/success/{current_datehour}"
    failure_output_dir = f"{output_dir}/failure/{current_datehour}"

    sdf_output_success.write.format("csv").option("header", "true").mode('overwrite').save(success_output_dir)
    print(f"Success file written as: {success_output_dir}")
    sdf_output_failed.write.format("csv").option("header", "true").mode('overwrite').save(failure_output_dir)
    print(f"Failure file written as: {failure_output_dir}")

    total_rows = sdf_output.count()
    print(f"Success proportion: {sdf_output_success.count()}/{total_rows}")
    print(f"Failed proportion: {sdf_output_failed.count()}/{total_rows}")


if __name__ == "__main__":
    sdf = read("data/input")
    sdf = process_all(sdf)
    output_file(sdf)