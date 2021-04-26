import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os

####################################
# Get global keys
pg_auth = os.environ.get("PG_AUTH")

# Heroku global variables
host = os.environ.get("HEROKU_HOST")
dbname = os.environ.get("DB_NAME")
user = os.environ.get("USER")
password = os.environ.get("PASSWORD")
####################################

###################
# CREATE DATABASE #
###################

### Connect to PostgreSQL DBMS
# con = psycopg2.connect(host="localhost", user="postgres", password=pg_auth)
# con = psycopg2.connect(host=host,
#                        user=user,
#                        password=password)
# con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

### Obtain a DB Cursor
# cursor = con.cursor()

### Create DB
# sqlCreateDatabase = "CREATE DATABASE investment_db;"
# cursor.execute(sqlCreateDatabase)


################
# CREATE TABLE #
################

### Connect to PostgreSQL database
postgresConnection = psycopg2.connect(host=host,
                                      dbname=dbname,
                                      user=user,
                                      password=password)

cur = postgresConnection.cursor()

## Create table for the stock indexes (S&P 500, Dow, NASDAQ)
cur.execute("""
                CREATE TABLE indexes(
                id SERIAL PRIMARY KEY,
                datetime DATE,
                snp_500 NUMERIC,
                snp_500_delta NUMERIC,
                snp_500_delta_perc NUMERIC,
                dow_30 NUMERIC,
                dow_30_delta NUMERIC,
                dow_30_delta_perc NUMERIC,
                nasdaq NUMERIC,
                nasdaq_delta NUMERIC,
                nasdaq_delta_perc NUMERIC
            )
            """)

### Create table for company profiles
cur.execute("""
               CREATE TABLE company_profile(
               id SERIAL PRIMARY KEY,
               date DATE,
               name VARCHAR(128),
               sector VARCHAR(128),
               industry VARCHAR(128),
               employee_count INTEGER
            )
            """)

### Create table for stock prices
cur.execute("""
               CREATE TABLE stock_prices(
               id SERIAL PRIMARY KEY,
               date DATE,
               name VARCHAR(128),
               price NUMERIC,
               delta_price NUMERIC,
               delta_price_perc NUMERIC,
               top_3_news VARCHAR(256),
               news_source VARCHAR(256)
            )
            """)


###############
# ALTER TABLE #
###############

# indexes
cur.execute("""
                ALTER TABLE indexes
                RENAME TO market_index
            """)

cur.execute("""
                ALTER TABLE market_index
                RENAME COLUMN datetime
                TO date
            """)

cur.execute("""
                ALTER TABLE market_index
                ALTER COLUMN date TYPE TIMESTAMP
            """)

# company_profile
cur.execute("""
                ALTER TABLE company_profile
                ALTER COLUMN date TYPE TIMESTAMP
            """)

# stock_prices
cur.execute("""
                ALTER TABLE stock_prices
                RENAME TO stock_price
            """)

cur.execute("""
                ALTER TABLE stock_price
                ALTER COLUMN date TYPE TIMESTAMP
            """)

cur.execute("""
                ALTER TABLE stock_price
                ALTER COLUMN top_3_news TYPE TEXT
            """)

cur.execute("""
                ALTER TABLE stock_price
                ALTER COLUMN news_source TYPE TEXT
            """)

postgresConnection.commit()
