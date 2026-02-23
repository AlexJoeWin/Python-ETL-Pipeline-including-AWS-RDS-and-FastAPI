import logging

from fastapi import FastAPI, Depends
from typing import List

from database import SessionLocal
from sqlalchemy.orm import Session

from etl_runner import run_etl
from Config.orm_model import Sales
from Config.schema import SalesScheme

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/run")
def trigger_etl():
    try:
        logging.info("ETL trigger received")
        run_etl()
        logging.info("ETL completed successfully")
        return {"status": "ETL complete"}
    except Exception as e:
        logging.warning(f"ETL failed: {e}", exc_info=True)
        return {"error": str(e)}

@app.get("/check", response_model = List[SalesScheme])
def get_sales(db: Session = Depends(get_db)):
    logging.info("Data retrieved")
    return db.query(Sales).all()

@app.get("/")
def health_check():
    return {"status": "FastAPI is running"}

@app.get("/ping")
def ping():
    return {"message": "pong"}