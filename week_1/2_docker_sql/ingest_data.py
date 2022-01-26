#!/usr/bin/env python
# coding: utf-8

from traceback import print_last
import pandas as pd
import argparse
import os
from time import time
from sqlalchemy import create_engine

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    csv = 'data.csv'
    os.system(f'wget {url} -O {csv}')

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    engine.connect()

    df_iter = pd.read_csv(csv, iterator=True, chunksize=100000)
    df = next(df_iter)
    df['tpep_pickup_datetime'] = pd.to_datetime(df.tpep_pickup_datetime)
    df['tpep_dropoff_datetime'] = pd.to_datetime(df.tpep_dropoff_datetime)
    df.head(0).to_sql(name=table_name, con=engine, if_exists='replace')
    df.to_sql(name=table_name, con=engine, if_exists='append')

    try:
        while True:
            t_start = time()
            df = next(df_iter)
            df['tpep_pickup_datetime'] = pd.to_datetime(df.tpep_pickup_datetime)
            df['tpep_dropoff_datetime'] = pd.to_datetime(df.tpep_dropoff_datetime)
            df.to_sql(name=table_name, con=engine, if_exists='append')
            t_end = time()
            print(f'Chunk inserted in {t_end - t_start}')
    except StopIteration:
        print('Data ingested.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV')

    parser.add_argument('--user',help='user name for postgres')
    parser.add_argument('--password',help='password for postgres')
    parser.add_argument('--host',help='host for postgres')
    parser.add_argument('--port',help='port for postgres')
    parser.add_argument('--db',help='database for postgres')
    parser.add_argument('--table_name',help='table name in postgres')
    parser.add_argument('--url',help='url of csv')

    args = parser.parse_args()

    main(args)
