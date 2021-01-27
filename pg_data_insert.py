import psycopg2
import json
import ast
import helper_functions as hf
import os
from datetime import datetime
import sys

def pipe_data(file_name):

    start = datetime.now()

    # Global variables
    file_path = "/Users/nikhilsawal/OneDrive/investment_portfolio/datafiles/"
    file_name = file_name
    pg_auth = os.environ.get("PG_AUTH")

    # Database credentials
    conn = psycopg2.connect(host="localhost",
                            user="postgres",
                            dbname="investment_db",
                            password=pg_auth)
    cur = conn.cursor()

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

    with open(file_path+file_name) as inpFile:

        for i, j in enumerate(inpFile):
            id = i+1

            try:
                values = (tuple([id] + list(ast.literal_eval(j).values())))
                cur.execute(sql, values)
                conn.commit()
            except (ValueError, psycopg2.DatabaseError) as e:
                hf.slack_msg("```{}```".format(e))

    duration = datetime.now()-start

    hf.slack_msg("""
    ```
    script: {}.py,
    datafile: {},
    status: {},
    runtime: {}
    ```
    """.format("pg_data_insert", file_name, "Success", duration))

def main():

    pipe_data("company_profile.jl")
    pipe_data("index.jl")
    pipe_data("stock_prices.jl")

if __name__ == "__main__":
    main()
