# MAIN
import os, sqlalchemy, logging
import pandas as pd
from dotenv import load_dotenv
from ETL.extraction import extract
from ETL.transform import transform
from ETL.load import load

def run_etl():
    load_dotenv()
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)

    file_path=os.getenv("FILE_PATH")
    db_path=os.getenv("DB_PATH")

    assert file_path, "Missing FILE_PATH in .env"
    assert db_path, "Missing DB_PATH in .env"

    db_engine=sqlalchemy.create_engine(db_path)
    df_sales=pd.read_sql("SELECT * FROM Sales", con=db_engine)
    logging.debug(f"Dataframe shape prior merging:{df_sales.shape}\n")

    merged_df = extract(df_sales, file_path)
    cleaned_df= transform(merged_df)
    load(cleaned_df)