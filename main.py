import logging

import awswrangler as wr
import boto3
import pandas as pd

logger = logging.getLogger("etl")


#  TODO: error handling, testing
def get_excel_data_df(filename: str):
    # TODO: csv parameters
    """read excel file into a DataFrame"""
    input_df = pd.read_excel(filename)
    return input_df


def write_df_to_csv(df: pd.DataFrame, path: str):
    """Writes a DataFrame to AWS s3 bucket csv file"""
    wr.s3.to_csv(df, path, index=False, line_terminator="\n")
    logger.info("Writing data to %s.", path)


def create_database(db_name: str):
    """Creates a Glue database if it doesn't exist"""
    databases = wr.catalog.databases()

    if db_name not in databases.values:
        wr.catalog.create_database("visits")
        logger.info("Creating database visits.")
    else:
        logger.info("Database %s already exists.", db_name)


def get_column_types(df: pd.DataFrame, file_format: str, index: bool = False):
    column_types, _ = wr.catalog.extract_athena_types(
        df=df, file_format=file_format, index=index
    )
    return column_types


def create_db_table(table: str, database: str, path: str, column_types):
    """Creates a Glue table in the database from the file"""
    wr.catalog.create_csv_table(
       table=table,
       database=database,
       path=path,
       columns_types=column_types
    )

def main():
    model_filename="./modelling-1.xlsx"
    model_s3_csv_path="s3://wr-visits/visits/visits.csv"
    glue_database="visits"
    table="visits"
    visits_df = get_excel_data_df(model_filename)
    write_df_to_csv(visits_df, model_s3_csv_path)
    create_database(glue_database)
    column_types = get_column_types(visits_df,"csv")
    create_db_table(table, glue_database, model_s3_csv_path)
if __name__ == "__main__":
    main()
