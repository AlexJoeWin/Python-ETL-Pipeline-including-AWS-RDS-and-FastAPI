# LOAD FUNCTION
from database import cloud_engine
def load(cleaned_data):
    cleaned_data.to_sql("sales", con=cloud_engine, if_exists="replace", index=False)