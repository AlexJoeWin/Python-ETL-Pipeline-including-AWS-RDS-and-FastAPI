# 🧪 ETL Pipeline with FastAPI & AWS RDS Integration

A modular ETL pipeline built with FastAPI, SQLAlchemy, and Pandas. Designed for secure cloud deployment, this project extracts, transforms, and loads sales data from local and external sources into a PostgreSQL database, with endpoints for triggering ETL and querying results.

> ⚠️ **Note:** This project was built solely for learning and testing purposes on a local machine. It is not configured for production use or public deployment.



## 📁 Project Structure
```

ETL pipeline poject/
├── .venv/ 						# Virtual environment (excluded from Git)
├── .env 						# Environment variables (excluded from Git)
├── .gitignore 					# Git ignore rules
├── Config/
│ ├── __init__.py
│ ├── models.py 				# SQLAlchemy ORM model
│ └── schemas.py 				# Pydantic schema for API responses
├── ETL/
│ ├── __init__.py
│ ├── extraction.py 			# Merges store and external data
│ ├── transform.py 				# Cleans and validates data
│ └── load.py 					# Loads cleaned data into PostgreSQL
├── database.py 				# AWS SecretsManager + SQLAlchemy engine setup
├── etl_runner.py				# Orchestrates ETL steps
├── main.py 					# FastAPI app with endpoints
├── extra_data.parquet 			# External data source
├── sales_data.db 				# Local SQLite source (for extraction)
├── requirements.txt 			# Python dependencies

```

---

## 🚀 Features

- **FastAPI REST endpoints**:
  - `POST /run` — Trigger ETL pipeline
  - `GET /check` — Retrieve cleaned data
  - `GET /` — Health check
  - `GET /ping` — Ping endpoint (for testing purposes)

- **ETL Pipeline**:
  - Extracts from local SQLite and external Parquet
  - Cleans missing values and validates types
  - Loads into PostgreSQL using SQLAlchemy
  - Logic essentially builds on previous project: /AlexJoeWin/Python-ETL-Pipeline

- **Security**:
  - Secrets (DB credentials) fetched securely via AWS Secrets Manager
  - `.env` used for local paths and keys (never committed)

---

## 🔐 Environment Setup

Create a `.env` file with the following keys:

```env
KEY=your_aws_secret_name
FILE_PATH=./extra_data.parquet
DB_PATH=sqlite:///sales_data.db

```

Ensure `.env` is listed in `.gitignore` to prevent accidental commits.

----------

## ☁️ AWS RDS Setup Guide

This section outlines how to provision a PostgreSQL database on AWS RDS, securely store credentials in Secrets Manager, and configure IAM access for local development.

----------

### 🗄️ Create a RDS Database in AWS Console

1.  **Engine**: PostgreSQL
2.  **Template**: Sandbox (pre-fills default values)
3.  **DB Cluster Identifier**: Choose a unique name
4.  **Master Username**: Set an admin username
5.  **Credentials Management**:
    -   Choose _Self-managed_
    -   Enable _Auto-generate password_
6.  **Public Access**: Enable to assign a public IP
7.  **Initial Database Name**: Set your desired DB name
8.  ✅ **Important**: View and save credentials after creation.

----------

### 🔐 Configure VPC Security Groups

On the setting page of the newly created database select the defined VPC Security; prevent traffic from all sources and ports and create instead:

-   **Inbound Rules**:
    -   Type: PostgreSQL
    -   Port: 5432
    -   Source: _My IP_ (restrict access to your machine)
-   **Outbound Rules**:
    
    -   Same configuration as inbound

----------

### 🔑 Store Credentials in AWS Secrets Manager

1.  **Create a New Secret**:
    
    -   Type: _Credentials for RDS database_
    -   Fields: Use the same `Username` and `Password` from database setup
2.  **Secret Name**:
    
    -   Set a descriptive name (e.g. `prod/db/credentials`)
    -   This will be used as the `KEY` in your `.env` file
3.  ✅ **Important**: View and save the Secret ARN — needed for IAM policy.
    

----------

### 👤 Create IAM User for CLI Access

1.  **Create a new IAM user**
2.  **Attach permissions**:
    -   Directly attach `AmazonRDSFullAccess`
    -   Additionally, add an inline policy for Secrets Manager access:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "secretsmanager:GetSecretValue",
        "secretsmanager:DescribeSecret"
      ],
      "Resource": "<Your Secret ARN>*"
    }
  ]
}

```

3.  **Create Access Keys**:
    -   Save the **Access Key** and **Secret Access Key** after generation.

----------

### 🧰 Configure AWS CLI Locally

Run the following in your terminal:

```bash
aws configure
```

Enter:

-   **Access Key**: from IAM user
-   **Secret Access Key**: from IAM user
-   **Region**: e.g. `eu-central-1`
-   **Output format**: `json`

----------


## 🧰 Installation

```bash

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

```

----------

## 🧪 Running the App

```bash
# Run the app
fastapi dev main.py

```

Then test the endpoints using `curl` in your CLI:

-   `curl http://localhost:8000/` → health check
-   `curl -X POST http://localhost:8000/run` → trigger ETL pipeline
-   `curl http://localhost:8000/check` → retrieve cleaned data

----------


## 📊 Sales Data Model

| Field         | Type     | Description                                  |
|---------------|----------|----------------------------------------------|
| `index`       | Integer  | Primary key, unique identifier               |
| `Store_ID`    | Integer  | Store identifier                             |
| `Date`        | String   | Date of the record                           |
| `Dept`        | Integer  | Department number                            |
| `Weekly_Sales`| String   | Weekly sales amount                          |
| `IsHoliday`   | Integer  | Holiday indicator (1 = holiday, 0 = regular) |
| `Temperature` | Float    | Temperature at the store location            |
| `Fuel_Price`  | Float    | Local fuel price                             |
| `CPI`         | Float    | Consumer Price Index                         |
| `Unemployment`| Float    | Unemployment rate                            |
| `Type`        | Float    | Store type code                              |
| `Size`        | Float    | Store size in square feet                    |




----------

## 📦 Dependencies

-   `fastapi`
-   `sqlalchemy`
-   `pandas`
-   `python-dotenv`
-   `boto3`
-   `psycopg2-binary`
-   `pydantic`
-   `logging`
-   `typing`
-   `json`
-   `pydantic`

## 📄 License

This project is licensed under the [MIT License](./LICENSE).  
You are free to use, modify, and distribute this code for personal or commercial purposes, provided that the original copyright and license notice are retained.

⚠️ **Note:** This project was built solely for learning and testing purposes on a local machine. It is not configured for production use or public deployment.
