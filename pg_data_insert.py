import psycopg2
import json
import ast
import helper_functions as hf
import os
from datetime import datetime
import sys

def pipe_data(file_name):

    """
    This piece of code perform the following opertions:
    1. Connect to database (investment_db)
    2. Custom builds the SQL script to pipe data into a specific table
    3. Iteratively pipes new data into the table
    4. Sends notification to slack about job completion or possible error messages
    """

    start = datetime.now()

    # Global variables
    file_path = "/Users/nikhilsawal/OneDrive/investment_portfolio/datafiles/"
    file_name = file_name
    pg_auth = os.environ.get("PG_AUTH")

    # Setup database credentials
    conn = psycopg2.connect(host="localhost",
                            user="postgres",
                            dbname="investment_db",
                            password=pg_auth)
    cur = conn.cursor()

    # Create custom SQL
    if file_name == "index.jl":
        sql = """INSERT INTO market_index
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING;"""
    elif file_name == "company_profile.jl":
        sql = """INSERT INTO company_profile
             VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING;"""
    elif file_name == "stock_prices.jl":
        sql = """INSERT INTO stock_price
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING;"""
    else:
        hf.slack_msg("```XXXXX {} not found in directory!!!! Check for possible renames!!```".format(file_name))
        sys.exit()

    # Pipe data to Postgres
    with open(file_path+file_name) as inpFile:
        unicode = ""
        for i, j in enumerate(inpFile):
            id = i+1

            try:
                values = (tuple([id] + list(ast.literal_eval(j).values())))
                cur.execute(sql, values)
                conn.commit()
                unicode = "\u2705"
                status = "Success"
            except (ValueError, psycopg2.DatabaseError) as e:
                hf.slack_msg("```{} at line number {} in file {}```".format(e, i, "\u274C"+file_name))
                unicode = "\u274C"
                status = "Fail"
                break

    duration = datetime.now()-start

    # Send Slack notifications
    hf.slack_msg("""
    ```
    script: {}.py,
    datafile: {},
    status: {},
    runtime: {}
    ```
    """.format("pg_data_insert", unicode+file_name, status, duration))

def main():

    # pipe_data("company_profile.jl")
    pipe_data("index.jl")
    pipe_data("stock_prices.jl")

if __name__ == "__main__":
    main()
