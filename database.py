import boto3, json, os, logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

key=os.getenv("KEY")
assert key, "Missing KEY in .env"

def get_db_config(secret_name: str, region_name: str):
    session = boto3.Session(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=region_name
    )
    client = session.client("secretsmanager")
    secret = client.get_secret_value(SecretId=secret_name)
    return json.loads(secret["SecretString"])

try:
    db_config = get_db_config(key, "eu-north-1")
except Exception as e:
    logging.error(f"SecretsManager error: {e}")
    raise

#URL: postgresql://username:password@host:port/dbname
SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg2://{db_config['username']}:{db_config['password']}"
    f"@{db_config['host']}:{db_config['port']}/{db_config['dbname']}")
#print(db_config)
cloud_engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=cloud_engine)
Base = declarative_base() #root of the ORM system; therefore, it is located in database.py (technically it could sit in orm_model.py, too)