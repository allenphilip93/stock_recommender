from __future__ import annotations

import json
from io import StringIO
from textwrap import dedent

import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

import pandas as pd
import psycopg2
import yfinance as yf


with DAG(
    "data_collector_dag",
    default_args={"retries": 0},
    # [END default_args]
    description="DAG tutorial",
    schedule="@once",
    start_date=datetime.datetime(2021, 1, 1),
    catchup=False,
    tags=["stocks"],
) as dag:

    dag.doc_md = __doc__
    
    # [START extract_function]
    def extract(**kwargs):
        print("Extract")

    # [END extract_function]

    # [START transform_function]
    def transform(**kwargs):
        print("Extract")

    # [END transform_function]

    # [START load_function]
    def load(**kwargs):
        print("Load equity listing")
        URL = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
        eq_listing = pd.read_csv(URL)
        eq_listing = eq_listing[['SYMBOL', 'NAME OF COMPANY', ' SERIES']]
        eq_listing = eq_listing.rename(columns={
            eq_listing.columns[0]: "ticker",
            eq_listing.columns[1]: "name",
            eq_listing.columns[2]: "industry"
        })
        eq_listing.info()
        
        conn = psycopg2.connect(
            host="timescaledb",
            port="5432",
            dbname="stocks",
            user="admin",
            password="password",
            connect_timeout=5
        )
        with conn.cursor() as cursor:
            # Truncate the existing table (i.e. remove all existing rows)
            cursor.execute(f"TRUNCATE stock_tickers CASCADE")
            conn.commit()
        upload_to_db_efficiently(conn, eq_listing, "stock_tickers")
        
#         with conn.cursor() as cursor:
#             # Truncate the existing table (i.e. remove all existing rows)
#             cursor.execute(f"TRUNCATE stock_prices")
#             conn.commit()
        
        try :
            # stock_data = pd.DataFrame()
            for name in eq_listing.ticker:
                try:
                    print(f"Adding {name} ... ")
                    stock_data = yf.download(f'{name}.NS')
                    stock_data = stock_data.reset_index() # remove the index
                    stock_data["ticker"] = name # add a column for the ticker
                    stock_data = stock_data.rename(columns={
                        "Date": "time",
                        "Open": "open",
                        "High": "high",
                        "Low": "low",
                        "Close": "close",
                        "Adj Close": "close_adj",
                        "Volume": "volume",
                    })
                    stock_data.head()
                    print("Inserting records to DB")
                    upload_to_db_efficiently(conn, stock_data, "stock_prices")
                    # stock_data = pd.concat([stock_data, data])
                except Exception as e:
                    print(f'Exception has occurred!')
                    print(f'{name} ===> {e}')
        finally:
            conn.close()
        
    # [END load_function]
    
    def upload_to_db_efficiently(conn, df, table_name="public.stock_prices"):
        """
        Upload the stock price data to the TimescaleDB database as quickly and efficiently
        as possible by truncating (i.e. removing) the existing data and copying all-new data
        """

        with conn.cursor() as cursor:
            # Truncate the existing table (i.e. remove all existing rows)
#             cursor.execute(f"TRUNCATE {table_name} CASCADE")
#             conn.commit()

            # Now insert the brand-new data
            # Initialize a string buffer
            sio = StringIO()
            # Write the Pandas DataFrame as a CSV file to the buffer
            sio.write(df.to_csv(index=None, header=None))
            # Be sure to reset the position to the start of the stream
            sio.seek(0)
            cursor.copy_from(
                file=sio,
                table=table_name,
                sep=",",
                null="",
                size=8192,
                columns=df.columns
            )
            conn.commit()
            print(f"Inserted {len(df)} rows to {table_name}")
                
    
    # [START main_flow]
    extract_task = PythonOperator(
        task_id="fetch_equity_listing",
        python_callable=extract,
    )
    extract_task.doc_md = dedent(
        """\
    #### Extract task
    A simple Extract task to get data ready for the rest of the data pipeline.
    In this case, getting data is simulated by reading from a hardcoded JSON string.
    This data is then put into xcom, so that it can be processed by the next task.
    """
    )

    transform_task = PythonOperator(
        task_id="transform",
        python_callable=transform,
    )
    transform_task.doc_md = dedent(
        """\
    #### Transform task
    A simple Transform task which takes in the collection of order data from xcom
    and computes the total order value.
    This computed value is then put into xcom, so that it can be processed by the next task.
    """
    )

    load_task = PythonOperator(
        task_id="collect_data",
        python_callable=load,
    )
    load_task.doc_md = dedent(
        """\
    #### Load task
    A simple Load task which takes in the result of the Transform task, by reading it
    from xcom and instead of saving it to end user review, just prints it out.
    """
    )

    extract_task >> transform_task >> load_task
