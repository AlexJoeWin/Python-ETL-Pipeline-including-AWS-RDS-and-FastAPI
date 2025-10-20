# EXTRACT FUNCTION
import pandas as pd
import logging

def extract(store_data, extra_data):
    extra_df = pd.read_parquet(extra_data)
    merged_df = store_data.merge(extra_df, on="index")
    logging.info("Data has been merged.\n")
    logging.debug(
        f"Dataframe shape post merging: {merged_df.shape}\n")
    return merged_df