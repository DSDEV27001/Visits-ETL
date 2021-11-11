import logging

import awswrangler as wr
import boto3.session
import pandas as pd
import botocore.exceptions as be

logger = logging.getLogger("etl")

# TODO: add error handling for all functions
# TODO: testing using pytest
# TODO: CI using black, pylint, lizard, flake8, bandit, and pytest


def get_aws_session():
    try:
        aws_session = boto3.session.Session()
        logger.info("Created boto3 default session.")
        return aws_session
    except be.ValidationError as e:
        logger.error("Validation Error. Unable to create default session with boto3.")
        raise e
    except be.ConnectionError as e:
        logger.error("Connection Error. Unable to create default session with boto3.")
        raise e
    except be.NoCredentialsError as e:
        logger.error(
            "No credentials supplied. Unable to create default session with boto3."
        )
        raise e
    except BaseException as e:
        logger.error("Unknown error. Unable to create default session with boto3.")
        raise e


def get_excel_data_df(filename: str):
    # TODO: excel parameters
    """read excel file into a DataFrame"""
    input_df = pd.read_excel(filename)
    return input_df


def write_df_to_parquet(df: pd.DataFrame, path: str, boto_session):
    """Writes a DataFrame to AWS s3 bucket csv file"""
    try:
        wr.s3.to_parquet(df, path, index=False, boto3_session=boto_session)
        logger.info("Writing data to %s.", path)
    except be.ValidationError as e:
        logger.error("Unable to write to s3 parquet file with AWS wrangler.")
        raise e


def create_database(db_name: str):
    """Creates a Glue database if it doesn't exist"""
    databases = wr.catalog.databases()

    if db_name not in databases.values:
        wr.catalog.create_database("visits")
        logger.info("Creating database visits.")
    else:
        logger.info("Database %s already exists.", db_name)


def get_column_types(df: pd.DataFrame, file_format: str, index: bool = False):
    """"""
    column_types, _ = wr.catalog.extract_athena_types(
        df=df, file_format=file_format, index=index
    )
    return column_types


def create_db_table(table: str, database: str, path: str, column_types):
    """Creates a Glue table in the database from the file"""
    wr.catalog.create_parquet_table(
        table=table, database=database, path=path, columns_types=column_types
    )


def create_parquet_table_from_sql(id_name: str, fields: str, s3_path: str):
    """Create parquet file"""
    sql = f""" 

    CREATE TABLE IF NOT EXISTS visits_parq ({id_name} INT AUTO_INCREMENT PRIMARY KEY)

       WITH (format='PARQUET', external_location={s3_path}) AS 

     SELECT 

       {fields}

     FROM 

       visits

    """

    return wr.athena.read_sql_query(sql=sql, database="visits", ctas_approach=False)


def main():
    model_filename = "./modelling-1.xlsx"
    model_s3_path = "s3://wr-visits/visits/"
    model_s3_parquet_path = f"{model_s3_path}visits.prq"
    visits_s3_parquet_path = f"{model_s3_path}visits-table.prq"
    glue_database = "visits"
    model_table = "visits"
    visit_table_id_name = "`visit_id_surrogate`"
    visit_table_fields = "`visit_id`,`visit_start_date`,`visit_end_date`,`visit_cost`"
    # Reads excel file into a pandas dataframe
    visits_df = get_excel_data_df(model_filename)
    # Writes df to csv file in s3 bucket
    write_df_to_parquet(visits_df, model_s3_parquet_path)
    # Create glue database
    create_database(glue_database)
    # Extract the column names and types
    column_types = get_column_types(visits_df, "csv")
    # Create glue catalogue entry
    create_db_table(model_table, glue_database, model_s3_parquet_path, column_types)
    # Creates parquet file
    parquet_df = create_parquet_table_from_sql(
        visit_table_id_name, visit_table_fields, visits_s3_parquet_path
    )


if __name__ == "__main__":
    main()
