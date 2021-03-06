# -*- coding: utf-8 -*-
"""
Script to read the santized xmls and store the output as parquet files
"""
from pyspark.sql import DataFrame, SparkSession
from constants import SANITIZED_STORAGE_NAME, SANITIZED_CONTAINER_NAME, PARQUET_CONTAINER_NAME, \
    PARQUET_STORAGE_NAME, PARQUET_OUTPUT_FOLDER
from launcher import logger
from spark_utils import save
from utils import create_spark_session


LOGGER_CHILD_NAME = "PARQUETIZER"
logger = logger.getChild(LOGGER_CHILD_NAME)
NUM_OUTPUT_FILES = 116  # TODO parametrize from num files and size


def run_parquetizer(spark: SparkSession):
    logger.info("Starting execution")
    df = read(spark)
    result = process(df)
    save(spark=spark, df=result, num_files=NUM_OUTPUT_FILES, containter_name=PARQUET_CONTAINER_NAME,
         storage_name=PARQUET_STORAGE_NAME, output_folder=PARQUET_OUTPUT_FOLDER, logger=logger)
    logger.info("Process finished!")
    return result


def read(spark: SparkSession) -> DataFrame:
    input_path = f"wasbs://{SANITIZED_CONTAINER_NAME}@{SANITIZED_STORAGE_NAME}.blob.core.windows.net/"
    logger.info(f"Reading from: {input_path}")
    df = spark.read.format("com.databricks.spark.xml").option("rowTag", "questel-patent-document").option(
        "mode", "DROPMALFORMED").load(input_path)
    return df


def process(df: DataFrame) -> DataFrame:
    # TODO ¿flatten fields?
    return df


if __name__ == '__main__':
    spark_session = create_spark_session("parquetizer")
    run_parquetizer(spark_session)
